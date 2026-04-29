import numpy as np
import pandas as pd
from sklearn import preprocessing



# データフレーム内の行・列の削除
def Check_df(df, head_lines=5):
    """
    dataframeの冒頭、カラム一覧、カラム数、行数、基本情報、統計量を表示。
    【引数】
    df[pandas.DataFrame]：表示するデータフレーム。
    head_lines[int]：冒頭から表示する行数。指定しない場合は5。
    【戻り値】
    columns[list]：データフレームのカラム一覧。
    number_of_rows[int]：データフレームの行数。
    """

    print("==================================")
    print("データフレームの冒頭{head_lines}行を表示".format(head_lines=head_lines))    
    print(df.head(head_lines))
    print("==================================")
    print("データフレームのカラム一覧、カラム数、列数を表示")
    columns = list(df.columns)
    print(f"カラム一覧: {columns}")
    print(f"カラム数: {len(columns)}")
    number_of_rows = len(df)
    print(f"行数: {number_of_rows}")
    print("==================================")
    print("データフレームの基本情報を表示")    
    print(df.info())
    print("==================================")
    print("データフレームの統計量を表示")
    print(df.describe())

    return columns, number_of_rows



# データフレーム内の行・列の削除
def Drop_index_column_df(df, drop_index=None, drop_column=None):
    """
    dataframeの指定した行・列を削除。
    【引数】
    df[pandas.DataFrame]：行・列を削除するデータフレーム。
    drop_index[list]：削除する行名（リスト形式）。
    drop_column[list]：削除する列名（リスト形式）。
    inplace[bool]：Trueの場合、元のデータフレームを変更。Falseの場合、新しいデータフレームを返す。
    【戻り値】
    df[pandas.DataFrame]：行・列が削除されたデータフレーム。
    """
    
    if drop_index != None:
        df.drop(drop_index, inplace=True)
    else:
        pass
    
    if drop_column != None:
        df.drop(drop_column, axis=1, inplace=True)
    else:
        pass

    return df



# データフレーム内の数値変数の正規化（Min-maxスケーリング）
def Min_max_scaler_df(df, x_list, replace=True):
    '''
    dataframeの指定したカラムの値を最小値0、最大値1の範囲にスケーリング。
    【引数】
    df[pandas.DataFrame]：正規化するデータフレーム。
    x_list[list]：正規化するカラム名のリスト。
    replace[bool]：Trueの場合、元のカラムを置き換える。Falseの場合、新しいカラムを作成する。
    【戻り値】
    df[pandas.DataFrame]：正規化されたデータフレーム。
    '''
    
    # x_listの各カラムに対して、最小値と最大値を計算し、Min-maxスケーリングを適用。replaceがTrueの場合は元のカラムを置き換え、Falseの場合は新しいカラムを作成。
    for x in x_list:
        x_min = df[x].min()
        x_max = df[x].max()
        if replace:
            df[x] = (df[x] - x_min) / (x_max - x_min)
        else:
            df[f"{x}_minmax"] = (df[x] - x_min) / (x_max - x_min)
    
    return df



# データフレーム内のカテゴリ変数のone-hotエンコーディング
def One_hot_encoding_df(df, columns=None, drop_first=True):
    """
    df：one-hotエンコーディングを実行するデータフレーム。
    columns：one-hotエンコーディングを実行するカラム名（リスト形式）。指定がなければ全カラムに実行。数値型の場合実行されないので、事前に文字列型に変換しておく。
    drop_first：エンコーディング後の最初のカラムを削除するかどうかを指定。Trueなら削除。
    """
    
    if columns == None:
        df = pd.get_dummies(df, drop_first=drop_first)
    elif type(columns) == list:
        df = pd.get_dummies(df, columns=columns, drop_first=drop_first)
    else:
        print("変数'columns'はリスト型、もしくは指定なし")
        
    return df


# ### ラベルエンコーディング

# In[ ]:


def Label_encoding_df(df, columns_labels_dict):
    """
    df：ラベルエンコーディングを実行するデータフレーム。
    columns_labels_dict：ラベルエンコーディングを実行するカラム名をキーに、そのカラム内のラベルのリストをバリューに持つ辞書。
    """
    
    le = preprocessing.LabelEncoder()
    
    for column, labels in columns_labels_dict.items():
        labels_id = le.fit_transform(labels)
        for l, i in zip(labels, labels_id):
            df[column] = df[column].replace(l, i)
    
    return df