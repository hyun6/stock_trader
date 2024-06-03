from datetime import datetime
from typing import Callable, Self
from attrs import asdict, frozen
from data.order_model import OrderModel, OrderStatus, OrderType
from util.singleton import SingletonInstance


@frozen
class OrderDto:
    주문번호: str
    종류: OrderType
    종목명: str
    종목코드: str
    주문수량: int
    주문가격: int
    주문일: datetime

    # # TODO: DTO를 DB 모델 (dict로?) 변환
    # @classmethod
    # def to_model(self) -> OrderModel:
    #     return OrderModel(
    #         주문번호=self.order_no,
    #         종류=self.종류,
    #         종목명=self.종목명,
    #         종목코드=self.종목코드,
    #         주문수량= self.주문수량,
    #         주문가격= self.주문가격,
    #         주문일= self.주문일
    #     )

    @classmethod
    def from_dict(self, d: dict[OrderModel]) -> Self:
        return OrderDto(
            주문번호=d.get("주문번호"),
            종류=d.get("종류"),
            종목명=d.get("종목명"),
            종목코드=d.get("종목코드"),
            주문수량=d.get("주문수량"),
            주문가격=d.get("주문가격"),
            주문일=d.get("주문일"),
        )


# 주식 매매 주문을 위한 데이터를 저장하고 체결된 주문 정보를 DB로 관리
class OrderRepository(SingletonInstance):
    def __init__(self):
        OrderModel.create_table()

    def insert_order(self, order: OrderDto):
        print(order)
        OrderModel.insert(asdict(order)).execute()

    # 복수의 주문을 한번에 기록
    def insert_orders(self, orders: list[OrderDto]) -> None:
        print(orders)
        orders_record = list(map(asdict, orders))

        OrderModel.insert_many(orders_record).execute()

    # DB에서 검색 결과를 조회
    # 이 종목들로 오전에 주식장이 시작할 때 매수 주문
    def get_orders(self, filter_fn: Callable = None) -> list[OrderDto]:
        query = OrderModel.select().where(filter_fn)
        # TODO: list로 변환하지 않고 iterator 그대로 리턴하는게 필요한지 검토 필요
        # 주문 개수가 많아지면 성능상 필요할 수 있어 보임, 사용하는 측에서 마지막 몇 개만 take하는 방식으로 최적화 가능
        return list(map(OrderDto.from_dict, query.dicts()))

    # 매수 주문 중 상태로 갱신
    #  - 체결된 종목은 제거하기 위해 사용함
    def update_buying_status(self, code: str, order_number: str) -> None:
        OrderModel.update(주문번호=order_number, 상태=OrderStatus.매수주문중).where(
            OrderModel.종목코드 == code
        ).execute()

    # 매수 완료 상태로 갱신
    def update_buy_complete_status(self, code: str) -> None:
        OrderModel.delete().where(OrderModel.종목코드 == code).execute()

    def clear_buy_status(self) -> None:
        OrderModel.update(주문번호=None).execute()
        OrderModel.update(상태=OrderStatus.매수대기).execute()


order_repository = OrderRepository.instance()
