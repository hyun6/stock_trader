import asyncio
import datetime

import api
import buy_low_price_strategy
from order_repository import order_repository
import notify
import command_handler

# TODO: 히스토리와 거래중인 종목을 관리할 DB 분리

async def 주식장_시작전():
    await notify.send_message('주식장_시작전')
    # 오늘 매수할 종목을 검색하고, 기존에 검색된 종목과 함께 매수 주문 요청
    find_stock_df = buy_low_price_strategy.find_stock()
    
    # 오늘 검색된 종목 notify
    await notify.send_message('매수 종목' + find_stock_df.to_markdown())
    
    # 어제자 매수 주문 정보 초기화
    order_repository.clear_buy_status()

async def 주식장_장중():
    await notify.send_message('주식장_장중')

    # TODO: 일정 시간 간격으로 주식 가격이 매수 조건에 맞는지 확인 후 주문
    while datetime.datetime.now().hour > 9 and datetime.datetime.now().hour < 16:
        buy_low_price_strategy.buy()
        await asyncio.sleep(60 * 60) # 1시간


async def 주식장_마감후():
    await notify.send_message('주식장_마감후')

    # 오늘 체결된 종목은 DB에서 제거
    buy_low_price_strategy.update_buy_list()

async def main():
    if api.is_holiday():
        await notify.send_message('오늘은 휴장일!')
        return

    await 주식장_시작전()
    await 주식장_장중()
    await 주식장_마감후()

if __name__ == '__main__':
    # telegram 커맨드 핸들러
    command_handler.init()

    asyncio.run(main())