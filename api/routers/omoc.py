from fastapi import APIRouter, Query, HTTPException
from typing import Annotated
from pymongo.collation import Collation

from api.db import get_db

from api.models.omoc import DATE_FIELDS, \
    VestingCreatedList, \
    ClaimOKList, \
    DelayMachinePaymentCancelList, \
    DelayMachinePaymentDepositList, \
    DelayMachinePaymentWithdrawList, \
    SupportersAddStakeList, \
    SupportersCancelEarningsList, \
    SupportersPayEarningsList, \
    SupportersWithdrawList, \
    SupportersWithdrawStakeList, \
    VotingMachineVoteEventList
from api.utils import fields_date_to_str


collation = Collation(locale="en", strength=2)
router = APIRouter()


@router.get(
    "/v1/omoc/vesting_created/",
    tags=["omoc"],
    response_description="Returns vesting created from a holder address",
    response_model=VestingCreatedList
)
async def vesting_created(
        holder: Annotated[str, Query(
            title="Holder address",
            description="Holder Address",
            pattern='^0x[a-fA-F0-9]{40}$')] = '0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3',
        limit: Annotated[int, Query(
            title="Limit",
            description="Limit",
            le=100)] = 50,
        skip: Annotated[int, Query(
            title="Skip",
            description="Skip",
            le=1000)] = 0):

    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {
        "holder": holder.lower()
    }

    rows = await db["event_VestingFactory_VestingCreated"]\
        .find(query_filter, collation=collation)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_VestingFactory_VestingCreated"].count_documents(query_filter, collation=collation)

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
        "transactions": rows,
        "count": len(rows),
        "total": rows_count,
        "last_block_indexed": last_block_indexed
    }

    return dict_values


@router.get(
    "/v1/omoc/claim_ok/",
    tags=["omoc"],
    response_description="Returns Claim from a holder address",
    response_model=ClaimOKList
)
async def claim_ok(
        holder: Annotated[str, Query(
            title="Holder address",
            description="Holder Address",
            pattern='^0x[a-fA-F0-9]{40}$')] = '0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3',
        limit: Annotated[int, Query(
            title="Limit",
            description="Limit",
            le=100)] = 20,
        skip: Annotated[int, Query(
            title="Skip",
            description="Skip",
            le=1000)] = 0):

    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {
        "recipient": holder.lower()
    }

    rows = await db["event_IncentiveV2_ClaimOK"]\
        .find(query_filter, collation=collation)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_IncentiveV2_ClaimOK"].count_documents(query_filter, collation=collation)

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
        "results": rows,
        "count": len(rows),
        "total": rows_count,
        "last_block_indexed": last_block_indexed
    }

    return dict_values


@router.get(
    "/v1/omoc/delay_machine_payment_cancel/",
    tags=["omoc"],
    response_description="Returns Claim from a holder address",
    response_model=DelayMachinePaymentCancelList
)
async def delay_machine_payment_cancel(
        limit: Annotated[int, Query(
            title="Limit",
            description="Limit",
            le=100)] = 20,
        skip: Annotated[int, Query(
            title="Skip",
            description="Skip",
            le=1000)] = 0):

    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {}

    rows = await db["event_DelayMachine_PaymentCancel"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_DelayMachine_PaymentCancel"].count_documents(query_filter)

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
        "results": rows,
        "count": len(rows),
        "total": rows_count,
        "last_block_indexed": last_block_indexed
    }

    return dict_values


@router.get(
    "/v1/omoc/delay_machine_payment_deposit/",
    tags=["omoc"],
    response_description="Returns Claim from a holder address",
    response_model=DelayMachinePaymentDepositList
)
async def delay_machine_payment_deposit(
        limit: Annotated[int, Query(
            title="Limit",
            description="Limit",
            le=100)] = 20,
        skip: Annotated[int, Query(
            title="Skip",
            description="Skip",
            le=1000)] = 0):

    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {}

    rows = await db["event_DelayMachine_PaymentDeposit"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_DelayMachine_PaymentDeposit"].count_documents(query_filter)

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
        "results": rows,
        "count": len(rows),
        "total": rows_count,
        "last_block_indexed": last_block_indexed
    }

    return dict_values


@router.get(
    "/v1/omoc/delay_machine_payment_withdraw/",
    tags=["omoc"],
    response_description="Returns Claim from a holder address",
    response_model=DelayMachinePaymentWithdrawList
)
async def delay_machine_payment_withdraw(
        limit: Annotated[int, Query(
            title="Limit",
            description="Limit",
            le=100)] = 20,
        skip: Annotated[int, Query(
            title="Skip",
            description="Skip",
            le=1000)] = 0):

    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {}

    rows = await db["event_DelayMachine_PaymentWithdraw"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_DelayMachine_PaymentWithdraw"].count_documents(query_filter)

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
        "results": rows,
        "count": len(rows),
        "total": rows_count,
        "last_block_indexed": last_block_indexed
    }

    return dict_values


