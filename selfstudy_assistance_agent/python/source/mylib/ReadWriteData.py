import pandas as pd
import os
from pathlib import Path
import chardet
from source.mylib.ConnectDB import Fetch_data
import openpyxl
import json

######################################################################################################################################################

# ファイル有無確認
def Check_file_exists(file_path):
    '''
    指定したパスのファイルが存在するか確認。
    【引数】
    file_path[str]: 確認するファイルのパス。
    【戻り値】
    bool: ファイルが存在する場合はTrue、存在しない場合はFalse。
    '''

    return Path(file_path).is_file()

######################################################################################################################################################

# CSVファイルをDataFrameで読み込み
def Read_csv_to_df(file_path, encoding=None, header=0, reset_index=True):
    '''
    CSVファイルをDataFrameで読み込み。
    【引数】
    file_path[str]: 読み込むCSVファイルのパス。
    encoding[str]: ファイルのエンコーディング。指定しない場合はchardetで自動検出。
    header[int, None]: ヘッダー行のインデックス。指定しない場合は0。ヘッダー行が無い場合はNoneを指定。
    reset_index[bool]: インデックスをリセットするかどうかを指定するブール値。Trueの場合はインデックスをリセット、Falseの場合はインデックスをリセットしない。指定しない場合はTrue。
    【戻り値】
    df[pandas.DataFrame]: 読み込んだデータを格納したDataFrame。
    '''

    try:
        file_path = Path(file_path)

        # エンコーディングが指定されていない場合はchardetで自動検出。
        if encoding is None:
            with open(file_path, 'rb') as f:
                encoding = chardet.detect(f.read())['encoding']

        # ファイル読み込み
        df = pd.read_csv(
            file_path, 
            encoding=encoding,
            header=header
        ).reset_index(drop = reset_index)

        return df

    # ファイルが見つからない場合の例外処理。
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {file_path}")
        
    # 文字コードが合わない場合の例外処理。
    except UnicodeDecodeError:
        print(f"文字コードが合いません。encoding='{encoding}' を確認してください。")

    # その他の例外処理。
    except Exception as e:
        print(f"エラー: {e}")

######################################################################################################################################################

# Excelファイル読み込み
def Read_xlsx_to_df(file_path, sheet_name=0, header=None, reset_index=True):
    '''
    ExcelファイルをDataFrameで読み込み。
    【引数】
    file_path[str]: 読み込むExcelファイルのパス。
    sheet_name[str, int]: 読み込むシート名またはインデックス。指定しない場合は0（最初のシート）。
    header[int, None]: ヘッダー行のインデックス。指定しない場合はNone。ヘッダー行が無い場合はNoneを指定。
    reset_index[bool]: インデックスをリセットするかどうかを指定するブール値。Trueの場合はインデックスをリセット、Falseの場合はインデックスをリセットしない。指定しない場合はTrue。
    【戻り値】
    df[pandas.DataFrame]: 読み込んだデータを格納したDataFrame。
    '''

    try:
        file_path = Path(file_path)

        # ファイル読み込み
        df = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            header=header,
            engine="openpyxl"  # .xlsx 読み込み用
        ).reset_index(drop = reset_index)

        return df

    # ファイルが見つからない場合の例外処理。
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {file_path}")

    # 列やシートの指定が不正な場合の例外処理。
    except ValueError as e:
        print(f"[エラー] 列やシートの指定が不正です: {e}")
    
    # その他の例外処理。
    except Exception as e:
        print(f"[エラー] 読み込み中に予期しないエラーが発生しました: {e}")
    
######################################################################################################################################################

# DataFrameをCSVファイルに書き込み
def Write_csv_from_df(df, file_path, encoding="utf-8-sig", index=False):
    '''
    DataFrameをCSVファイルに書き込み。
    【引数】
    df[pandas.DataFrame]: 書き込むデータを格納したDataFrame。
    file_path[str]: 書き込むCSVファイルのパス。
    encoding[str]: ファイルのエンコーディング。指定しない場合は"utf-8-sig"。
    '''

    file_path = Path(file_path)

    # ファイル書き込み
    df.to_csv(
        file_path, 
        encoding=encoding,
        index=index
    )

