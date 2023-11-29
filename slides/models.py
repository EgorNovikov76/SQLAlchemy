from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from slides.src.database import Base

metadata_obj = MetaData()


#
# workers_table = Table(
#     'workers',
#     metadata_obj,
#     Column('id', Integer, primary_key=True),
#     Column('username', String(255)),
# )


class WorkerOrm(Base):
    __tablename__ = 'workers'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
