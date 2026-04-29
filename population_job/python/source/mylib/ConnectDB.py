import pandas as pd
import pyodbc
import chardet



# データベースに接続、クエリを実行してテーブルの内容を取得し、結果をDataFrame形式で返す関数。
def Fetch_data(query, config_path):
    '''
    データベースに接続、クエリを実行してテーブルの内容を取得し、結果をDataFrame形式で返す。
    【引数】
    query[str]: SQLのクエリ文字列。
    config_path[str]: configファイルのパス。
    【戻り値】
    df[pandas.DataFrame]: クエリの実行結果を格納したDataFrame。
    '''
    
    # エンコーディングをchardetで自動検出。
    with open(config_path, 'rb') as f:
        encoding = chardet.detect(f.read())['encoding']

    with open(config_path, 'r', encoding=encoding) as f:
        lines = f.readlines()
    connection_string = ''.join(line.strip() for line in lines if not line.strip().startswith('#')).strip()
    conn = pyodbc.connect(connection_string)

    try:
        df = pd.read_sql(query, conn)
        return df
    finally:
        conn.close()


