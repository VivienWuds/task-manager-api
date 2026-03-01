from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

# Пользователи
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# Токены
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Проекты
class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    task_count: int = 0
    
    class Config:
        orm_mode = True

class ProjectDetailResponse(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    tasks: List["TaskResponse"] = []
    
    class Config:
        orm_mode = True

# Задачи
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    assignee_id: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    assignee_id: Optional[int] = None

class TaskResponse(TaskBase):
    id: int
    status: str
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    assignee_username: Optional[str] = None
    
    class Config:
        orm_mode = True