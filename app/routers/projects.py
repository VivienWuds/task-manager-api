from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app import schemas, models
from app.database import get_db
from app.dependencies import get_current_user, check_project_owner

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", response_model=List[schemas.ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    projects = db.query(
        models.Project,
        func.count(models.Task.id).label("task_count")
    ).outerjoin(
        models.Task
    ).filter(
        models.Project.owner_id == current_user.id
    ).group_by(
        models.Project.id
    ).order_by(
        models.Project.created_at.desc()
    ).all()
    
    result = []
    for project, task_count in projects:
        project_dict = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "owner_id": project.owner_id,
            "created_at": project.created_at,
            "updated_at": project.updated_at,
            "task_count": task_count
        }
        result.append(project_dict)
    
    return result

@router.post("/", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_project = models.Project(
        name=project_data.name,
        description=project_data.description,
        owner_id=current_user.id
    )
    
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return {
        "id": new_project.id,
        "name": new_project.name,
        "description": new_project.description,
        "owner_id": new_project.owner_id,
        "created_at": new_project.created_at,
        "updated_at": new_project.updated_at,
        "task_count": 0
    }

@router.get("/{project_id}", response_model=schemas.ProjectDetailResponse)
def get_project_detail(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    project = check_project_owner(project_id, current_user, db)
    
    tasks = []
    for task in project.tasks:
        tasks.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "project_id": task.project_id,
            "assignee_id": task.assignee_id,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "assignee_username": task.assignee.username if task.assignee else None
        })
    
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "owner_id": project.owner_id,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "tasks": tasks
    }