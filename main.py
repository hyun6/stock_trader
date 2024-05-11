import buy_low_price_strategy
from order_repository import order_repository
import telegram

def 주식장_시작전():
    # 오늘 매수할 종목을 검색하고, 기존에 검색된 종목과 함께 매수 주문 요청
    buy_low_price_strategy.find_stock()
    # 어제자 매수 주문 정보 초기화
    order_repository.clear_buy_status()
    buy_low_price_strategy.buy()

def 주식장_장중():
    pass

def 주식장_마감후():
    # 오늘 체결된 종목은 DB에서 제거
    buy_low_price_strategy.update_buy_list()
    pass

주식장_시작전()
주식장_장중()
# 주식장_마감후()