from datetime import timezone
from fastapi import APIRouter, Path, HTTPException
from typing import Annotated, List

from api.db import get_incentives_db, CASE_INSENSITIVE_COLLATION
from api.models.incentives import IncentivesBalance, IncentiveClaim, \
    IncentivesAgent

from .common import make_responses


# Port of MoC_Incentive's miniwebservice (moc-incentives.moneyonchain.com),
# keeping its response formats, which the dapps parse as they are.

tags_metadata = [{
    "name": "Incentives",
    "description": "MoC v1 Liquidity Mining rewards: MoC balances accrued by "
                   "BPro holders and their claims, paid out by an off-chain "
                   "agent (MoC_Incentive)"}]

router = APIRouter(tags=["Incentives"])

AddressPath = Annotated[str, Path(
    title="Address",
    description="Account address",
    pattern='^0x[a-fA-F0-9]{40}$')]


async def require_incentives_db():
    db = await get_incentives_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Cannot get DB access")
    return db


def _unix(x):
    """Mongo dates are naive UTC."""
    if x is None:
        return None
    return int(x.replace(tzinfo=timezone.utc).timestamp())


def _str(x):
    return None if x is None else str(x)


@router.get(
    "/v1/incentives/balance/{address}",
    response_description="Returns the MoC rewards balance of an address",
    response_model=IncentivesBalance,
    response_model_exclude_unset=True,
    responses=make_responses(503),
)
async def incentives_balance(address: AddressPath):
    """Returns the MoC rewards balance of the given address, and the current
    reward period (daily MoCs, total BPro and its end) to estimate the
    rewards of the day. An empty object when the address has no balance."""
    db = await require_incentives_db()
    balance = await db["mocin_balances"].find_one(
        # Assumes a unique record for each address
        {"account_address": address},
        {"account_address": 1, "balance_moc": 1, "_id": 0},
        collation=CASE_INSENSITIVE_COLLATION)
    if not balance:
        return {}

    result = {
        "moc_balance": _str(balance.get("balance_moc")),
        "account_address": balance.get("account_address"),
    }
    period = await db["mocin_rewards_extscaninfo"].find_one(
        {}, sort=[("end_block", -1)])
    if period:
        result.update(
            daily_moc=_str(period.get("daily_moc")),
            total_bpro=_str(period.get("total_bpro")),
            end_block_dt=_str(period.get("end_block_dt")))
    return result


@router.get(
    "/v1/incentives/claims/{address}",
    response_description="Returns the reward claims of an address",
    response_model=List[IncentiveClaim],
    response_model_exclude_unset=True,
    responses=make_responses(503),
)
async def incentives_claims(address: AddressPath):
    """Returns every reward claim of the given address, oldest first (by
    block number and index in the block)."""
    db = await require_incentives_db()
    rows = await db["mocin_agent_tx"].find(
        {"address": address},
        {"hash": 1, "createdAt": 1, "stateTS": 1, "value": 1, "state": 1,
         "result": 1, "mocs": 1, "sentHash": 1, "_id": 0},
        collation=CASE_INSENSITIVE_COLLATION,
    ).sort([("blocknr", 1), ("blockidx", 1)]).to_list(None)

    claims = []
    for row in rows:
        claim = {
            "hash": row.get("hash"),
            "value": _str(row.get("value")),
            "state": row.get("state"),
            "result": row.get("result"),
            "sent_hash": row.get("sentHash"),
            "creation": _unix(row.get("createdAt")),
            "modification": _unix(row.get("stateTS")),
        }
        # MoCs sent: only for a successful claim
        if "mocs" in row and row.get("result") == "ok":
            claim["mocs"] = _str(row["mocs"])
        claims.append(claim)
    return claims


@router.get(
    "/v1/incentives/agent/",
    response_description="Returns the agent that pays out the claims",
    response_model=IncentivesAgent,
    response_model_exclude_unset=True,
    responses=make_responses(503),
)
async def incentives_agent():
    """Returns the address of the agent that pays out the claims, and the
    gas cost it charges per claim. An empty object when unknown."""
    db = await require_incentives_db()
    agent = await db["mocin_agent_state"].find_one(
        {}, {"agent_address": 1, "fee": 1, "_id": 0},
        sort=[("last_block_confirmed", -1)])
    if not agent:
        return {}
    return {"agent_address": agent.get("agent_address"),
            "gas_cost": _str(agent.get("fee"))}
