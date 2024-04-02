import pandas as pd
from pprint import pprint
from pykrx import stock
import stock_finder
import api
from buy_db import buyListDB
import time

# 코스피
kospi_list = pd.DataFrame({'종목코드':stock.get_market_ticker_list(market="KOSPI")})
kosdaq_list = pd.DataFrame({'종목코드':stock.get_market_ticker_list(market="KOSDAQ")})

stock_list = pd.concat([kospi_list, kosdaq_list])
stock_list['종목명'] = stock_list['종목코드'].map(lambda x: stock.get_market_ticker_name(x))
find_stock_list = stock_finder.일봉_신고거래량(stock_list)
pprint(find_stock_list)

# 일봉 신고거래량 검색된 종목 저가 매수 리스트 저장
buy_stock_list = find_stock_list[['종목코드', '종목명', '시가', '고가', '저가', '종가']]
buy_stock_list = buy_stock_list.reset_index(drop=True)
pprint(buy_stock_list)
buy_stock_list['매수가'] = (buy_stock_list['저가'] * 1.01)
buy_stock_list['매도가'] = (buy_stock_list['매수가'] * 1.1)
buy_stock_list['시작일'] = time.strftime('%Y%m%d')
buy_stock_list['만료일'] = (pd.Timestamp.now() + pd.Timedelta(days=14)).strftime('%Y%m%d')

# 매수 예정 목록 DB에 저장
buyListDB.insert_buy_list(buy_stock_list)

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

batting_price = 200000 # 20만 (임시로 설정)
order_list = []
# 매수 요청
for stock_item in buy_stock_list.iterrows():
    buy_price = calc_by_bid_price(int(stock_item['매수가']))
    quantity = abs(int(batting_price / buy_price))
    order = api.account.buy(code=stock_item['종목코드'], unpr=buy_price, qty=quantity)
    order_list.append(order)
    time.sleep(0.5)
