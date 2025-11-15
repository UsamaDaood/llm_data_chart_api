import pandas as pd

def dataframe_schema(df: pd.DataFrame) -> dict:
    cols = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        cols.append({"name": col, "dtype": dtype})
    return {"columns": cols, "row_count": len(df)}
