import unittest
from datetime import datetime
from pprint import pprint
from peewee import SqliteDatabase

import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from data.order_model import OrderModel
from data.order_repository import OrderDto, order_repository


class OrderRepositoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        # 테스트 용도로 메모리 db 사용
        self.test_db = SqliteDatabase(":memory:")

        self.test_db.bind([OrderModel])
        self.test_db.connect()
        self.test_db.create_tables([OrderModel])

    @classmethod
    def tearDownClass(self) -> None:
        self.test_db.drop_tables([OrderModel])
        self.test_db.close()

    def test_insert_order(self):
        order = OrderDto(
            주문번호="0",
            종류="매수",
            주문수량=2,
            주문가격=2000,
            주문일=datetime.now(),
            종목코드="456",
            종목명="네이버",
        )
        order_repository.insert_order(order)
        orders = order_repository.get_orders()
        self.assertGreater(len(orders), 0)
        pprint(orders)

    def test_insert_orders(self):
        orders = [
            OrderDto(
                주문번호="1",
                종류="매수",
                주문수량=1,
                주문가격=1000,
                주문일=datetime.now(),
                종목코드="123",
                종목명="카카오",
            ),
            OrderDto(
                주문번호="2",
                종류="매수",
                주문수량=2,
                주문가격=2000,
                주문일=datetime.now(),
                종목코드="456",
                종목명="네이버",
            ),
        ]
        order_repository.insert_orders(orders)
        orders = order_repository.get_orders()
        self.assertGreater(len(orders), 1)
        pprint(orders)

    def test_get_orders(self):
        order = OrderDto(
            주문번호="3",
            종류="매수",
            주문수량=2,
            주문가격=2000,
            주문일=datetime.now(),
            종목코드="456",
            종목명="네이버",
        )
        order_repository.insert_order(order)
        orders = order_repository.get_orders()
        self.assertGreater(len(orders), 0)
        self.assertEqual(orders[0].종목명, "네이버")

        # TODO: get_orders(filter_fn=filter) 필터 함수 추가해서 테스트


if __name__ == "__main__":
    unittest.main()
