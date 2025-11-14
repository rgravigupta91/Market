import pymysql
import os
import pandas   as pd

from dotenv     import load_dotenv
from pydantic   import BaseModel
from typing     import Literal

class RangeTable(BaseModel):
    fieldname: str
    sign: str = Literal['I','E']      # I: Including,  E: Excluding
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
    
class DBConnection:
    def __init__(self, schema: None):
        load_dotenv()
        if schema is None:
            schema = os.environ['database']
        match os.environ['dbserver']:
            case 'mysqlserver':                    
                self.connection = pymysql.connect(
                    host        = os.environ['dbhost'],
                    user        = os.environ['dbuser'],
                    password    = os.environ['dbpassword'],
                    database    = schema,
                    cursorclass = pymysql.cursors.DictCursor
                        )
            case _:
                raise Exception('Database not configured')

        self.cursor = self.connection.cursor()
    
    def __del__(self):
        self.connection.close()
        print('DataBase Disconnected')

    def execute_query(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
    def get_connection(self):
        return self.connection


    
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
        self.sql_update = f"Update {tablename} set {tablename} where {tablename}"
        self.sql_delete = f"Delete {tablename} where {tablename}"



    def __getstructure__(self):
        # Example query
        sql = "Describe " + self.tablename
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        print(results)


    def Create(self, df):
        data = df.values.tolist()
        print(data)
        try:
            self.cursor.executemany(self.sql_insert, data)
            self.connection.commit()
        except Exception as e:
            print(e)
            self.connection.rollback()
        #for row in df.itertuples(index=False): 
        #    self.cursor.execute(self.sql_insert, row)

    def Read(self, data):
        self.cursor.execute(self.sql_select)
        df = pd.DataFrame(self.cursor.fetchall(), columns=self.schema.keys())
        return df
    
    def Update(self, data):
        values = data
        self.cursor.execute(self.sql_update, values)
        self.connection.commit()
    def delete(self, data):
        values = data
        self.cursor.execute(self.sql_delete, values)
        self.connection.commit()
    def upsert(self, data):
        pass