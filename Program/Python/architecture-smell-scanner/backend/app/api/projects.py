from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from typing import List, Optional
import os
import uuid
import aiofiles
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.core.config import settings
from app.models import Project, ProjectCollaborator, User, Scan, ScanStatus
from app.schemas import (
    ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse,
    CollaboratorAdd, CollaboratorResponse, PaginatedResponse
)

router = APIRouter(prefix="/projects", tags=["Projects"])


def check_project_access(project: Project, user_id: int) -> bool:
    """Check if user has access to the project (owner or collaborator)"""
    if project.owner_id == user_id:
        return True
    return False


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    project = Project(
        name=project_data.name,
        description=project_data.description,
        git_url=project_data.git_url,
        owner_id=user_id
    )
    db.add(project)
    await db.flush()
    await db.refresh(project)
    return project


@router.get("/", response_model=PaginatedResponse)
async def list_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    sort_by: Optional[str] = Query("health_score", regex="^(name|health_score|created_at)$"),
    sort_order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # Build base query for projects user has access to
    base_query = select(Project).outerjoin(
        ProjectCollaborator, Project.id == ProjectCollaborator.project_id
    ).where(
        or_(Project.owner_id == user_id, ProjectCollaborator.user_id == user_id)
    )
    
    # Apply search filter
    if search:
        base_query = base_query.where(Project.name.ilike(f"%{search}%"))
    
    # Get total count
    count_query = select(func.count()).select_from(base_query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Apply sorting
    if sort_by == "name":
        order_col = Project.name
    elif sort_by == "created_at":
        order_col = Project.created_at
    else:
        order_col = Project.id
    
    if sort_order == "desc":
        base_query = base_query.order_by(order_col.desc())
    else:
        base_query = base_query.order_by(order_col.asc())
    
    # Apply pagination
    offset = (page - 1) * page_size
    base_query = base_query.offset(offset).limit(page_size)
    
    result = await db.execute(base_query)
    projects = result.scalars().all()
    
    # Get last scan info for each project
    project_list = []
    for project in projects:
        last_scan_query = select(Scan).where(
            Scan.project_id == project.id,
            Scan.status == ScanStatus.COMPLETED
        ).order_by(Scan.completed_at.desc()).limit(1)
        scan_result = await db.execute(last_scan_query)
        last_scan = scan_result.scalar_one_or_none()
        
        project_list.append(ProjectListResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            owner_id=project.owner_id,
            last_scan_health_score=last_scan.health_score if last_scan else None,
            last_scan_date=last_scan.completed_at if last_scan else None,
            total_smells=last_scan.total_smells if last_scan else 0
        ))
    
    # Sort project_list by health_score if needed
    if sort_by == "health_score":
        project_list.sort(
            key=lambda x: x.last_scan_health_score if x.last_scan_health_score is not None else 0,
            reverse=(sort_order == "desc")
        )
    
    total_pages = (total + page_size - 1) // page_size
    
    return PaginatedResponse(
        items=project_list,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(
        select(Project).where(Project.id == project_id).options(selectinload(Project.owner))
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if not check_project_access(project, user_id):
        raise HTTPException(status_code=403, detail="Access denied")
    
    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Only owner can update project")
    
    if project_data.name is not None:
        project.name = project_data.name
    if project_data.description is not None:
        project.description = project_data.description
    
    await db.flush()
    await db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Only owner can delete project")
    
    await db.delete(project)
    return None


@router.post("/{project_id}/upload", response_model=ProjectResponse)
async def upload_code_snapshot(
    project_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Only owner can upload code")
    
    if file.size and file.size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 100MB)")
    
    # Create storage directory
    project_dir = os.path.join(settings.STORAGE_PATH, str(project_id))
    os.makedirs(project_dir, exist_ok=True)
    
    # Save file
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"code_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}{file_ext}"
    file_path = os.path.join(project_dir, unique_filename)
    
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    project.code_snapshot_path = file_path
    await db.flush()
    await db.refresh(project)
    
    return project


# Collaborator endpoints
@router.post("/{project_id}/collaborators", response_model=CollaboratorResponse, status_code=status.HTTP_201_CREATED)
async def add_collaborator(
    project_id: int,
    collaborator_data: CollaboratorAdd,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Only owner can add collaborators")
    
    # Find user by email
    user_result = await db.execute(select(User).where(User.email == collaborator_data.email))
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot add yourself as collaborator")
    
    # Check if already a collaborator
    collab_result = await db.execute(
        select(ProjectCollaborator).where(
            ProjectCollaborator.project_id == project_id,
            ProjectCollaborator.user_id == user.id
        )
    )
    if collab_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User is already a collaborator")
    
    collaborator = ProjectCollaborator(project_id=project_id, user_id=user.id)
    db.add(collaborator)
    await db.flush()
    await db.refresh(collaborator)
    
    return CollaboratorResponse(
        id=collaborator.id,
        user_id=user.id,
        email=user.email,
        username=user.username,
        created_at=collaborator.created_at
    )


@router.get("/{project_id}/collaborators", response_model=List[CollaboratorResponse])
async def list_collaborators(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if not check_project_access(project, user_id):
        raise HTTPException(status_code=403, detail="Access denied")
    
    collab_result = await db.execute(
        select(ProjectCollaborator).where(ProjectCollaborator.project_id == project_id)
    )
    collabs = collab_result.scalars().all()
    
    collaborators = []
    for collab in collabs:
        user_result = await db.execute(select(User).where(User.id == collab.user_id))
        user = user_result.scalar_one()
        collaborators.append(CollaboratorResponse(
            id=collab.id,
            user_id=user.id,
            email=user.email,
            username=user.username,
            created_at=collab.created_at
        ))
    
    return collaborators


@router.delete("/{project_id}/collaborators/{collaborator_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_collaborator(
    project_id: int,
    collaborator_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Only owner can remove collaborators")
    
    collab_result = await db.execute(
        select(ProjectCollaborator).where(
            ProjectCollaborator.id == collaborator_id,
            ProjectCollaborator.project_id == project_id
        )
    )
    collab = collab_result.scalar_one_or_none()
    
    if not collab:
        raise HTTPException(status_code=404, detail="Collaborator not found")
    
    await db.delete(collab)
    return None