import pandas as pd
import pyodbc
from pathlib import Path

# データベースへの接続文字列をconfigファイルから読み込む。
config_path = Path(__file__).resolve().parents[2] / 'config' / 'connect_DB.config'
with open(config_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
connection_string = ''.join(line.strip() for line in lines if not line.strip().startswith('#')).strip()
conn = pyodbc.connect(connection_string)

# データベースに接続、クエリを実行してテーブルの内容を取得し、結果をDataFrame形式で返す関数。
def fetch_data(query, conn=conn):
    '''
    データベースに接続、クエリを実行してテーブルの内容を取得し、結果をDataFrame形式で返す。
    query[str]: SQLのクエリ文字列
    conn[pyodbc.connection]: データベースへの接続オブジェクト
    '''
    df = pd.read_sql(query, conn)
    return df


