from sqlalchemy import text, insert
from slides.src.database import sync_engine, async_engine
from slides.models import metadata_obj, workers_table


# def get_123():
#     with sync_engine.connect() as conn:
#         res = conn.execute(text("SELECT 1,2,3 union select 4,5,6"))
#         print(f"{res.first()=}")
#
# async def get_123_async():
#     async with async_engine.connect() as conn:
#         res = await conn.execute(text("SELECT 1,2,3 union select 4,5,6"))
#         print(f"{res.first()=}")

def create_tables():
    sync_engine.echo = False
    metadata_obj.drop_all(bind=sync_engine)
    metadata_obj.create_all(bind=sync_engine)
    sync_engine.echo = True


def insert_data():
    with sync_engine.connect() as conn:
        # smtm = """INSERT INTO workers (username) VALUES
        #     ('Bobr'),
        #     ('Volk');"""
        smtm = insert(workers_table).values(
            [
                {"username": "Bobr"},
                {"username": "Volk"},
            ]
        )
        conn.execute(smtm)
        conn.commit()
