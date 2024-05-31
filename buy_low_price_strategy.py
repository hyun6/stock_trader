# 일봉 저가매수 전략
from datetime import datetime, timedelta
import pandas as pd
from pykrx import stock
import stock_finder
from data.order_repository import OrderStatus, order_repository
import time
from pprint import pprint
import api


TIME_FRAME = "10m"


# 코스피, 코스닥에서 일봉 신고거래량 검색
def find_stock() -> pd.DataFrame:
    kospi_stock_codes = pd.DataFrame(
        {"종목코드": stock.get_market_ticker_list(market="KOSPI")}
    )
    kosdaq_stock_codes = pd.DataFrame(
        {"종목코드": stock.get_market_ticker_list(market="KOSDAQ")}
    )

    kospi_kosdaq_stock_list = pd.concat([kospi_stock_codes, kosdaq_stock_codes])
    kospi_kosdaq_stock_list["종목명"] = kospi_kosdaq_stock_list["종목코드"].map(
        lambda x: stock.get_market_ticker_name(x)
    )
    find_stock_list = stock_finder.일봉_신고거래량(kospi_kosdaq_stock_list)
    pprint(find_stock_list)

    # 일봉 신고거래량 검색된 종목 저가 매수 리스트 저장
    buy_stock_list = find_stock_list[
        ["종목코드", "종목명", "시가", "고가", "저가", "종가"]
    ]
    buy_stock_list = buy_stock_list.reset_index(drop=True)

    buy_stock_list["매수목표가"] = buy_stock_list["저가"] * 1.01
    buy_stock_list["매도목표가"] = buy_stock_list["매수목표가"] * 1.1
    buy_stock_list["매매시작일"] = time.strftime("%Y%m%d")
    buy_stock_list["매매만료일"] = (
        pd.Timestamp.now() + pd.Timedelta(days=14)
    ).strftime("%Y%m%d")
    buy_stock_list["매매전략명"] = "일봉저가매수"
    pprint(buy_stock_list)

    # 주문DB에 새로운 매수 주문 추가
    order_repository.insert_orders(buy_stock_list)
    return buy_stock_list


def buy():
    buy_stock_list = order_repository.get_orders()
    # 매수 대기 중인 종목만 추출
    buy_stock_list = buy_stock_list[buy_stock_list["상태"] == OrderStatus.매수대기]

    # 호가 단위에 맞춰 매수 가격 보정
    # 1만~2만 원 미만: 10원
    # 10만~20만 원 미만: 100원
    # 20만~50만 원: 500원
    # 50만 원 이상: 1,000원
    def calc_by_bid_price(price: int) -> int:
        bid_price = 10
        if price < 200000:
            bid_price = 100
        elif price < 500000:
            bid_price = 500
        else:
            bid_price = 1000
        return price // bid_price * bid_price

    batting_price = 200000  # 20만 (임시로 설정)
    stock_code_order_number_dict = {}  # {종목코드: 주문번호}
    # 매수 요청
    for _, stock_item in buy_stock_list.iterrows():
        buy_price = calc_by_bid_price(int(stock_item["매수목표가"]))
        if batting_price < buy_price:
            quantity = 1
        else:
            quantity = abs(int(batting_price / buy_price))
            try:
                code = stock_item["종목코드"]
                order = api.account.buy(code=code, unpr=buy_price, qty=quantity)

                # 매수DB: 매수 중 상태로 갱신
                order_repository.update_buying_status(
                    code=code, order_number=order.odno
                )
            except Exception as e:
                pprint(e)
                time.sleep(0.5)
                continue
            stock_code_order_number_dict[stock_item["종목코드"]] = order.odno
            time.sleep(0.5)


# 체결된 종목을 조회해서 매수 DB에서 제거
def update_buy_list():
    buy_stock_list = order_repository.get_orders()
    # 체결된 주문 조회
    now = datetime.now()
    buy_complete_orders = api.account.daily_order_all(
        now - timedelta(days=1), now, ccld="체결"
    )

    # TODO: 체결된 주문 정보 갱신
    #  - 주문 상태 '매수완료'
    #  - 매수 체결 가격 갱신
    # ...
    for order in buy_complete_orders.orders:
        complete_order = buy_stock_list.loc[buy_stock_list["주문번호"] == order.odno]
        complete_order["주문상태"] = "매수완료"
        complete_order["매수가격"] = order.ord_unpr
