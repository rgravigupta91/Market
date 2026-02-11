#from mymodule.mymodule.DatabaseConnection import CRUD, RangeParser, RangeTable
from dotenv import load_dotenv
from mymodule.DatabaseConnection import CRUD, DBConnectionFactory, CSVHandler, SqlServerHandler
from mymodule.Range import RangeParser, RangeTable
load_dotenv()

__all__ = ["CRUD", "RangeParser", "RangeTable", "DBConnectionFactory", "CSVHandler", "SqlServerHandler"]

class update_ticker():
    def __init__(self):
        pass

    def update_book_value(self, ISIN:str, bookvalue:float):
        pass