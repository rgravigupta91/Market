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