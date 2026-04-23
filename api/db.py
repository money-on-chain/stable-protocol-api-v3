from os import getenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv

from api.logger import log

load_dotenv()

db_client: AsyncIOMotorClient = None


async def get_db() -> AsyncIOMotorClient:
    db_name = getenv("APP_MONGO_DB", default="example")
    if db_client is None:
        log.warning('Connection is None, nothing to get.')
        return
    return db_client[db_name]


async def connect_and_init_db():
    global db_client
    mongo_uri = getenv("APP_MONGO_URI")
    if not mongo_uri or mongo_uri == "SET_VIA_APP_MONGO_URI_ENV":
        raise RuntimeError("APP_MONGO_URI environment variable is not set")
    try:
        db_client = AsyncIOMotorClient(mongo_uri)
        log.info('Connected to mongo.')
    except Exception as e:
        log.exception(f'Could not connect to mongo: {e}')
        raise


async def close_db_connect():
    global db_client
    if db_client is None:
        log.warning('Connection is None, nothing to close.')
        return
    db_client.close()
    db_client = None
    log.info('Mongo connection closed.')

