import pymysql
from dotenv import load_dotenv
import os
import pandas as pd
from pydantic import BaseModel
from typing import Literal

load_dotenv()

class DBConnection:
    def __init__(self):
        self.connection = pymysql.connect(
            host        = os.environ['dbhost'],
            user        = os.environ['dbuser'],
            password    = os.environ['dbpassword'],
            database    = os.environ['database'],
            cursorclass = pymysql.cursors.DictCursor
        )

        self.cursor = self.connection.cursor()
    
    def __del__(self):
        self.connection.close()
        print('DataBase Disconnected')

    def get_connection(self):
        return self.connection

class RangeTable(BaseModel):
    fieldname: str
    sign: str = Literal['I','E']
    option: str = Literal['EQ','GT','GE','LT','LE','BT','NE','CS']
    low: str
    high: str

class RangeParser:
    def __init__(self, df_range):
        self.range = df_range

    def get_parsed(self):
        for row in self.range:
            match row.option: #['option']:
                case 'EQ':
                    condition = f"{row.fieldname} = {row.low}"
        return condition
    @staticmethod
    def get_initial_rangetable():
        return pd.DataFrame(columns=RangeTable.model_fields.keys())
    
class CRUD(DBConnection):
    def __init__(self, tablename:str):
        super().__init__()
        self.tablename = tablename

        sql = f"Describe {tablename}"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        
        self.schema = {}
        for row in results:
            key = row['Field']
            self.schema[key] = row
        self.df_schema = pd.DataFrame(results)
        
        self.sql_insert = f"INSERT INTO {tablename} ({', '.join(self.schema.keys())}) values({', '.join(['%s'] * self.df_schema.shape[0])})"
        self.sql_select = f"Select * from {tablename}"
        self.sql_update = f""
        self.sql_delete = f""



    def __getstructure__(self):
        # Example query
        sql = "Describe " + self.tablename
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        print(results)
        #for row in results:
            # print((row))

    def Create(self, df):
        for row in df.itertuples(index=False): 
            self.cursor.execute(self.sql_insert, row)
        self.connection.commit()

    def Read(self, data):
        self.cursor.execute(self.sql_select)
        return self.cursor.fetchall()
    def Update(self, data):
        pass
    def delete(self, data):
        pass