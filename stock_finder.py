import pandas as pd
import numpy as np
from pykrx import stock
from datetime import datetime, timedelta

def 일봉_신고거래량(df_all_stocks) -> pd.DataFrame:
    # 모든 종목을 순회하며 조건에 부합하는 종목을 찾는다
    # 시가    고가    저가    종가      거래량       등락률
    find_stock_list = []
    for _, stock_item in df_all_stocks.iterrows():
        stock_code = stock_item.loc['종목코드']
        # 1년치 가격 데이터 추이를 필터링하기 위해 1년 기간 데이터 조회
        today = datetime.now()
        one_year_ago = today - timedelta(days=365)
        stock_data = stock.get_market_ohlcv(one_year_ago.strftime('%Y%m%d'), today.strftime('%Y%m%d'), stock_code)

        # 최근 60일 데이터 추출
        latest_60days = stock_data.tail(60)

        # 상장 60일 미만 종목 제외
        if latest_60days.size < 60:
            continue

        # 전 날 데이터 (-1이 오늘)
        one_day_ago = latest_60days.iloc[-2]
        # 이틀전 데이터
        two_day_ago = latest_60days.iloc[-3]

        # 동전주 제외
        if one_day_ago.loc['종가'] < 2000:
            continue

        # 전 날(1봉전) 60봉 신고거래량
        # pprint(latest_60days['거래량'].max())
        # print(last_day.loc['거래량'])
        if latest_60days[:-1]['거래량'].max() != one_day_ago.loc['거래량']:
            continue
        
        # 이틀전 대비 어제 종가 15% 이상 상승
        if int(two_day_ago.loc['종가'] * 1.15) > one_day_ago.loc['종가']:
            continue

        # 이틀전 대비 어제 고가 20% 이상 상승
        if int(two_day_ago.loc['고가'] * 1.20) > one_day_ago.loc['고가']:
            continue

        # 이틀부터 연속 양봉 발생
        if one_day_ago.loc['종가'] < one_day_ago.loc['시가']:
            continue

        one_day_ago.loc['종목코드'] = stock_code
        one_day_ago.loc['종목명'] = stock_item.loc['종목명']

        find_stock_list.append(one_day_ago)

    return pd.DataFrame(find_stock_list)

def 내재가치():
    # 종목 리스트
    stock_list = pd.DataFrame({'종목코드':stock.get_market_ticker_list(market="ALL")})
    stock_list['종목명'] = stock_list['종목코드'].map(lambda x: stock.get_market_ticker_name(x))

    # 펀더먼탈 지표 합치기
    yyyymmdd = datetime.now().strftime('%Y%m%d')
    stock_fud = pd.DataFrame(stock.get_market_fundamental_by_ticker(date=yyyymmdd, market="ALL"))
    stock_fud = stock_fud.reset_index()
    stock_fud.rename(columns={'티커':'종목코드'}, inplace=True)
    stock_fud_list = pd.merge(stock_list, stock_fud, left_on='종목코드', right_on='종목코드', how='outer')

    # 가격 정보 합치기
    stock_price = stock.get_market_ohlcv_by_ticker(date=yyyymmdd, market="ALL")
    stock_price = stock_price.reset_index()
    stock_price.rename(columns={'티커':'종목코드'}, inplace=True)
    stock_fud_price_list = pd.merge(stock_fud_list, stock_price, left_on='종목코드', right_on='종목코드', how='outer')
    pprint(stock_fud_price_list)

    # 값이 0이면 nan으로 바꾸고 삭제
    stock_fud_price_list = stock_fud_price_list.replace([0], np.nan)
    stock_fud_price_list = stock_fud_price_list.dropna(axis=0)

    # 내재가치 계산
    stock_fud_price_list['내재가치'] = (stock_fud_price_list['BPS'] + (stock_fud_price_list['EPS']) * 10) / 2
    stock_fud_price_list['내재가치/종가'] = (stock_fud_price_list['내재가치'] / stock_fud_price_list['종가'])

    # 필터링
    PERv10 = stock_fud_price_list['PER'] <= 10
    PBRv1 = stock_fud_price_list['PBR'] <= 1
    inner_value = stock_fud_price_list['내재가치/종가'] >= 4
    filtered_list = stock_fud_price_list[PERv10 & PBRv1 & inner_value]
    filtered_list = filtered_list.reset_index()

    