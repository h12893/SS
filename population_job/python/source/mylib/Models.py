import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# サンプルデータ生成（2次元）
np.random.seed(42)
X = np.vstack([
    np.random.normal([0, 0], 0.5, size=(50, 2)),
    np.random.normal([3, 3], 0.5, size=(50, 2)),
    np.random.normal([0, 4], 0.5, size=(50, 2))
])



# K-means クラスタリング
def K_means_2D(df, primary_key_list=None, n_clusters=3, n_init=10):
    '''
    2次元のデータフレーム（主キーは除く）に対してK-means法によるクラスタリングを実施。
    【引数】
    df[pandas.DataFrame]：K-meansクラスタリングを実施するデータフレーム。主キーを除いてカラムが2次元でない場合は実施不可。
    primary_key_list[list]：K-meansクラスタリングには用いない主キーのカラム名のリスト。
    n_clusters[int]：クラスタの数。指定しない場合は3で設定。
    n_init[int]：クラスタ中心をランダムな初期位置から試行する回数。指定しない場合は10で設定。
    【戻り値】
    df[pandas.DataFrame]：入力したデータフレームに、カラム名'cluster'でクラスタ番号を追加したデータフレーム。
    '''

    # 主キーがある場合
    if primary_key_list != None:
        variables = [column for column in df.columns if column not in primary_key_list]
        # 主キーを除いたカラム数が2になっているか確認。なっていない場合は処理中止。
        if len(variables) != 2:
            print("主キーを除いたデータフレームが2次元でないので実行不可")
            exit
        else:
            pass
        df_2D = df[variables]
    # 主キーが無い場合
    else:
        # カラム数が2になっているか確認。なっていない場合は処理中止。
        if len(df.columns != 2):
            print("データフレームが2次元でないので実行不可")
            exit
        else:
            pass
        df_2D = df.copy()
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=n_init)
    df['cluster'] = kmeans.fit_predict(df_2D)

    return df