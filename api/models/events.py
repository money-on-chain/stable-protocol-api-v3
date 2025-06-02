import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid


DATE_FIELDS = [
    'createdAt',
    'lastUpdatedAt',
]

# Event MocMultiCollateralGuard MicroLiquidationExecuted

class EventMocMultiCollateralGuardMicroLiquidationExecuted(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    hash: Optional[str]
    blockNumber: Optional[int] = None
    createdAt: Optional[datetime.datetime] = None
    lastUpdatedAt: Optional[datetime.datetime] = None
    executor_: Optional[str] = None
    originBucket: Optional[str] = None
    targetBucket_: Optional[str] = None
    targetTP_: Optional[str] = None
    qACtoSwap_: Optional[str] = None
    qACOut_: Optional[str] = None
    qTPtoRebalance_: Optional[str] = None
    qACExecFee_: Optional[str] = None

    class Config:
        #allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "_id": "658dac848e6961287ceb62e5",
                "hash": "0xaddc1a3b49fcd5528a4a394d98e095c1f89475e1e30b9a237e93231c15e4a265",
                "blockNumber": 4643915,
                "createdAt": None,
                "lastUpdatedAt": "2023-12-28T14:15:01.629000Z",
                "executor_": "0x8D7c61aab2Db42739560682A4f949765Ce48feaA",
                "originBucket": "0x8D7c61aab2Db42739560682A4f949765Ce48feaA",
                "targetBucket_": "0x8D7c61aab2Db42739560682A4f949765Ce48feaA",
                "targetTP_": "0x8D7c61aab2Db42739560682A4f949765Ce48feaA",
                "qACtoSwap_": "5000000000000000000",
                "qACOut_": "5000000000000000000",
                "qTPtoRebalance_": "5000000000000000000",
                "qACExecFee_": "5000000000000000000",
            }
        }


class EventMocMultiCollateralGuardMicroLiquidationExecutedList(BaseModel):
    rows: List[EventMocMultiCollateralGuardMicroLiquidationExecuted]
    count: int = 0
    total: int = 0
    last_block_indexed: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "rows": "[]",
                "count": "0",
                "total": "0",
                "last_block_indexed": "12345678"
            }
        }


# Event MocMultiCollateralGuard PartialLiquidationExecuted

class EventMocMultiCollateralGuardPartialLiquidationExecuted(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    hash: Optional[str]
    blockNumber: Optional[int] = None
    createdAt: Optional[datetime.datetime] = None
    lastUpdatedAt: Optional[datetime.datetime] = None
    executor_: Optional[str] = None
    originBucket: Optional[str] = None
    targetBucket_: Optional[str] = None
    targetTP_: Optional[str] = None
    qACtoSwap_: Optional[str] = None
    qACOut_: Optional[str] = None
    qTPtoRebalance_: Optional[str] = None
    qACExecFee_: Optional[str] = None

    class Config:
        #allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "_id": "658dac848e6961287ceb62e5",
                "hash": "0xaddc1a3b49fcd5528a4a394d98e095c1f89475e1e30b9a237e93231c15e4a265",
                "blockNumber": 4643915,
                "createdAt": None,
                "lastUpdatedAt": "2023-12-28T14:15:01.629000Z",
                "executor_": "0x8D7c61aab2Db42739560682A4f949765Ce48feaA",
                "originBucket": "0x8D7c61aab2Db42739560682A4f949765Ce48feaA",
                "targetBucket_": "0x8D7c61aab2Db42739560682A4f949765Ce48feaA",
                "targetTP_": "0x8D7c61aab2Db42739560682A4f949765Ce48feaA",
                "qACtoSwap_": "5000000000000000000",
                "qACOut_": "5000000000000000000",
                "qTPtoRebalance_": "5000000000000000000",
                "qACExecFee_": "5000000000000000000",
            }
        }


class EventMocMultiCollateralGuardPartialLiquidationExecutedList(BaseModel):
    rows: List[EventMocMultiCollateralGuardPartialLiquidationExecuted]
    count: int = 0
    total: int = 0
    last_block_indexed: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "rows": "[]",
                "count": "0",
                "total": "0",
                "last_block_indexed": "12345678"
            }
        }


# Event MocMultiCollateralGuard BucketLiquidated

class EventMocMultiCollateralGuardBucketLiquidated(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    hash: Optional[str]
    blockNumber: Optional[int] = None
    createdAt: Optional[datetime.datetime] = None
    lastUpdatedAt: Optional[datetime.datetime] = None
    originBucket: Optional[str] = None

    class Config:
        #allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "_id": "658dac848e6961287ceb62e5",
                "hash": "0xaddc1a3b49fcd5528a4a394d98e095c1f89475e1e30b9a237e93231c15e4a265",
                "blockNumber": 4643915,
                "createdAt": None,
                "lastUpdatedAt": "2023-12-28T14:15:01.629000Z",
                "originBucket": "0x8D7c61aab2Db42739560682A4f949765Ce48feaA"
            }
        }


