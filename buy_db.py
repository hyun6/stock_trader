import pandas as pd
import sqlite3
from util import SingletonInstane

# TODO: peewee ORM 사용 고려해 보자

DB_FILE_NAME = "buy_list.db"
TABLE_NAME = "buy_list"

# 테이블 컬럼
# 종목코드, 종목명, 시가, 저가, 종가, 고가, 매수가, 매도가, 시작일, 만료일

class BuyListDB(SingletonInstane):
    def __init__(self):
        self.con = sqlite3.connect(DB_FILE_NAME, check_same_thread=False)
        self.cursor = self.con.cursor()

    # 조건 검색 결과 종목들을 일정 기간동안 매수 시도하기 위해 db에 저장
    # 매일 주식장이 끝난 후 갱신
    def set_buy_list(self, df_buy_list: pd.DataFrame) -> None:
        print("----set_buy_list----")
        print(df_buy_list)

        # TODO: 매수 목록에 이미 있는 종목을 추가로 매수하고 싶은 경우 replace 파라미터 제거
        df_buy_list.to_sql(TABLE_NAME, self.con, if_exists="replace")
        self.con.commit()

    # DB에서 검색 결과를 조회
    # 이 종목들로 오전에 주식장이 시작할 때 매수 주문
    def get_buy_list(self) -> pd.DataFrame:
        try:
            df_buy_list = pd.read_sql_query(
                f"SELECT * FROM {TABLE_NAME}", self.con
            )
            print("----get_search_result_db----")
            print(df_buy_list)
            return df_buy_list
        except Exception as e:
            print(f"DB 조회 실패: {e}, {type(e)}")
            return None

    # 매수 주문 번호를 갱신한다
    #  - 체결된 종목은 제거하기 위해 사용함
    def update_order_number(self, order_dict: dict):
        for code, order in order_dict.items():
            self.cursor.execute(f"UPDATE {TABLE_NAME} SET 주문번호={order.odno} WHERE 종목코드={code}")
        self.con.commit()

buyListDB = BuyListDB.instance()