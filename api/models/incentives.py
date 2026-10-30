from pydantic import BaseModel
from typing import Any, Optional


class IncentivesBalance(BaseModel):
    account_address: Optional[str] = None
    # Amounts in wei, as strings
    moc_balance: Optional[str] = None
    daily_moc: Optional[str] = None
    total_bpro: Optional[str] = None
    # End of the last rewarded period (UTC, "YYYY-MM-DD HH:MM:SS")
    end_block_dt: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "account_address": "0xcd8a1c9acc980ae031456573e34dc05cd7dae6e3",
                "moc_balance": "1500000000000000000",
                "daily_moc": "2000000000000000000000",
                "total_bpro": "150000000000000000000",
                "end_block_dt": "2026-10-29 00:00:12"
            }
        }


class IncentiveClaim(BaseModel):
    hash: Optional[str] = None
    # Claimed amount in wei, as a string
    value: Optional[str] = None
    state: Optional[Any] = None
    result: Optional[Any] = None
    # MoCs sent, in wei: only when result is "ok"
    mocs: Optional[str] = None
    sent_hash: Optional[str] = None
    # Unix timestamps (seconds)
    creation: Optional[int] = None
    modification: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "hash": "0x9f2b...",
                "value": "1000000000000000",
                "state": "confirmed",
                "result": "ok",
                "mocs": "1500000000000000000",
                "sent_hash": "0x4a1c...",
                "creation": 1761700000,
                "modification": 1761700300
            }
        }


class IncentivesAgent(BaseModel):
    agent_address: Optional[str] = None
    # Gas cost of a claim, in wei, as a string
    gas_cost: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "agent_address": "0xcd8a1c9acc980ae031456573e34dc05cd7dae6e3",
                "gas_cost": "100000000000000"
            }
        }