class EventMocMultiCollateralGuardBucketLiquidatedList(BaseModel):
    rows: List[EventMocMultiCollateralGuardBucketLiquidated]
    count: int = 0
    total: int = 0
    last_block_indexed: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "rows": "[]",
                "count": "0",
                "total": "0",
                "last_block_indexed": "12345678"
            }
        }


# Event MocMultiCollateralGuard BucketChange

class EventMocMultiCollateralGuardBucketChange(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    hash: Optional[str]
    blockNumber: Optional[int] = None
    createdAt: Optional[datetime.datetime] = None
    lastUpdatedAt: Optional[datetime.datetime] = None
    bucketIndex_: Optional[str] = None
    bucket_: Optional[str] = None
    bucketParams_: Optional[str] = None
    mocSwappers: Optional[str] = None

    class Config:
        #allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "_id": "658dac848e6961287ceb62e5",
                "hash": "0xaddc1a3b49fcd5528a4a394d98e095c1f89475e1e30b9a237e93231c15e4a265",
                "blockNumber": 4643915,
                "createdAt": None,
                "lastUpdatedAt": "2023-12-28T14:15:01.629000Z",
                "bucketIndex_": "0x8D7c61aab2Db42739560682A4f949765Ce48feaA",
                "bucket_": "0x8D7c61aab2Db42739560682A4f949765Ce48feaA",
                "bucketParams_": "0x8D7c61aab2Db42739560682A4f949765Ce48feaA",
                "mocSwappers": "0x8D7c61aab2Db42739560682A4f949765Ce48feaA",
            }
        }


class EventMocMultiCollateralGuardBucketChangeList(BaseModel):
    rows: List[EventMocMultiCollateralGuardBucketChange]
    count: int = 0
    total: int = 0
    last_block_indexed: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "rows": "[]",
                "count": "0",
                "total": "0",
                "last_block_indexed": "12345678"
            }
        }


# Settlement Executed

class EventMocSettlementExecuted(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    hash: Optional[str]
    blockNumber: Optional[int] = None
    createdAt: Optional[datetime.datetime] = None
    lastUpdatedAt: Optional[datetime.datetime] = None

    class Config:
        #allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "_id": "658dac848e6961287ceb62e5",
                "hash": "0xaddc1a3b49fcd5528a4a394d98e095c1f89475e1e30b9a237e93231c15e4a265",
                "blockNumber": 4643915,
                "createdAt": None,
                "lastUpdatedAt": "2023-12-28T14:15:01.629000Z"
            }
        }


class EventMocSettlementExecutedList(BaseModel):
    rows: List[EventMocSettlementExecuted]
    count: int = 0
    total: int = 0
    last_block_indexed: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "rows": "[]",
                "count": "0",
                "total": "0",
                "last_block_indexed": "12345678"
            }
        }


# SUCCESS FEE

class EventMocSuccessFeeDistributed(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    hash: Optional[str]
    blockNumber: Optional[int] = None
    createdAt: Optional[datetime.datetime] = None
    lastUpdatedAt: Optional[datetime.datetime] = None
    mocGain_: Optional[str] = None
    tpGain_: Optional[str] = None

    class Config:
        #allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "_id": "658dac848e6961287ceb62e5",
                "hash": "0xaddc1a3b49fcd5528a4a394d98e095c1f89475e1e30b9a237e93231c15e4a265",
                "blockNumber": 4643915,
                "createdAt": None,
                "lastUpdatedAt": "2023-12-28T14:15:01.629000Z",
                "mocGain_": "0",
                "tpGain_": "(0,)"
            }
        }


class EventMocSuccessFeeDistributedList(BaseModel):
    rows: List[EventMocSuccessFeeDistributed]
    count: int = 0
    total: int = 0
    last_block_indexed: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "rows": "[]",
                "count": "0",
                "total": "0",
                "last_block_indexed": "12345678"
            }
        }


# INTEREST PAYMENT

class EventMocTCInterestPayment(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    hash: Optional[str]
    blockNumber: Optional[int] = None
    createdAt: Optional[datetime.datetime] = None
    lastUpdatedAt: Optional[datetime.datetime] = None
    interestAmount_: Optional[str] = None

    class Config:
        #allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "_id": "658dac848e6961287ceb62e5",
                "hash": "0xaddc1a3b49fcd5528a4a394d98e095c1f89475e1e30b9a237e93231c15e4a265",
                "blockNumber": 4643915,
                "createdAt": None,
                "lastUpdatedAt": "2023-12-28T14:15:01.629000Z",
                "interestAmount_": "0"
            }
        }


