from enum import StrEnum
from peewee import AutoField, CharField, DateField, IntegerField

from data.base_model import BaseModel


class OrderType(StrEnum):
    매수 = "매수"
    매도 = "매도"


class OrderStatus(StrEnum):
    매수대기 = "매수대기"
    매수주문중 = "매수주문중"
    매수체결완료 = "매수체결완료"
    매도대기 = "매도대기"
    매도주문중 = "매도주문중"
    매도체결완료 = "매도체결완료"


class OrderResult(StrEnum):
    대기 = "대기"
    익절 = "익절"
    손절 = "손절"
    매매기간만료 = "매매기간만료"


# 주문 정보 DB 스키마
class OrderModel(BaseModel):
    id = AutoField()
    주문번호 = CharField(unique=True)
    종류 = CharField(default=OrderType.매수)
    종목명 = CharField()
    종목코드 = CharField()
    주문수량 = IntegerField()
    주문가격 = IntegerField()
    주문일 = DateField()
    체결수량 = IntegerField(null=True)
    체결가격 = IntegerField(null=True)
    체결일 = DateField(null=True)
    상태 = CharField(default=OrderStatus.매수대기)
    결과 = CharField(default=OrderResult.대기)
