from sqlalchemy import text, insert
from slides.src.database import sync_engine, async_engine, session_factory, async_session_factory
from slides.models import WorkerOrm, metadata_obj


def create_tables():
    sync_engine.echo = False
    metadata_obj.drop_all(bind=sync_engine)
    metadata_obj.create_all(bind=sync_engine)
    sync_engine.echo = True


def insert_data():
    worker_bobr = WorkerOrm(username='Bobr')
    worker_volk = WorkerOrm(username='Volk')
    with session_factory() as session:
        session.add(worker_bobr)
        session.add(worker_volk)
        session.commit()

