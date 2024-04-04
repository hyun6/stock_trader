from typing import Literal
import pandas as pd
from peewee import *
from enum import StrEnum
from util import SingletonInstance

class OrderStatus(StrEnum):
    대기 = '대기'
    매수중 = '매수중'
    매수완료 = '매수완료'
    매도중 = '매도중'
    매도완료 = '매도완료'

db = SqliteDatabase('order.db')

class BaseModel(Model):
    class Meta:
        database = db

# 테이블 컬럼
# 종목코드, 종목명, 시가, 저가, 종가, 고가, 매수가, 매도가, 시작일, 만료일
class Order(BaseModel):
    매매전략명 = CharField()
    상태 = CharField(default=OrderStatus.대기)
    주문번호 = CharField(unique=True, null=True)
    종목코드 = CharField()
    종목명 = CharField()
    매수목표가 = IntegerField()
    매수가 = IntegerField(null=True)
    매도목표가 = IntegerField()
    매도가 = IntegerField(null=True)
    매매시작일 = DateField()
    매매만료일 = DateField()
    시가 = IntegerField()
    저가 = IntegerField()
    종가 = IntegerField()
    고가 = IntegerField()

class BuyOrder(Order):
    pass

class SellOrder(Order):
    pass

class HistoryOrder(Order):
    pass

class OrderRepository(SingletonInstance):
    def __init__(self):
        db.connect()
        db.create_tables([BuyOrder, SellOrder, HistoryOrder])

    # 조건 검색 결과 종목들을 일정 기간동안 매수 시도하기 위해 db에 저장
    # 매일 주식장이 끝난 후 갱신
    def insert_buy_orders(self, df_orders: pd.DataFrame) -> None:
        print(df_orders)
        BuyOrder.insert_many(df_orders.to_dict(orient='records')).execute()

    # DB에서 검색 결과를 조회
    # 이 종목들로 오전에 주식장이 시작할 때 매수 주문
    def get_buy_orders(self) -> pd.DataFrame:
        query = BuyOrder.select()
        return pd.DataFrame(query.dicts())

    # 매수 주문 번호를 갱신한다
    #  - 체결된 종목은 제거하기 위해 사용함
    def update_buy_order_number(self, order_dict: dict) -> None:
        for code, order_number in order_dict.items():
            BuyOrder.update(주문번호=order_number).where(BuyOrder.종목코드 == code).execute()

    def delete_buy_order(self, order_dict: dict) -> None:
        for code, order_number in order_dict.items():
            BuyOrder.delete().where(BuyOrder.종목코드 == code).execute()

order_repository = OrderRepository()