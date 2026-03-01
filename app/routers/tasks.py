from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from app.dependencies import get_current_user, check_project_owner, check_task_access

router = APIRouter(tags=["tasks"])

@router.post("/projects/{project_id}/tasks/", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    project_id: int,
    task_data: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Проверка доступа к проекту
    check_project_owner(project_id, current_user, db)
    
    # Проверка исполнителя
    if task_data.assignee_id:
        assignee = db.query(models.User).filter(models.User.id == task_data.assignee_id).first()
        if not assignee:
            raise HTTPException(status_code=400, detail="Исполнитель не найден")
    
    new_task = models.Task(
        title=task_data.title,
        description=task_data.description,
        project_id=project_id,
        assignee_id=task_data.assignee_id
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "status": new_task.status,
        "project_id": new_task.project_id,
        "assignee_id": new_task.assignee_id,
        "created_at": new_task.created_at,
        "updated_at": new_task.updated_at,
        "assignee_username": new_task.assignee.username if new_task.assignee else None
    }

@router.patch("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task_data: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    task = check_task_access(task_id, current_user, db)
    
    # Обновление полей
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.status is not None:
        if task_data.status not in ["todo", "in_progress", "done"]:
            raise HTTPException(status_code=400, detail="Неверный статус")
        task.status = task_data.status
    if task_data.assignee_id is not None:
        if task_data.assignee_id:
            assignee = db.query(models.User).filter(models.User.id == task_data.assignee_id).first()
            if not assignee:
                raise HTTPException(status_code=400, detail="Исполнитель не найден")
        task.assignee_id = task_data.assignee_id
    
    db.commit()
    db.refresh(task)
    
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "project_id": task.project_id,
        "assignee_id": task.assignee_id,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
        "assignee_username": task.assignee.username if task.assignee else None
    }

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    task = check_task_access(task_id, current_user, db)
    db.delete(task)
    db.commit()
    return None