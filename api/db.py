import re
from os import getenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv
from pymongo.collation import Collation

from api.logger import log

load_dotenv()

db_client: AsyncIOMotorClient = None

# Lets address queries match regardless of checksum casing while still
# being able to use an index (unlike a $regex/i scan of every document).
# The indexes themselves are built by the indexer with this same collation -
# the API's mongo user may be read-only, so it never creates indexes itself.
CASE_INSENSITIVE_COLLATION = Collation(locale="en", strength=2)

# Upper bound for every operation (pymongo client-side operation timeout,
# also sent to the server as maxTimeMS), so an expensive public query can't
# keep the DB busy indefinitely. Keep it below nginx's proxy_read_timeout.
MONGO_TIMEOUT_MS = int(getenv("APP_MONGO_TIMEOUT_MS", default="20000"))


def _mask_mongo_uri(uri: str) -> str:
    return re.sub(r"://[^@/]+@", "://***:***@", uri)


async def get_db() -> AsyncIOMotorClient:
    db_name = getenv("APP_MONGO_DB", default="example")
    if db_client is None:
        log.warning('Connection is None, nothing to get.')
        return
    return db_client[db_name]


async def get_incentives_db() -> AsyncIOMotorDatabase:
    """The MoC Liquidity Mining incentives database (MoC_Incentive's
    `mocin_*` collections): APP_MONGO_DB, unless INCENTIVES_MONGO_DB names
    another database on the same server."""
    db_name = getenv("INCENTIVES_MONGO_DB") or getenv("APP_MONGO_DB", default="example")
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
        db_client = AsyncIOMotorClient(mongo_uri, timeoutMS=MONGO_TIMEOUT_MS)
        # Fail at startup, not on every request, when the server is
        # unreachable or its version unsupported by this pymongo
        server_info = await db_client.server_info()
        log.info(f"Connected to mongo! (version {server_info['version']}).")
    except Exception as e:
        log.error(
            f"Could not connect to mongo at {_mask_mongo_uri(mongo_uri)}: "
            f"{type(e).__name__}: {_mask_mongo_uri(str(e))}"
        )
        raise


async def close_db_connect():
    global db_client
    if db_client is None:
        log.warning('Connection is None, nothing to close.')
        return
    db_client.close()
    db_client = None
    log.info('Mongo connection closed.')

