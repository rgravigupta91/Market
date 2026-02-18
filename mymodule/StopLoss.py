from pandas import DataFrame
class StopLoss():
    def __init__(self, df: DataFrame):
        self.df = df
    
    def get_ATR(self, days=14):
        df1 = self.df.copy()
        df1['TR'] = abs(df1['high'] - df1['low'])
        df1['ATR'] = df1['TR'].rolling(days).mean()

        return float(df1.tail(1)['ATR'].values[0])