@router.get(
    "/v1/omoc/supporters_add_stake/",
    tags=["omoc"],
    response_description="Returns Claim from a holder address",
    response_model=SupportersAddStakeList
)
async def supporters_add_stake(
        limit: Annotated[int, Query(
            title="Limit",
            description="Limit",
            le=100)] = 20,
        skip: Annotated[int, Query(
            title="Skip",
            description="Skip",
            le=1000)] = 0):

    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {}

    rows = await db["event_Supporters_AddStake"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_Supporters_AddStake"].count_documents(query_filter)

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
        "results": rows,
        "count": len(rows),
        "total": rows_count,
        "last_block_indexed": last_block_indexed
    }

    return dict_values


@router.get(
    "/v1/omoc/supporters_cancel_earnings/",
    tags=["omoc"],
    response_description="Returns Claim from a holder address",
    response_model=SupportersCancelEarningsList
)
async def supporters_cancel_earnings(
        limit: Annotated[int, Query(
            title="Limit",
            description="Limit",
            le=100)] = 20,
        skip: Annotated[int, Query(
            title="Skip",
            description="Skip",
            le=1000)] = 0):

    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {}

    rows = await db["event_Supporters_CancelEarnings"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_Supporters_CancelEarnings"].count_documents(query_filter)

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
        "results": rows,
        "count": len(rows),
        "total": rows_count,
        "last_block_indexed": last_block_indexed
    }

    return dict_values


@router.get(
    "/v1/omoc/supporters_pay_earnings/",
    tags=["omoc"],
    response_description="Returns Claim from a holder address",
    response_model=SupportersPayEarningsList
)
async def supporters_pay_earnings(
        limit: Annotated[int, Query(
            title="Limit",
            description="Limit",
            le=100)] = 20,
        skip: Annotated[int, Query(
            title="Skip",
            description="Skip",
            le=1000)] = 0):

    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {}

    rows = await db["event_Supporters_PayEarnings"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_Supporters_PayEarnings"].count_documents(query_filter)

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
        "results": rows,
        "count": len(rows),
        "total": rows_count,
        "last_block_indexed": last_block_indexed
    }

    return dict_values


@router.get(
    "/v1/omoc/supporters_withdraw/",
    tags=["omoc"],
    response_description="Returns Claim from a holder address",
    response_model=SupportersWithdrawList
)
async def supporters_withdraw(
        limit: Annotated[int, Query(
            title="Limit",
            description="Limit",
            le=100)] = 20,
        skip: Annotated[int, Query(
            title="Skip",
            description="Skip",
            le=1000)] = 0):

    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {}

    rows = await db["event_Supporters_Withdraw"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_Supporters_Withdraw"].count_documents(query_filter)

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
        "results": rows,
        "count": len(rows),
        "total": rows_count,
        "last_block_indexed": last_block_indexed
    }

    return dict_values


@router.get(
    "/v1/omoc/supporters_withdraw_stake/",
    tags=["omoc"],
    response_description="Returns Claim from a holder address",
    response_model=SupportersWithdrawStakeList
)
async def supporters_withdraw_stake(
        limit: Annotated[int, Query(
            title="Limit",
            description="Limit",
            le=100)] = 20,
        skip: Annotated[int, Query(
            title="Skip",
            description="Skip",
            le=1000)] = 0):

    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {}

    rows = await db["event_Supporters_WithdrawStake"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_Supporters_WithdrawStake"].count_documents(query_filter)

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
        "results": rows,
        "count": len(rows),
        "total": rows_count,
        "last_block_indexed": last_block_indexed
    }

    return dict_values


@router.get(
    "/v1/omoc/voting_machine_vote_event/",
    tags=["omoc"],
    response_description="Returns Claim from a holder address",
    response_model=VotingMachineVoteEventList
)
async def voting_machine_vote_event(
        limit: Annotated[int, Query(
            title="Limit",
            description="Limit",
            le=100)] = 20,
        skip: Annotated[int, Query(
            title="Skip",
            description="Skip",
            le=1000)] = 0):

    # get mongo db connection
    db = await get_db()

    if db is None:
        raise HTTPException(status_code=400, detail="Cannot get DB")

    query_filter = {}

    rows = await db["event_VotingMachine_VoteEvent"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_VotingMachine_VoteEvent"].count_documents(query_filter)

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
        "results": rows,
        "count": len(rows),
        "total": rows_count,
        "last_block_indexed": last_block_indexed
    }

    return dict_values
