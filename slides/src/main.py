import asyncio
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from queries.core import SyncCore
from queries.orm import SyncORM

SyncORM.create_tables()
# SyncCore.create_tables()

# SyncORM.insert_workers()

# SyncCore.insert_workers()
SyncORM.insert_workers()

# SyncCore.select_workers()
# SyncCore.update_worker()

SyncORM.select_workers()
SyncORM.update_worker()

# asyncio.run(async_insert_data())