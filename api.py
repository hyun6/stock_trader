from datetime import datetime, timedelta
from pprint import pprint
import pykis as pk
from prettytable import PrettyTable
import env

kis = pk.PyKis(
    # 앱 키  예) Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX
    appkey=env.get(env.EnvNames.APPKEY),
    # 앱 시크릿  예) V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvY . . .
    appsecret=env.get(env.EnvNames.APPSECRET),
    # 가상 계좌 여부
    virtual_account=True,
)

account = kis.account('50102375-01')

# 휴장일 여부
def is_holiday() -> bool:
    return kis.market.today().is_holiday


# 체결된 주문 조회
# now = datetime.now()
# daily_orders = account.daily_order_all(now - timedelta(days=1), now)
# for order in daily_orders.orders:
#     pprint(order)

# 체결 이벤트 리스너 설정
def on_oder(cli: pk.KisRTClient, res: pk.KisRTConclude):
    print(f'{res.acnt_no} {res.acpt_yn_name} {res.cntg_isnm} {res.cntg_yn_name} {res.order_kind_name}', end=' ')
    print(f'수량: {res.oder_qty:,}', end=' ')
    print(f'가격: {res.cntg_unpr:,}')
kis.rtclient.event.oder.add(on_oder)

# 체결 이벤트 수신 시작
kis.rtclient.add('체결', '$0380847')

# balance = account.balance_all()

# # 결과를 출력한다.
# print(f'예수금: {balance.dnca_tot_amt:,}원 평가금: {balance.tot_evlu_amt:,} 손익: {balance.evlu_pfls_smtl_amt:,}원')

# # 테이블을 시각화 하기 위해 PrettyTable을 사용한다.

# table = PrettyTable(field_names=[
#         '상품번호', '상품명', '보유수량', '매입금액',
#         '현재가', '평가손익율', '평가손익',
#     ], align='r',
# )

# # 잔고를 테이블에 추가한다.
# for stock in balance.stocks:
#     table.add_row([
#         stock.pdno,
#         stock.prdt_name,
#         f'{stock.hldg_qty:,}주',
#         f'{stock.pchs_amt:,}원',
#         f'{stock.prpr:,}원',
#         f'{stock.evlu_pfls_rt:.2f}%',
#         f'{stock.evlu_pfls_amt:,}원',
#     ])

# print(table)