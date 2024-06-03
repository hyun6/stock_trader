from peewee import Model, SqliteDatabase


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase("stock_trader.db")
