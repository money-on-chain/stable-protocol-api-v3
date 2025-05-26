import datetime
from typing import Dict
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid

DATE_FIELDS = [
    'params.createdAt',
    'params.lastUpdatedAt',
    'executed.createdAt',
    'executed.lastUpdatedAt',
    'createdAt',
    'lastUpdatedAt',
    'confirmationTime'
]


class Params(BaseModel):
    tp: Optional[str] = None
    tpIndex: Optional[int] = None
    token: Optional[str] = None
    amount: Optional[str] = None
    qTP: Optional[str] = None
    qTC: Optional[str] = None
    qACmax: Optional[str] = None
    qACmin: Optional[str] = None
    qTPmin: Optional[str] = None
    qTCmin: Optional[str] = None
    tpFrom: Optional[str] = None
    tpFromIndex: Optional[int] = None
    tpTo: Optional[str] = None
    tpToIndex: Optional[int] = None
    sender: Optional[str] = None
    recipient: Optional[str] = None
    vendor: Optional[str] = None
    hash: Optional[str]
    blockNumber: Optional[int] = None
    createdAt: Optional[datetime.datetime] = None
    lastUpdatedAt: Optional[datetime.datetime] = None


class Executed(BaseModel):
    tp_: Optional[str] = None
    tpIndex_: Optional[int] = None
    tpFrom_: Optional[str] = None
    tpFromIndex_: Optional[int] = None
    tpTo_: Optional[str] = None
    tpToIndex_: Optional[int] = None
    qTPfrom_: Optional[str] = None
    qTPto_: Optional[str] = None
    tp: Optional[str] = None
    qTP_: Optional[str] = None
    qTC_: Optional[str] = None
    qAC_: Optional[str] = None
    qACfee_: Optional[str] = None
    qFeeToken_: Optional[str] = None
    qACVendorMarkup_: Optional[str] = None
    qFeeTokenVendorMarkup_: Optional[str] = None
    vendor_: Optional[str] = None
    operId_: Optional[int] = None
    sender_: Optional[str] = None
    recipient_: Optional[str] = None
    hash: Optional[str]
    blockNumber: Optional[int] = None
    createdAt: Optional[datetime.datetime] = None
    lastUpdatedAt: Optional[datetime.datetime] = None


class Operations(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    hash: Optional[str]
    blockNumber: Optional[int] = None
    operId_: Optional[int] = None
    bucket_index: Optional[int] = None
    gas: Optional[int] = None
    gasPrice: Optional[str] = None
    gasUsed: Optional[int] = None
    gasFeeRBTC: Optional[str] = None
    status: Optional[int] = None
    errorCode_: Optional[str] = None
    msg_: Optional[str] = None
    reason_: Optional[str] = None
    operation: Optional[str] = None
    createdAt: Optional[datetime.datetime] = None
    lastUpdatedAt: Optional[datetime.datetime] = None
    confirmationTime: Optional[datetime.datetime] = None
    params: Optional[Params] = None
    executed: Optional[Executed] = None
    last_block_indexed: Optional[int] = None

    class Config:
        #allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "_id": "658dac848e6961287ceb62e5",
                "hash": "0xaddc1a3b49fcd5528a4a394d98e095c1f89475e1e30b9a237e93231c15e4a265",
                "blockNumber": 4643915,
                "operId_": 13,
                "bucket_index": 0,
                "gas": 4500000,
                "gasPrice": "66458000",
                "gasUsed": 117984,
                "gasFeeRBTC": "7840980672000",
                "status": 1,
                "errorCode_": None,
                "msg_": None,
                "reason_": None,
                "operation": "TPRedeem",
                "createdAt": None,
                "lastUpdatedAt": "2023-12-28T14:15:01.629000Z",
                "confirmationTime": "2023-12-28T14:20:05.481000Z",
                "params": {
                    "tp": "0x0AE66294941fdA20c336cfC57EEAF5C2c35cecB4",
                    "token": None,
                    "amount": None,
                    "qTP": "5000000000000000000",
                    "qTC": None,
                    "qACmax": None,
                    "qACmin": "5142292984339019",
                    "qTPmin": None,
                    "qTCmin": None,
                    "tpFrom": None,
                    "tpTo": None,
                    "sender": "0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3",
                    "recipient": "0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3",
                    "vendor": "0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3",
                    "hash": "0xdca55acfd2673032ae215affe4d14b7a924ec920cab0d5f09c33c15bf62252f8",
                    "blockNumber": 4643908,
                    "createdAt": "2023-12-28T17:11:54Z",
                    "lastUpdatedAt": "2023-12-28T14:12:36.867000Z"
                },
                "executed": {
                    "tp_": "0x0AE66294941fdA20c336cfC57EEAF5C2c35cecB4",
                    "tpFrom_": None,
                    "tpTo_": None,
                    "qTPfrom_": None,
                    "qTPto_": None,
                    "tp": None,
                    "qTP_": "5000000000000000000",
                    "qTC_": None,
                    "qAC_": "5152598180700420",
                    "qACfee_": "52099071594544",
                    "qFeeToken_": "0",
                    "qACVendorMarkup_": "5209907159454",
                    "qFeeTokenVendorMarkup_": "0",
                    "vendor_": "0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3",
                    "operId_": 13,
                    "sender_": "0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3",
                    "recipient_": "0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3",
                    "hash": "0xaddc1a3b49fcd5528a4a394d98e095c1f89475e1e30b9a237e93231c15e4a265",
                    "blockNumber": 4643915,
                    "createdAt": "2023-12-28T17:13:57Z",
                    "lastUpdatedAt": "2023-12-28T14:15:01.603000Z"
                },
                "last_block_indexed": None
            }
        }


class OperationsList(BaseModel):
    operations: List[Operations]
    count: int = 0
    total: int = 0
    last_block_indexed: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "operations": "[]",
                "count": "0",
                "total": "0",
                "last_block_indexed": "12345678"
            }
        }

class OperationSummary(BaseModel):
    qTP: int = 0
    qTC: int = 0
    tpIndex: int = 0

class OperationsSummaryResponse(BaseModel):
    result: Dict[str, List[OperationSummary]]