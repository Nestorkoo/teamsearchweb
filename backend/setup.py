from database import get_session, engine, SessionDep
from models import Base
import asyncio

async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(setup_db())