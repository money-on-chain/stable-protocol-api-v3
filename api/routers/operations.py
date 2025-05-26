from fastapi import APIRouter, Query, HTTPException
from typing import Annotated

from api.db import get_db
from api.models.operations import OperationSummary, OperationsList, Operations, DATE_FIELDS, OperationsSummaryResponse
from api.utils import fields_date_to_str


router = APIRouter()


@router.get(
    "/v1/operations/list/",
    tags=["operations"],
    response_description="List operations of the given address user",
    response_model=OperationsList
)
async def operations_list(
        recipient: Annotated[str, Query(
            title="Recipient address",
            description="Recipient address",
            regex='^0x[a-fA-F0-9]{40}$')] = '0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3',
        limit: Annotated[int, Query(
            title="Limit",
            description="Limit",
            le=1000)] = 20,
        skip: Annotated[int, Query(
            title="Skip",
            description="Skip",
            le=10000)] = 0
):

    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {
        "$or": [
            {"params.recipient": {"$regex": recipient.lower(), '$options': 'i'}},
            {"params.sender": {"$regex": recipient.lower(), '$options': 'i'}},
            {"executed.recipient_": {"$regex": recipient.lower(), '$options': 'i'}},
            {"executed.sender_": {"$regex": recipient.lower(), '$options': 'i'}}
        ]
    }

    operations = await db["operations"]\
        .find(query_filter)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    operations_count = await db["operations"].count_documents(query_filter)

    for trx in operations:
        trx['_id'] = str(trx['_id'])

        fields_date_to_str(trx, DATE_FIELDS)

    # Last block indexed

    indexer = await db["moc_indexer"] \
        .find_one(sort=[("updatedAt", -1)])

    last_block_indexed = 0
    if indexer:
        if 'last_raw_tx_block' in indexer:
            last_block_indexed = indexer['last_raw_tx_block']

    dict_values = {
        "operations": operations,
        "count": len(operations),
        "total": operations_count,
        "last_block_indexed": last_block_indexed
    }

    return dict_values


@router.get(
    "/v1/operations/oper_id/",
    tags=["operations"],
    response_description="Status operations given oper id",
    response_model=Operations
)
async def operations_oper_id(
        oper_id: Annotated[int, Query(
            title="Operation ID",
            description="Operation ID")] = 13,
        bucket_index: Annotated[int, Query(
            title="Bucket Index",
            description="Bucket Index")] = 0
):

    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {
        "operId_": oper_id,
        "bucket_index": bucket_index
    }

    operations = await db["operations"]\
        .find_one(query_filter)

    if not operations:
        raise HTTPException(status_code=404, detail="Operation id not found")

    operations['_id'] = str(operations['_id'])

    fields_date_to_str(operations, DATE_FIELDS)

    # Last block indexed
    indexer = await db["moc_indexer"] \
        .find_one(sort=[("updatedAt", -1)])

    last_block_indexed = 0
    if indexer:
        if 'last_raw_tx_block' in indexer:
            last_block_indexed = indexer['last_raw_tx_block']

    operations['last_block_indexed'] = last_block_indexed

    return operations

@router.get(
    "/v1/operations/queued_opers/",
    tags=["operations"],
    response_description="Accumulated value for queued operations",
    response_model=OperationsSummaryResponse
)
async def queued_opers():
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {
        "status": 0,
        "operation": {"$in": ["TPMint", "TPRedeem", "TCandTPMint", "TCandTPRedeem", "TCSwapForTP", "TPSwapForTC", "TPSwapForTP"]}
    }

    try:
        cursor = db["operations"].find(query_filter)

        result = {
            "TPMint": [],
            "TPRedeem": [],
            "TCandTPMint": [],
            "TCandTPRedeem": [],
            "TCSwapForTP": [],
            "TPSwapForTC": [],
            "TPSwapForTP": []
        }

        async for operation in cursor:
            operation_type = operation["operation"]
            qtp_value = int(operation["params"].get("qTP", 0) or 0)
            qtc_value = int(operation["params"].get("qTC", 0) or 0)
            tp_index = int(operation["params"].get("tpIndex", 0) or 0)

            if operation_type in result:
                found = False
                for summary in result[operation_type]:
                    if summary.tpIndex == tp_index:
                        summary.qTP += qtp_value
                        summary.qTC += qtc_value
                        found = True
                        break
                if not found:
                    result[operation_type].append(OperationSummary(qTP=qtp_value, qTC=qtc_value, tpIndex=tp_index))

        return {"result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))