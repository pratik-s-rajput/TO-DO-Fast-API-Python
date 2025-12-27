from fastapi import FastAPI
from app.db.database import engine
from app.db.base import Base
from app.api.v1.tasks import router as tasks_router
from app.api.v1.auth import router as auth_router

app = FastAPI(title="Todo API")

@app.get("/")
def root():
    return {"message": "Todo API is running"}


# create tables
Base.metadata.create_all(bind=engine)

# register routers
app.include_router(auth_router)
app.include_router(tasks_router)
