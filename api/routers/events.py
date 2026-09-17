from fastapi import APIRouter, Query, HTTPException
from typing import Annotated

from api.db import get_db
from api.models.events import EventMocSettlementExecutedList, EventMocSuccessFeeDistributedList, \
                              EventMocTCInterestPaymentList, EventMocTPemaUpdatedList, \
                              EventMocQueueOperationErrorList, EventMocQueueOperationExecutedList, \
                              EventMocQueueOperationQueuedList, DATE_FIELDS
from api.utils import fields_date_to_str


router = APIRouter()


@router.get(
    "/v1/events/moc_settlement_executed/",
    tags=["events"],
    response_description="Events MoC Settlement executed",
    response_model=EventMocSettlementExecutedList
)
async def event_moc_settlement_executed(
        limit: Annotated[int, Query(
            title="Limit",
            description="Limit",
            le=10000)] = 2000,
        skip: Annotated[int, Query(
            title="Skip",
            description="Skip",
            le=10000)] = 0
):
    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {}

    rows = await db["event_Moc_SettlementExecuted"] \
        .find(query_filter) \
        .skip(skip) \
        .limit(limit) \
        .to_list(limit)

    rows_count = await db["event_Moc_SettlementExecuted"].estimated_document_count()

    for trx in rows:
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
        "rows": rows,
        "count": len(rows),
        "total": rows_count,
        "last_block_indexed": last_block_indexed
    }

    return dict_values


@router.get(
    "/v1/events/moc_success_fee_distributed/",
    tags=["events"],
    response_description="Events Moc Success Fee Distributed",
    response_model=EventMocSuccessFeeDistributedList
)
async def moc_success_fee_distributed(
        limit: Annotated[int, Query(
            title="Limit",
            description="Limit",
            le=10000)] = 2000,
        skip: Annotated[int, Query(
            title="Skip",
            description="Skip",
            le=10000)] = 0
):
    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {}

    rows = await db["event_Moc_SuccessFeeDistributed"] \
        .find(query_filter) \
        .skip(skip) \
        .limit(limit) \
        .to_list(limit)

    rows_count = await db["event_Moc_SuccessFeeDistributed"].estimated_document_count()

    for trx in rows:
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
        "rows": rows,
        "count": len(rows),
        "total": rows_count,
        "last_block_indexed": last_block_indexed
    }

    return dict_values


@router.get(
    "/v1/events/moc_tc_interest_payment/",
    tags=["events"],
    response_description="Events TC Interest Payment",
    response_model=EventMocTCInterestPaymentList
)
async def moc_tc_interest_payment(
        limit: Annotated[int, Query(
            title="Limit",
            description="Limit",
            le=10000)] = 2000,
        skip: Annotated[int, Query(
            title="Skip",
            description="Skip",
            le=10000)] = 0
):
    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {}

    rows = await db["event_Moc_TCInterestPayment"] \
        .find(query_filter) \
        .skip(skip) \
        .limit(limit) \
        .to_list(limit)

    rows_count = await db["event_Moc_TCInterestPayment"].estimated_document_count()

    for trx in rows:
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
        "rows": rows,
        "count": len(rows),
        "total": rows_count,
        "last_block_indexed": last_block_indexed
    }

    return dict_values


@router.get(
    "/v1/events/moc_tp_ema_updated/",
    tags=["events"],
    response_description="Event Moc_TPemaUpdated",
    response_model=EventMocTPemaUpdatedList
)
async def moc_tp_ema_updated(
        limit: Annotated[int, Query(
            title="Limit",
            description="Limit",
            le=10000)] = 2000,
        skip: Annotated[int, Query(
            title="Skip",
            description="Skip",
            le=10000)] = 0
):
    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {}

    rows = await db["event_Moc_TPemaUpdated"] \
        .find(query_filter) \
        .skip(skip) \
        .limit(limit) \
        .to_list(limit)

    rows_count = await db["event_Moc_TPemaUpdated"].estimated_document_count()

    for trx in rows:
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
        "rows": rows,
        "count": len(rows),
        "total": rows_count,
        "last_block_indexed": last_block_indexed
    }

    return dict_values


@router.get(
    "/v1/events/moc_queue_operation_error/",
    tags=["events"],
    response_description="events MocQueue OperationError",
    response_model=EventMocQueueOperationErrorList
)
async def moc_queue_operation_error(
        limit: Annotated[int, Query(
            title="Limit",
            description="Limit",
            le=10000)] = 2000,
        skip: Annotated[int, Query(
            title="Skip",
            description="Skip",
            le=10000)] = 0
):
    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {}

    rows = await db["event_MocQueue_OperationError"] \
        .find(query_filter) \
        .skip(skip) \
        .limit(limit) \
        .to_list(limit)

    rows_count = await db["event_MocQueue_OperationError"].estimated_document_count()

    for trx in rows:
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
        "rows": rows,
        "count": len(rows),
        "total": rows_count,
        "last_block_indexed": last_block_indexed
    }

    return dict_values


@router.get(
    "/v1/events/moc_queue_operation_executed/",
    tags=["events"],
    response_description="events MocQueue_OperationExecuted",
    response_model=EventMocQueueOperationExecutedList
)
async def moc_queue_operation_executed(
        limit: Annotated[int, Query(
            title="Limit",
            description="Limit",
            le=10000)] = 2000,
        skip: Annotated[int, Query(
            title="Skip",
            description="Skip",
            le=10000)] = 0
):
    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {}

    rows = await db["event_MocQueue_OperationExecuted"] \
        .find(query_filter) \
        .skip(skip) \
        .limit(limit) \
        .to_list(limit)

    rows_count = await db["event_MocQueue_OperationExecuted"].estimated_document_count()

    for trx in rows:
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
        "rows": rows,
        "count": len(rows),
        "total": rows_count,
        "last_block_indexed": last_block_indexed
    }

    return dict_values


@router.get(
    "/v1/events/moc_queue_operation_queued/",
    tags=["events"],
    response_description="events MocQueue OperationQueued",
    response_model=EventMocQueueOperationQueuedList
)
async def moc_queue_operation_queued(
        limit: Annotated[int, Query(
            title="Limit",
            description="Limit",
            le=10000)] = 2000,
        skip: Annotated[int, Query(
            title="Skip",
            description="Skip",
            le=10000)] = 0
):
    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {}

    rows = await db["event_MocQueue_OperationQueued"] \
        .find(query_filter) \
        .skip(skip) \
        .limit(limit) \
        .to_list(limit)

    rows_count = await db["event_MocQueue_OperationQueued"].estimated_document_count()

    for trx in rows:
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
        "rows": rows,
        "count": len(rows),
        "total": rows_count,
        "last_block_indexed": last_block_indexed
    }

    return dict_values
