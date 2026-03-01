from fastapi import FastAPI
from app.routers import auth, projects, tasks

app = FastAPI(title="Task Manager API")

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Task Manager API работает!"}