######################################################################################################################################################

# def Write_xlsx_from_df(df, file_path, sheet_name='Sheet1', index=False):
#     '''
#     DataFrameをExcelファイルに書き込み。
#     【引数】
#     df[pandas.DataFrame]: 書き込むデータを格納したDataFrame。
#     file_path[str]: 書き込むExcelファイルのパス。
#     sheet_name[str]: 書き込むシート名。指定しない場合は'Sheet1'。
#     index[bool]: インデックスをファイルに書き込むかどうかを指定するブール値。Trueの場合はインデックスも書き込む、Falseの場合はインデックスを書き込まない。指定しない場合はFalse。
#     '''

#     file_path = Path(file_path)

    # ファイル書き込み
    # df.to_excel(
    #     file_path,
    #     sheet_name=sheet_name,
    #     index=index,
    #     engine="openpyxl"  # .xlsx 書き込み用
    # )
# with pd.ExcelWriter('multi_sheet.xlsx') as writer:
#    df.to_excel(writer, sheet_name='シート1', index=False)
#    df.to_excel(writer, sheet_name='シート2', index=False)

######################################################################################################################################################

# 辞書型データをJSONファイルで保存
def Write_json_from_dict(output_dict, file_path, encoding="utf-8-sig"):
    '''
    辞書型データをJSONファイル形式で保存
    【引数】
    output_dict[dict]: 書き込むデータを格納した辞書。
    file_path[str]: 書き込むJSONファイルのパス。
    encoding[str]: ファイルのエンコーディング。指定しない場合は"utf-8-sig"。
    '''

    file_path = Path(file_path)

    try:
        with open(file_path, "w", encoding=encoding) as f:
            json.dump(output_dict, 
                      f, 
                      ensure_ascii=False, # ensure_ascii=False で日本語をそのまま出力
                      indent=4 # indent=4 で見やすく整形
                      )
        print(f"JSONファイルに保存しました: {file_path}")
    except (OSError, TypeError) as e:
        print(f"保存中にエラーが発生しました: {e}")

######################################################################################################################################################
    
# 指定したデータをdata_dictに追加する関数
def Add_data_to_dict(data_dict, data_name, data_dir, config_path):
    '''
    指定したデータがdataディレクトリにCSVファイルとして存在する場合は読み込み、存在しない場合はSQLクエリを実行してデータを取得。
    どちらの場合もデータを取得後にdata_dictに追加。
    keyは'{data_name}_df'、valueはDataFrame形式のデータ。
    【引数】
    data_dict[dict]: データを格納する辞書。
    data_name[str]: 追加するデータの名前。
    data_dir[str]: データが保存されているディレクトリのパス。
    config_path[str]: configファイルのパス。SQLクエリを実行してデータを取得する場合に使用。
    【戻り値】
    data_dict[dict]: データが追加された辞書。
    '''

    # dataディレクトリにcsvファイルが存在する場合は読み込み、存在しない場合はSQLクエリを実行してデータを取得
    data_path = os.path.join(data_dir, f"{data_name}.csv")
    if os.path.isfile(data_path):
        print(f"✓ ファイルが存在します: {data_path}")
        data_dict[f'{data_name}_df'] = Read_csv_to_df(data_path)

        print(f"✓ ファイル取得完了")

    else:
        print(f"✗ ファイルが存在しません: {data_path}")
        print("SQLクエリを実行してデータを取得します")

        # 実行するクエリを定義
        query = """
        SELECT
            *
        FROM {data_name}
        """.format(data_name=data_name)

        print(f"実行するクエリ:")
        print(query)

        # クエリを実行してデータを取得
        data_dict[f'{data_name}_df'] = Fetch_data(query, config_path)
        print(f"✓ クエリ実行完了")

        # 取得したデータをCSVファイルに保存
        Write_csv_from_df(data_dict[f'{data_name}_df'], data_path)
        print(f"✓ データをCSVファイルに保存しました: {data_path}")

    return data_dict

