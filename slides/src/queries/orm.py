from sqlalchemy import text, insert, select, update
from slides.src.database import sync_engine, async_engine, session_factory, async_session_factory, Base
from slides.models import WorkerOrm

class SyncORM:
    @staticmethod
    def create_tables():
        sync_engine.echo = False
        Base.metadata.drop_all(bind=sync_engine)
        Base.metadata.create_all(bind=sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_data():
        worker_jack = WorkerOrm(username='Jeck')
        worker_michael = WorkerOrm(username='Michael')
        with session_factory() as session:
            session.add_all([worker_jack, worker_michael])
            session.flush()
            session.commit()

    @staticmethod
    def insert_workers():
        with sync_engine.connect() as conn:
            stmt = insert(WorkerOrm).values(
                [
                    {"username": "Jack"},
                    {"username": "Michael"},
                ]
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_workers():
        with session_factory() as session:
            query = select(WorkerOrm)
            result = session.execute(query)
            workers = result.scalar()
            print(f"{workers=}")

    @staticmethod
    def update_worker(worker_id: int = 2, new_username: str = "Misha"):
        with session_factory() as session:
            worker_michael = session.get(WorkerOrm, worker_id)
            worker_michael.username = new_username
            session.refresh(worker_michael)
            session.commit()




async def async_insert_data():
    async with async_session_factory() as session:
        worker_bobr = WorkerOrm(username='Bobr')
        worker_volk = WorkerOrm(username='Volk')
        session.add_all([worker_bobr, worker_volk])
        await session.commit()

