from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


# Enums
class SeverityLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ScanStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ProgrammingLanguage(str, Enum):
    PYTHON = "python"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"


# Auth Schemas
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


# Project Schemas
class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    git_url: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    git_url: Optional[str]
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    code_snapshot_path: Optional[str]

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    last_scan_health_score: Optional[int] = None
    last_scan_date: Optional[datetime] = None
    total_smells: int = 0

    class Config:
        from_attributes = True


# Collaborator Schemas
class CollaboratorAdd(BaseModel):
    email: EmailStr


class CollaboratorResponse(BaseModel):
    id: int
    user_id: int
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


# Scan Schemas
class ScanCreate(BaseModel):
    project_id: int


class ScanResponse(BaseModel):
    id: int
    project_id: int
    status: ScanStatus
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    health_score: Optional[int]
    total_smells: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    error_message: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ScanDetailResponse(ScanResponse):
    smells: List["SmellResponse"] = []


# Smell Schemas
class SmellResponse(BaseModel):
    id: int
    smell_type: str
    severity: SeverityLevel
    file_path: str
    line_number: Optional[int]
    class_name: Optional[str]
    method_name: Optional[str]
    description: str
    suggestion: Optional[str]
    code_snippet: Optional[str]
    language: ProgrammingLanguage
    created_at: datetime

    class Config:
        from_attributes = True


class SmellFilter(BaseModel):
    severity: Optional[SeverityLevel] = None
    smell_type: Optional[str] = None
    language: Optional[ProgrammingLanguage] = None


# Trend Data
class TrendDataPoint(BaseModel):
    date: datetime
    health_score: int
    total_smells: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int


class TrendResponse(BaseModel):
    project_id: int
    project_name: str
    data_points: List[TrendDataPoint]


# Pagination
class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    page_size: int
    total_pages: int


# Update forward reference
ScanDetailResponse.model_rebuild()