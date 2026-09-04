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
    VotingMachineVoteEventList, \
    VotingMachinePreVoteEventList, \
    VotingMachinePreVoteStepEventList, \
    VotingMachineVoteStepEventList, \
    VotingMachineAcceptedStepEventList, \
    VotingMachineUnregisterEventList, \
    OracleManagerOracleRegisteredList, \
    OracleManagerOracleStakeAddedList, \
    OracleManagerOracleSubscribedList, \
    OracleManagerOracleUnsubscribedList, \
    OracleManagerOracleRemovedList, \
    CoinPairPricePricePublishedList, \
    CoinPairPriceEmergencyPricePublishedList, \
    CoinPairPriceForcedPriceQueryModeSetList, \
    CoinPairPriceOracleRewardTransferList, \
    CoinPairPriceNewRoundList, \
    CoinPairPriceOracleAutoUnsubscribedList
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


@router.get(
    "/v1/omoc/voting_machine_pre_vote_event/",
    tags=["omoc"],
    response_description="Returns voting machine pre-vote events",
    response_model=VotingMachinePreVoteEventList
)
async def voting_machine_pre_vote_event(
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

    rows = await db["event_VotingMachine_PreVoteEvent"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_VotingMachine_PreVoteEvent"].count_documents(query_filter)

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
    "/v1/omoc/voting_machine_pre_vote_step_event/",
    tags=["omoc"],
    response_description="Returns voting machine pre-vote step events",
    response_model=VotingMachinePreVoteStepEventList
)
async def voting_machine_pre_vote_step_event(
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

    rows = await db["event_VotingMachine_PreVoteStepEvent"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_VotingMachine_PreVoteStepEvent"].count_documents(query_filter)

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
    "/v1/omoc/voting_machine_vote_step_event/",
    tags=["omoc"],
    response_description="Returns voting machine vote step events",
    response_model=VotingMachineVoteStepEventList
)
async def voting_machine_vote_step_event(
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

    rows = await db["event_VotingMachine_VoteStepEvent"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_VotingMachine_VoteStepEvent"].count_documents(query_filter)

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
    "/v1/omoc/voting_machine_accepted_step_event/",
    tags=["omoc"],
    response_description="Returns voting machine accepted step events",
    response_model=VotingMachineAcceptedStepEventList
)
async def voting_machine_accepted_step_event(
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

    rows = await db["event_VotingMachine_AcceptedStepEvent"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_VotingMachine_AcceptedStepEvent"].count_documents(query_filter)

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
    "/v1/omoc/voting_machine_unregister_event/",
    tags=["omoc"],
    response_description="Returns voting machine unregister events",
    response_model=VotingMachineUnregisterEventList
)
async def voting_machine_unregister_event(
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

    rows = await db["event_VotingMachine_UnregisterEvent"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_VotingMachine_UnregisterEvent"].count_documents(query_filter)

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
    "/v1/omoc/oracle_manager_oracle_registered/",
    tags=["omoc"],
    response_description="Returns oracle manager oracle registered events",
    response_model=OracleManagerOracleRegisteredList
)
async def oracle_manager_oracle_registered(
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

    rows = await db["event_OracleManager_OracleRegistered"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_OracleManager_OracleRegistered"].count_documents(query_filter)

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
    "/v1/omoc/oracle_manager_oracle_stake_added/",
    tags=["omoc"],
    response_description="Returns oracle manager oracle stake added events",
    response_model=OracleManagerOracleStakeAddedList
)
async def oracle_manager_oracle_stake_added(
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

    rows = await db["event_OracleManager_OracleStakeAdded"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_OracleManager_OracleStakeAdded"].count_documents(query_filter)

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
    "/v1/omoc/oracle_manager_oracle_subscribed/",
    tags=["omoc"],
    response_description="Returns oracle manager oracle subscribed events",
    response_model=OracleManagerOracleSubscribedList
)
async def oracle_manager_oracle_subscribed(
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

    rows = await db["event_OracleManager_OracleSubscribed"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_OracleManager_OracleSubscribed"].count_documents(query_filter)

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
    "/v1/omoc/oracle_manager_oracle_unsubscribed/",
    tags=["omoc"],
    response_description="Returns oracle manager oracle unsubscribed events",
    response_model=OracleManagerOracleUnsubscribedList
)
async def oracle_manager_oracle_unsubscribed(
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

    rows = await db["event_OracleManager_OracleUnsubscribed"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_OracleManager_OracleUnsubscribed"].count_documents(query_filter)

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
    "/v1/omoc/oracle_manager_oracle_removed/",
    tags=["omoc"],
    response_description="Returns oracle manager oracle removed events",
    response_model=OracleManagerOracleRemovedList
)
async def oracle_manager_oracle_removed(
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

    rows = await db["event_OracleManager_OracleRemoved"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_OracleManager_OracleRemoved"].count_documents(query_filter)

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
    "/v1/omoc/coin_pair_price_price_published/",
    tags=["omoc"],
    response_description="Returns CoinPairPrice price published events",
    response_model=CoinPairPricePricePublishedList
)
async def coin_pair_price_price_published(
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

    rows = await db["event_CoinPairPrice_PricePublished"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_CoinPairPrice_PricePublished"].count_documents(query_filter)

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
    "/v1/omoc/coin_pair_price_emergency_price_published/",
    tags=["omoc"],
    response_description="Returns CoinPairPrice emergency price published events",
    response_model=CoinPairPriceEmergencyPricePublishedList
)
async def coin_pair_price_emergency_price_published(
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

    rows = await db["event_CoinPairPrice_EmergencyPricePublished"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_CoinPairPrice_EmergencyPricePublished"].count_documents(query_filter)

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
    "/v1/omoc/coin_pair_price_forced_price_query_mode_set/",
    tags=["omoc"],
    response_description="Returns CoinPairPrice forced price query mode set events",
    response_model=CoinPairPriceForcedPriceQueryModeSetList
)
async def coin_pair_price_forced_price_query_mode_set(
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

    rows = await db["event_CoinPairPrice_ForcedPriceQueryModeSet"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_CoinPairPrice_ForcedPriceQueryModeSet"].count_documents(query_filter)

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
    "/v1/omoc/coin_pair_price_oracle_reward_transfer/",
    tags=["omoc"],
    response_description="Returns CoinPairPrice oracle reward transfer events",
    response_model=CoinPairPriceOracleRewardTransferList
)
async def coin_pair_price_oracle_reward_transfer(
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

    rows = await db["event_CoinPairPrice_OracleRewardTransfer"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_CoinPairPrice_OracleRewardTransfer"].count_documents(query_filter)

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
    "/v1/omoc/coin_pair_price_new_round/",
    tags=["omoc"],
    response_description="Returns CoinPairPrice new round events",
    response_model=CoinPairPriceNewRoundList
)
async def coin_pair_price_new_round(
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

    rows = await db["event_CoinPairPrice_NewRound"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_CoinPairPrice_NewRound"].count_documents(query_filter)

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
    "/v1/omoc/coin_pair_price_oracle_auto_unsubscribed/",
    tags=["omoc"],
    response_description="Returns CoinPairPrice oracle auto unsubscribed events",
    response_model=CoinPairPriceOracleAutoUnsubscribedList
)
async def coin_pair_price_oracle_auto_unsubscribed(
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

    rows = await db["event_CoinPairPrice_OracleAutoUnsubscribed"]\
        .find(query_filter)\
        .sort("createdAt", -1)\
        .skip(skip)\
        .limit(limit)\
        .to_list(limit)

    rows_count = await db["event_CoinPairPrice_OracleAutoUnsubscribed"].count_documents(query_filter)

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
