import pandas as pd
from pprint import pprint
from pykrx import stock
import stock_finder
import api

# 코스피
kospi_list = pd.DataFrame({'종목코드':stock.get_market_ticker_list(market="KOSPI")})
kosdaq_list = pd.DataFrame({'종목코드':stock.get_market_ticker_list(market="KOSDAQ")})

stock_list = pd.concat([kospi_list, kosdaq_list])
stock_list['종목명'] = stock_list['종목코드'].map(lambda x: stock.get_market_ticker_name(x))
find_stock_list = stock_finder.일봉_신고거래량(stock_list)
pprint(find_stock_list)

stock.get_market_ohlcv()
# 일봉 신고거래량 검색된 종목 저가 매수
batting_price = 200000 # 20만 (임시로 설정)

api.account.buy()
