from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models import Project, Scan, ArchitectureSmell, ProjectCollaborator, ScanStatus, SeverityLevel
from app.schemas import ScanCreate, ScanResponse, ScanDetailResponse, SmellResponse, TrendResponse, TrendDataPoint
from app.services.scan_service import ScanService

router = APIRouter(prefix="/scans", tags=["Scans"])


@router.post("/", response_model=ScanResponse, status_code=status.HTTP_201_CREATED)
async def create_scan(
    scan_data: ScanCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # Check project access
    result = await db.execute(select(Project).where(Project.id == scan_data.project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check access
    if project.owner_id != user_id:
        collab_result = await db.execute(
            select(ProjectCollaborator).where(
                ProjectCollaborator.project_id == project.id,
                ProjectCollaborator.user_id == user_id
            )
        )
        if not collab_result.scalar_one_or_none():
            raise HTTPException(status_code=403, detail="Access denied")
    
    # Create scan record
    scan = Scan(
        project_id=scan_data.project_id,
        status=ScanStatus.PENDING
    )
    db.add(scan)
    await db.flush()
    await db.refresh(scan)
    
    # Start scan in background (would be Celery task in production)
    scan_service = ScanService(db)
    await scan_service.start_scan(scan.id)
    
    return scan


@router.get("/project/{project_id}", response_model=List[ScanResponse])
async def list_project_scans(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # Check project access
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner_id != user_id:
        collab_result = await db.execute(
            select(ProjectCollaborator).where(
                ProjectCollaborator.project_id == project.id,
                ProjectCollaborator.user_id == user_id
            )
        )
        if not collab_result.scalar_one_or_none():
            raise HTTPException(status_code=403, detail="Access denied")
    
    scans_result = await db.execute(
        select(Scan).where(Scan.project_id == project_id).order_by(Scan.created_at.desc())
    )
    scans = scans_result.scalars().all()
    
    return scans


@router.get("/{scan_id}", response_model=ScanDetailResponse)
async def get_scan(
    scan_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(
        select(Scan).where(Scan.id == scan_id).options()
    )
    scan = result.scalar_one_or_none()
    
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    # Check project access
    project_result = await db.execute(select(Project).where(Project.id == scan.project_id))
    project = project_result.scalar_one_or_none()
    
    if project.owner_id != user_id:
        collab_result = await db.execute(
            select(ProjectCollaborator).where(
                ProjectCollaborator.project_id == project.id,
                ProjectCollaborator.user_id == user_id
            )
        )
        if not collab_result.scalar_one_or_none():
            raise HTTPException(status_code=403, detail="Access denied")
    
    # Get smells
    smells_result = await db.execute(
        select(ArchitectureSmell).where(ArchitectureSmell.scan_id == scan_id)
    )
    smells = smells_result.scalars().all()
    
    return ScanDetailResponse(
        id=scan.id,
        project_id=scan.project_id,
        status=scan.status,
        started_at=scan.started_at,
        completed_at=scan.completed_at,
        health_score=scan.health_score,
        total_smells=scan.total_smells,
        critical_count=scan.critical_count,
        high_count=scan.high_count,
        medium_count=scan.medium_count,
        low_count=scan.low_count,
        error_message=scan.error_message,
        created_at=scan.created_at,
        smells=[SmellResponse.model_validate(s) for s in smells]
    )


@router.get("/project/{project_id}/trends", response_model=TrendResponse)
async def get_project_trends(
    project_id: int,
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # Check project access
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner_id != user_id:
        collab_result = await db.execute(
            select(ProjectCollaborator).where(
                ProjectCollaborator.project_id == project.id,
                ProjectCollaborator.user_id == user_id
            )
        )
        if not collab_result.scalar_one_or_none():
            raise HTTPException(status_code=403, detail="Access denied")
    
    # Get scans within the time range
    start_date = datetime.utcnow() - timedelta(days=days)
    scans_result = await db.execute(
        select(Scan).where(
            Scan.project_id == project_id,
            Scan.status == ScanStatus.COMPLETED,
            Scan.completed_at >= start_date
        ).order_by(Scan.completed_at)
    )
    scans = scans_result.scalars().all()
    
    data_points = [
        TrendDataPoint(
            date=scan.completed_at,
            health_score=scan.health_score,
            total_smells=scan.total_smells,
            critical_count=scan.critical_count,
            high_count=scan.high_count,
            medium_count=scan.medium_count,
            low_count=scan.low_count
        )
        for scan in scans
    ]
    
    return TrendResponse(
        project_id=project_id,
        project_name=project.name,
        data_points=data_points
    )


@router.get("/{scan_id}/smells", response_model=List[SmellResponse])
async def get_scan_smells(
    scan_id: int,
    severity: Optional[SeverityLevel] = None,
    smell_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(Scan).where(Scan.id == scan_id))
    scan = result.scalar_one_or_none()
    
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    # Check project access
    project_result = await db.execute(select(Project).where(Project.id == scan.project_id))
    project = project_result.scalar_one_or_none()
    
    if project.owner_id != user_id:
        collab_result = await db.execute(
            select(ProjectCollaborator).where(
                ProjectCollaborator.project_id == project.id,
                ProjectCollaborator.user_id == user_id
            )
        )
        if not collab_result.scalar_one_or_none():
            raise HTTPException(status_code=403, detail="Access denied")
    
    # Build query
    query = select(ArchitectureSmell).where(ArchitectureSmell.scan_id == scan_id)
    if severity:
        query = query.where(ArchitectureSmell.severity == severity)
    if smell_type:
        query = query.where(ArchitectureSmell.smell_type == smell_type)
    
    smells_result = await db.execute(query)
    smells = smells_result.scalars().all()
    
    return [SmellResponse.model_validate(s) for s in smells]