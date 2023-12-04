from sqlalchemy import text, insert, select, update, func, Integer, cast, and_
from sqlalchemy.orm import aliased
from slides.src.database import sync_engine, session_factory, async_session_factory, Base
from slides.models import WorkerOrm, ResumesOrm, WorkLoad


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
        worker_bob = WorkerOrm(username='Bob')
        worker_john = WorkerOrm(username='John')
        with session_factory() as session:
            session.add_all([worker_jack, worker_michael])
            session.add(worker_bob)
            session.add(worker_john)
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

    @staticmethod
    def insert_resumes():
        with sync_engine.connect() as conn:
            stmt = insert(ResumesOrm).values(
                [
                    {"title":
                         "Python Junior Developer",
                     "compensation": 50000,
                     "workload": WorkLoad.fulltime,
                     "worker_id": 1},
                    {"title":
                         "Python Разработчик",
                     "compensation": 150000,
                     "workload": WorkLoad.fulltime,
                     "worker_id": 2},
                    {"title":
                         "Python Data Engineer",
                     "compensation": 250000,
                     "workload": WorkLoad.parttime,
                     "worker_id": 1},
                    {"title":
                         "Data Scientist",
                     "compensation": 300000,
                     "workload": WorkLoad.fulltime,
                     "worker_id": 2},
                ]
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_resumes_avg_compensation(like_language: str = 'Python'):
        """select workload, avg(compensation)::int as avg_compensation
            from resumes
            where title like '%Python%' and compensation > 40000
            group by workload
        """
        with session_factory() as session:
            query = (
                select(ResumesOrm.workload,
                       cast(func.avg(ResumesOrm.compensation), Integer).label('avg_compensation'),
                       )
                .select_from(ResumesOrm)
                .filter(and_(
                    ResumesOrm.title.contains(like_language),
                    ResumesOrm.compensation > 40000,
                ))
                .group_by(ResumesOrm.workload)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = session.execute(query)
            reuslt = res.all()
            print(reuslt)

    @staticmethod
    def insert_additional_resumes():
        with sync_engine.connect() as conn:
            workers = [
                {"username": "Artem"},
                {"username": "Petr"},
                {"username": "Roman"},
            ]
            resumes = [
                {"title": "Python Программист", "compensation": 60000, "workload": WorkLoad.fulltime, "worker_id": 3},
                {"title": "Machine Learning Engineer", "compensation": 70000, "workload": WorkLoad.fulltime,
                 "worker_id": 3},
                {"title": "Python Data Scientst", "compensation": 80000, "workload": WorkLoad.parttime, "worker_id": 4},
                {"title": "Python Analyst", "compensation": 90000, "workload": WorkLoad.fulltime, "worker_id": 4},
                {"title": "Python Junior Developer", "compensation": 10000, "workload": WorkLoad.parttime,
                 "worker_id": 5},
            ]
            insert_workers = insert(WorkerOrm).values(workers)
            insert_resumes = insert(ResumesOrm).values(resumes)
            conn.execute(insert_workers)
            conn.execute(insert_resumes)
            conn.commit()

    async def join_cte_subquery_window_func(like_language: str = 'Python'):
        """WITH helper2 AS (
                SELECT *, compensation-avg_workload_compensation AS compensation_diff
	            FROM
	            (SELECT
                    w.id,
                    w.username,
                    r.compensation,
                    r.workload,
                    avg(compensation) OVER (PARTITION BY workload)::int AS avg_workload_compensation

            FROM resumes r
            JOIN workers w ON r.worker_id = w.id) helper1
        )
        SELECT * FROM helper2
        ORDER BY compensation_diff DESC;
        """
        async with async_session_factory() as session:
            r = aliased(ResumesOrm)
            w = aliased(WorkerOrm)
            subq = (
                select(
                    r,
                    w,
                    func.avg(r.compensation).over(partitionby=r.workload).label('avg_workload_compensation'),
                )
                .join(r, r.worker_id == w.id).subquery("helper1")
            )
            cte = (
                select(
                    subq.c.id,
                    subq.c.username,
                    subq.c.compensation,
                    subq.c.workload,
                    subq.c.avg_workload_compensation,
                    (subq.c.compensation - subq.c.avg_workload_compensation).label("compensation_diff")
                )
                .cte("helper2")
            )
            query = (
                select(cte)
                .order_by(cte.c.compensation_diff.desc())
            )

            res = await session.execute(query)
            result = res.all()


async def async_insert_data():
    async with async_session_factory() as session:
        worker_bobr = WorkerOrm(username='Bobr')
        worker_volk = WorkerOrm(username='Volk')
        session.add_all([worker_bobr, worker_volk])
        await session.commit()
