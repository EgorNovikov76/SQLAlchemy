from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from slides.models import WorkLoad

class WorkersAddDTO(BaseModel):
    username: str

class WorkersDTO(WorkersAddDTO):
    id: int

class ResumesAddDTO(BaseModel):
    title: str
    compensation: Optional[int]
    workerload: WorkLoad
    worker_id: int

class ResumesDTO(ResumesAddDTO):
    id: int
    created_at: datetime
    updated_at: datetime

class ResumesRelDTO(ResumesDTO):
    worker: "WorkerDTO"

class WorkersRelDTO(WorkersDTO):
    resumes: list["ResumesDTO"]