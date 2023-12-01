from sqlalchemy import text, insert, select, update
from slides.src.database import sync_engine, async_engine, session_factory, async_session_factory, Base
from slides.models import WorkerOrm, workers_table


class SyncCore:
    @staticmethod
    def create_tables():
        sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_workers():
        with sync_engine.connect() as conn:
            stmt = insert(workers_table).values(
                [
                    {"username": "Jack"},
                    {"username": "Michael"},
                ]
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_workers():
        with sync_engine.connect() as conn:
            query = select(workers_table)
            result = conn.execute(query)
            workers = result.all
            print(f"{workers=}")

    @staticmethod
    def update_worker(worker_id: int = 2, new_username: str = "Misha"):
        with sync_engine.connect() as conn:
            stmt = text("UPDATE workers SET username=:username WHERE id=:id")
            stmt = stmt.bindparams(username=new_username, id=worker_id)
            conn.execute(stmt)
            conn.commit()
