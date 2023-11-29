from datetime import datetime
from typing import Optional, Annotated
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from slides.src.database import Base, str_256
import enum

intpk = Annotated[int, mapped_column(Integer, primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.utcnow,
)]


class WorkerOrm(Base):
    __tablename__ = 'workers'

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column()


class WorkLoad(enum.Enum):
    parttime = 'parttime'
    fulltime = 'fulltime'


class ResumesOrm(Base):
    __tablename__ = 'resumes'

    id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[int | None]
    workload: Mapped[WorkLoad]
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id', ondelete='CASCADE'))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
