from fastapi import FastAPI, Path, Query, Response
from mymodule.DatabaseConnection import CRUD
from dotenv import load_dotenv
import pandas as pd

app = FastAPI()
load_dotenv()

@app.get('/')
def welcome():
    return 'Welcome to Market API'
@app.get('/StockCode')
def getStockCode():
    lo_stockcode = CRUD('stock')
    df = pd.DataFrame(lo_stockcode.Read(''))
    return Response(content=df.to_json(orient='records', indent=4), media_type='application/json')