class EventMocTCInterestPaymentList(BaseModel):
    rows: List[EventMocTCInterestPayment]
    count: int = 0
    total: int = 0
    last_block_indexed: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "rows": "[]",
                "count": "0",
                "total": "0",
                "last_block_indexed": "12345678"
            }
        }


# EMA UPDATED

class EventMocTPemaUpdated(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    hash: Optional[str]
    blockNumber: Optional[int] = None
    createdAt: Optional[datetime.datetime] = None
    lastUpdatedAt: Optional[datetime.datetime] = None
    i_: Optional[int] = None
    newTPema_: Optional[str] = None
    oldTPema_: Optional[str] = None

    class Config:
        #allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "_id": "658dac848e6961287ceb62e5",
                "hash": "0xaddc1a3b49fcd5528a4a394d98e095c1f89475e1e30b9a237e93231c15e4a265",
                "blockNumber": 4643915,
                "createdAt": None,
                "lastUpdatedAt": "2023-12-28T14:15:01.629000Z",
                "i_": "0",
                "newTPema_": "177577695063561323",
                "oldTPema_": "177504820146449227"
            }
        }


class EventMocTPemaUpdatedList(BaseModel):
    rows: List[EventMocTPemaUpdated]
    count: int = 0
    total: int = 0
    last_block_indexed: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "rows": "[]",
                "count": "0",
                "total": "0",
                "last_block_indexed": "12345678"
            }
        }


# OPERATION ERROR

class EventMocQueueOperationError(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    hash: Optional[str]
    blockNumber: Optional[int] = None
    createdAt: Optional[datetime.datetime] = None
    lastUpdatedAt: Optional[datetime.datetime] = None
    msg_: Optional[str] = None
    errorCode_: Optional[str] = None
    operId_: Optional[int] = None

    class Config:
        #allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "_id": "658dac848e6961287ceb62e5",
                "hash": "0xaddc1a3b49fcd5528a4a394d98e095c1f89475e1e30b9a237e93231c15e4a265",
                "blockNumber": 4643915,
                "createdAt": None,
                "lastUpdatedAt": "2023-12-28T14:15:01.629000Z",
                "msg_": "qAC below minimum required",
                "errorCode_": "0x54cde313",
                "operId_": 9
            }
        }


class EventMocQueueOperationErrorList(BaseModel):
    rows: List[EventMocQueueOperationError]
    count: int = 0
    total: int = 0
    last_block_indexed: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "rows": "[]",
                "count": "0",
                "total": "0",
                "last_block_indexed": "12345678"
            }
        }


# OPERATION EXECUTED


class EventMocQueueOperationExecuted(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    hash: Optional[str]
    blockNumber: Optional[int] = None
    createdAt: Optional[datetime.datetime] = None
    lastUpdatedAt: Optional[datetime.datetime] = None
    executor: Optional[str] = None
    operId_: Optional[int] = None

    class Config:
        #allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "_id": "658dac848e6961287ceb62e5",
                "hash": "0xaddc1a3b49fcd5528a4a394d98e095c1f89475e1e30b9a237e93231c15e4a265",
                "blockNumber": 4643915,
                "createdAt": None,
                "lastUpdatedAt": "2023-12-28T14:15:01.629000Z",
                "executor": "0x8D7c61aab2Db42739560682A4f949765Ce48feaA",
                "operId_": 9
            }
        }


class EventMocQueueOperationExecutedList(BaseModel):
    rows: List[EventMocQueueOperationExecuted]
    count: int = 0
    total: int = 0
    last_block_indexed: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "rows": "[]",
                "count": "0",
                "total": "0",
                "last_block_indexed": "12345678"
            }
        }


# OPERATION QUEUED

class EventMocQueueOperationQueued(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    hash: Optional[str]
    blockNumber: Optional[int] = None
    createdAt: Optional[datetime.datetime] = None
    lastUpdatedAt: Optional[datetime.datetime] = None
    bucket_: Optional[str] = None
    operId_: Optional[int] = None
    operType_: Optional[int] = None

    class Config:
        #allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "_id": "658dac848e6961287ceb62e5",
                "hash": "0xaddc1a3b49fcd5528a4a394d98e095c1f89475e1e30b9a237e93231c15e4a265",
                "blockNumber": 4643915,
                "createdAt": None,
                "lastUpdatedAt": "2023-12-28T14:15:01.629000Z",
                "bucket_": "0xA27024Ed70035E46dba712609fc2Afa1c97aA36A",
                "operId_": 0,
                "operType_": 1
            }
        }


class EventMocQueueOperationQueuedList(BaseModel):
    rows: List[EventMocQueueOperationQueued]
    count: int = 0
    total: int = 0
    last_block_indexed: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "rows": "[]",
                "count": "0",
                "total": "0",
                "last_block_indexed": "12345678"
            }
        }
