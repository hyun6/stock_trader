import buy_low_price_strategy

# 장 시작: 오늘 매수할 종목을 검색하고, 기존에 검색된 종목과 함께 매수 주문 요청
buy_low_price_strategy.find_stock()
buy_low_price_strategy.buy()

# 장 마감: 오늘 체결된 종목은 DB에서 제거
# buy_low_price_strategy.update_buy_list()