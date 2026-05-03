import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler



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
def Drop_index_column_df(df, drop_index_list=None, drop_column_list=None):
    """
    dataframeの指定した行・列を削除。
    【引数】
    df[pandas.DataFrame]：行・列を削除するデータフレーム。
    drop_index_list[list]：削除する行名（リスト形式）。
    drop_column_list[list]：削除する列名（リスト形式）。
    inplace[bool]：Trueの場合、元のデータフレームを変更。Falseの場合、新しいデータフレームを返す。
    【戻り値】
    df[pandas.DataFrame]：行・列が削除されたデータフレーム。
    """
    
    if drop_index_list != None:
        df.drop(drop_index_list, inplace=True)
    else:
        pass
    
    if drop_column_list != None:
        df.drop(drop_column_list, axis=1, inplace=True)
    else:
        pass

    return df



# データフレーム内の数値変数の正規化（Min-maxスケーリング）
def Min_max_scaler_df(df, column_list, replace=True):
    '''
    dataframeの指定したカラムの値を最小値0、最大値1の範囲にスケーリング。
    【引数】
    df[pandas.DataFrame]：正規化するデータフレーム。
    column_list[list]：正規化するカラム名のリスト。
    replace[bool]：Trueの場合、元のカラムを置き換える。Falseの場合、新しいカラムを作成する。
    【戻り値】
    df[pandas.DataFrame]：正規化されたデータフレーム。
    '''
    
    # column_listの各カラムに対して、最小値と最大値を計算し、Min-maxスケーリングを適用。replaceがTrueの場合は元のカラムを置き換え、Falseの場合は新しいカラムを作成。
    for column in column_list:
        column_min = df[column].min()
        column_max = df[column].max()
        if replace:
            df[column] = (df[column] - column_min) / (column_max - column_min)
        else:
            df[f"{column}_minmax"] = (df[column] - column_min) / (column_max - column_min)
    
    return df



# データフレーム内の数値変数の標準化
def Standard_scaler_df(df, column_list=None):
    '''
    dataframeの指定したカラムの値を標準化（平均を0、標準偏差を1にスケーリング）。
    【引数】
    df[pandas.DataFrame]：標準化するデータフレーム。
    column_list[list]：標準化するカラム名のリスト。指定しない場合は全てのカラムを使用。
    【戻り値】
    scaler_array[numpy.array]：正規化された値の配列。
    mean_dict[dict]：各カラムの平均値を格納した辞書。キーがカラム名、バリューが平均値。
    var_dict[dict]：各カラムの分散を格納した辞書。キーがカラム名、バリューが分散。
    '''
    
    if column_list == None:
        column_list = df.columns()

    df_ = df[column_list]
    scaler = StandardScaler()
    scaler_array = scaler.fit_transform(df_)

    mean_list = [float(mean) for mean in scaler.mean_]
    mean_dict = {}
    for column, mean in zip(column_list, mean_list):
        mean_dict[column] = mean

    var_list = [float(var) for var in scaler.var_]
    var_dict = {}
    for column, var in zip(column_list, var_list):
        var_dict[column] = var

    return scaler_array, mean_dict, var_dict



# データフレーム内のカテゴリ変数のone-hotエンコーディング
def One_hot_encoding_df(df, columns=None, drop_first=True):
    """
    dataframeの指定したカラムにone-hotエンコーディングを実施。
    【引数】
    df[pandas.DataFrame]：one-hotエンコーディングを実行するデータフレーム。
    columns[list]：one-hotエンコーディングを実行するカラム名（リスト形式）。指定がなければ全カラムに実行。数値型の場合実行されないので、事前に文字列型に変換しておく。
    drop_first[bool]：エンコーディング後の最初のカラムを削除するかどうかを指定。Trueなら削除。
    【戻り値】
    df[pandas.DataFrame]：one-hotエンコードされたデータフレーム。
    """
    
    if columns == None:
        df = pd.get_dummies(df, drop_first=drop_first)
    elif type(columns) == list:
        df = pd.get_dummies(df, columns=columns, drop_first=drop_first)
    else:
        print("変数'columns'はリスト型、もしくは指定なし")
        
    return df



# ラベルエンコーディング
def Label_encoding_df(df, columns_labels_dict):
    """
    dataframeの指定したカラムにラベルエンコーディングを実施。
    【引数】
    df[pandas.DataFrame]：ラベルエンコーディングを実行するデータフレーム。
    columns_labels_dict[dict]：ラベルエンコーディングを実行するカラム名をキーに、そのカラム内のラベルのリストをバリューに持つ辞書。
    【戻り値】
    df[pandas.DataFrame]：ラベルエンコードされたデータフレーム。
    """
    
    le = preprocessing.LabelEncoder()
    
    for column, labels in columns_labels_dict.items():
        labels_id = le.fit_transform(labels)
        for l, i in zip(labels, labels_id):
            df[column] = df[column].replace(l, i)
    
    return df



def Principal_component_analysis_df(df, n_components=2, column_list=None, primary_key_column_list=None):
    '''
    dataframeの指定したカラムに主成分分析を実施。
    【引数】
    df[pandas.DataFrame]：主成分分析するデータフレーム。
    n_components[int]：主成分数。指定しない場合は2。
    column_list[list]：主成分分析するカラム名のリスト。指定しない場合はprimary_key_column_listで指定した手記ー以外の全てのカラムを使用。
    primary_key_column_list[list]：主成分分析するデータフレームの主キーリスト。指定したカラムの内容を主成分分析後のデータフレームに付与。指定しない場合は無し。
    【戻り値】
    pca_df[pandas.DataFrame]：主成分分析後のデータフレーム。
    explained_variance_ratio[dict]：主成分分析後の各カラムのバリアンスを格納した辞書（バリアンスの降順）。キーがカラム名、バリューがバリアンス。
    cumulative_variance_ratio[dict]：主成分分析後の各カラムのバリアンスの累積和を格納した辞書。キーがカラム名、バリューがバリアンスの累積和。
    '''

    # column_listがNoneでprimary_key_column_listが指定されている場合に、column_listはprimary_key_column_listで指定した主キー以外の全カラムで指定
    if (column_list == None) and (primary_key_column_list != None):
        column_list = [column for column in df.columns if column not in primary_key_column_list]
    # column_listとprimary_key_column_listの両方がNoneの場合に、column_listは全カラムで指定
    elif (column_list == None) and (primary_key_column_list == None):
        column_list = [column for column in df.columns]

    scaler_array, _, _ = Standard_scaler_df(df, column_list)
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(scaler_array)
    PCA_column_list = [f'PC{num}' for num in range(1, n_components+1)]
    pca_df = pd.DataFrame(principal_components, columns=PCA_column_list)

    if primary_key_column_list != None:
        for primary_key in primary_key_column_list:
            pca_df[primary_key] = df[primary_key]
        
        pca_df = pca_df[primary_key_column_list+PCA_column_list]

    explained_variance_ratio_dict = {}
    explained_variance_ratio = [float(variance) for variance in pca.explained_variance_ratio_]
    for column, variance in zip(PCA_column_list, explained_variance_ratio):
        explained_variance_ratio_dict[column] = variance

    cumulative_variance_ratio_dict = {}
    cumulative_variance_ratio = [float(cumulative) for cumulative in np.cumsum(explained_variance_ratio)]
    for column, cumulative in zip(PCA_column_list, cumulative_variance_ratio):
        cumulative_variance_ratio_dict[column] = cumulative

    return pca_df, explained_variance_ratio, cumulative_variance_ratio