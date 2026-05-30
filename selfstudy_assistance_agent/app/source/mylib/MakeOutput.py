import matplotlib.pyplot as plt
import japanize_matplotlib 
japanize_matplotlib.japanize()
from matplotlib.ticker import MaxNLocator
import numpy as np

######################################################################################################################################################

# 散布図
def Make_scatter_plot(x_dict, y_dict, x_integer=False, y_integer=False, x_lim=None, y_lim=None, title='', xlabel='', ylabel='', legend_bottom=False, ncol=2, path=None):
    '''
    散布図を作図し、コンソールに表示 or 指定したパスに保存。
    【引数】
    x_dict[dict]: x軸のデータを格納した辞書。keyは特に意味は無し、valueはx軸のデータ。
    y_dict[dict]: y軸のデータを格納した辞書。keyは凡例、valueはy軸のデータ。
    x_integer[bool]: x軸の目盛りを整数に設定するかどうか。指定しない場合は自動で設定。
    y_integer[bool]: y軸の目盛りを整数に設定するかどうか。指定しない場合は自動で設定。
    x_lim[tuple]: x軸の範囲を指定するタプル。（最小値, 最大値）の形式。指定しない場合は自動で設定。
    y_lim[tuple]: y軸の範囲を指定するタプル。（最小値, 最大値）の形式。指定しない場合は自動で設定。
    title[str]: グラフのタイトル。指定しない場合は空白。
    xlabel[str]: x軸のラベル。指定しない場合は空白。
    ylabel[str]: y軸のラベル。指定しない場合は空白。
    legend_bottom[bool]: 凡例をグラフの下部に表示するかどうか。Trueの場合は下部に表示、Falseの場合は通常位置に表示。指定しない場合はFalse。
    ncol[int]:凡例をグラフの下部に表示する場合の1行当たりの凡例件数。指定しない場合は2で設定。
    path[str]: グラフを保存するパス。指定しない場合はコンソールに表示。
    '''

    fig, ax = plt.subplots()

    # x_dictとy_dictのkeyをzipで同時にループさせて、複数要素の散布図を1枚のグラフ内に描画。
    for key_x, key_y in zip(x_dict, y_dict):
        ax.scatter(x_dict[key_x], y_dict[key_y], label=key_y)
    
    # グラフのタイトル、軸ラベル、範囲を設定。凡例も表示。
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if legend_bottom:
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.11), ncol=ncol, fontsize=8)
    else:
        plt.legend(fontsize=8)

    # x_limとy_limがNoneでない場合は、グラフの範囲を設定。
    if x_lim is not None:
        ax.set_xlim(x_lim[0], x_lim[1])
    if y_lim is not None:
        ax.set_ylim(y_lim[0], y_lim[1])

    if x_integer:
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if y_integer:
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # グリッドを表示。グリッドのスタイルは、線の色を灰色、線のスタイルを点線、線の太さを0.7、透明度を0.7に設定。
    plt.grid(
        True,                # グリッド表示
        which='both',        # 'major', 'minor', 'both'
        axis='both',         # 'x', 'y', 'both'
        color='gray',        # 線の色
        linestyle='--',      # '--', '-.', ':', '-'
        linewidth=0.7,       # 線の太さ
        alpha=0.7            # 透明度
    )
    # グラフを保存するか表示するかをpathの内容から判断。
    if path == None:
        plt.tight_layout()
        plt.show()
    else:        
        plt.tight_layout()
        plt.savefig(path, bbox_inches='tight', pad_inches=0.1)
        plt.show()

######################################################################################################################################################

# 折れ線グラフ
def Make_line_plot(x_dict, y_dict, x_integer=False, y_integer=False, x_lim=None, y_lim=None, title='', xlabel='', ylabel='', legend_bottom=False, ncol=2, path=None):
    '''
    折れ線グラフを作図し、コンソールに表示 or 指定したパスに保存。
    【引数】
    x_dict[dict]: x軸のデータを格納した辞書。keyは特に意味は無し、valueはx軸のデータ。
    y_dict[dict]: y軸のデータを格納した辞書。keyは凡例、valueはy軸のデータ。
    x_integer[bool]: x軸の目盛りを整数に設定するかどうか。指定しない場合は自動で設定。
    y_integer[bool]: y軸の目盛りを整数に設定するかどうか。指定しない場合は自動で設定。
    x_lim[tuple]: x軸の範囲を指定するタプル。（最小値, 最大値）の形式。指定しない場合は自動で設定。
    y_lim[tuple]: y軸の範囲を指定するタプル。（最小値, 最大値）の形式。指定しない場合は自動で設定。
    title[str]: グラフのタイトル。指定しない場合は空白。
    xlabel[str]: x軸のラベル。指定しない場合は空白。
    ylabel[str]: y軸のラベル。指定しない場合は空白。
    legend_bottom[bool]: 凡例をグラフの下部に表示するかどうか。Trueの場合は下部に表示、Falseの場合は通常位置に表示。指定しない場合はFalse。
    ncol[int]:凡例をグラフの下部に表示する場合の1行当たりの凡例件数。指定しない場合は2で設定。
    path[str]: グラフを保存するパス。指定しない場合はコンソールに表示。'''

    fig, ax = plt.subplots()

    # x_dictとy_dictのkeyをzipで同時にループさせて、複数要素の折れ線グラフを1枚のグラフ内に描画。
    for key_x, key_y in zip(x_dict, y_dict):
        ax.plot(x_dict[key_x], y_dict[key_y], label=key_y, marker='o')

    # グラフのタイトル、軸ラベル、範囲を設定。凡例も表示。
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if legend_bottom:
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.11), ncol=ncol, fontsize=8)
    else:
        plt.legend(fontsize=8)

    # x_limとy_limがNoneでない場合は、グラフの範囲を設定。
    if x_lim is not None:
        ax.set_xlim(x_lim[0], x_lim[1])
    if y_lim is not None:
        ax.set_ylim(y_lim[0], y_lim[1])

    if x_integer:
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if y_integer:
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # グリッドを表示。グリッドのスタイルは、線の色を灰色、線のスタイルを点線、線の太さを0.7、透明度を0.7に設定。
    plt.grid(
        True,                # グリッド表示
        which='both',        # 'major', 'minor', 'both'
        axis='both',         # 'x', 'y', 'both'
        color='gray',        # 線の色
        linestyle='--',      # '--', '-.', ':', '-'
        linewidth=0.7,       # 線の太さ
        alpha=0.7            # 透明度
    )

    # グラフを保存するか表示するかをpathの内容から判断。
    if path == None:
        plt.tight_layout()
        plt.show()
    else:        
        plt.tight_layout()
        plt.savefig(path, bbox_inches='tight', pad_inches=0.1)
        plt.show()

######################################################################################################################################################

# 棒グラフ
def Make_bar_plot(x, y_dict, title='', xlabel='', ylabel='', legend_bottom=False, ncol=2, path=None):
    '''
    棒グラフを作図し、コンソールに表示 or 指定したパスに保存。
    【引数】
    x[list]: x軸のデータを格納したリスト。
    y_dict[dict]: y軸のデータを格納した辞書。keyは凡例、valueはy軸のデータ。
    title[str]: グラフのタイトル。指定しない場合は空白。
    xlabel[str]: x軸のラベル。指定しない場合は空白。
    ylabel[str]: y軸のラベル。指定しない場合は空白。
    legend_bottom[bool]: 凡例をグラフの下部に表示するかどうか。Trueの場合は下部に表示、Falseの場合は通常位置に表示。指定しない場合はFalse。
    ncol[int]:凡例をグラフの下部に表示する場合の1行当たりの凡例件数。指定しない場合は2で設定。
    path[str]: グラフを保存するパス。指定しない場合はコンソールに表示。
    '''

    fig, ax = plt.subplots()

    # xの要素数に基づいてx軸の位置を設定。y_dictの要素数に基づいて棒の幅を設定。
    x_point = np.arange(len(x))  # X軸の位置
    group_num = len(y_dict)  # グループ数
    blank = 0.15  # 棒と棒の間のスペース
    width = (1.0-2*blank) / group_num  # 棒の幅

    # y_dictのkeyをループさせて、複数要素の棒グラフを1枚のグラフ内に描画。rectsは棒のオブジェクトを格納する辞書。
    rects = {}
    for i, key_y in enumerate(y_dict):
        rects[key_y] = ax.bar(x_point + (i - group_num/2 + 0.5) * width, y_dict[key_y], width, label=key_y)
    # rectsは辞書の値がリストになっているので、すべての棒のオブジェクトを1つのリストにまとめる。
    all_rects = [rect for rects in rects.values() for rect in rects]

    # 棒の上に値を表示するためのループ。all_rectsはすべての棒のオブジェクトを格納したリスト。
    for rect in all_rects:
        height = rect.get_height()
        ax.annotate(f'{height}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 上に3px
                    textcoords="offset points",
                    ha='center', va='bottom')

    # グラフのタイトル、軸ラベルを設定。凡例も表示。
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if legend_bottom:
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.11), ncol=ncol, fontsize=8)
    else:
        plt.legend(fontsize=8)

    # グリッドを表示。グリッドのスタイルは、線の色を灰色、線のスタイルを点線、線の太さを0.7、透明度を0.7に設定。
    plt.grid(
        True,                # グリッド表示
        which='both',        # 'major', 'minor', 'both'
        axis='y',            # 'x', 'y', 'both'
        color='gray',        # 線の色
        linestyle='--',      # '--', '-.', ':', '-'
        linewidth=0.7,       # 線の太さ
        alpha=0.7            # 透明度
    )

    # グラフを保存するか表示するかをpathの内容から判断。
    if path == None:
        plt.tight_layout()
        plt.show()
    else:        
        plt.tight_layout()
        plt.savefig(path, bbox_inches='tight', pad_inches=0.1)
        plt.show()

######################################################################################################################################################

# ヒストグラム
def Make_hist_plot(x_dict, title='', x_lim=None, y_lim=None, x_label='', legend_bottom=False, ncol=2, path=None, bin_width=None, bins=None, alpha=0.4, density=False, normed=False):
    '''
    ヒストグラムを作図し、コンソールに表示 or 指定したパスに保存。
    【引数】
    x_dict[dict]: ヒストグラムのデータを格納した辞書。keyは凡例、valueはヒストグラムのデータ。
    title[str]: グラフのタイトル。指定しない場合は空白。
    x_lim[tuple]: x軸の範囲を指定するタプル。（最小値, 最大値）の形式。指定しない場合は自動で設定。
    y_lim[tuple]: y軸の範囲を指定するタプル。（最小値, 最大値）の形式。指定しない場合は自動で設定。
    x_label[str]: x軸のラベル。指定しない場合は空白。
    legend_bottom[bool]: 凡例をグラフの下部に表示するかどうか。Trueの場合は下部に表示、Falseの場合は通常位置に表示。指定しない場合はFalse。
    ncol[int]:凡例をグラフの下部に表示する場合の1行当たりの凡例件数。指定しない場合は2で設定。
    path[str]: グラフを保存するパス。指定しない場合はコンソールに表示。
    bin_width[int]: ヒストグラムのビンの幅。指定しない場合は自動でビンの数を設定。
    bins[int or list]: ヒストグラムのビンの数またはビンのエッジを指定するリスト。bin_widthが指定されている場合は無視される。指定しない場合は自動でビンの数を設定。
    alpha[float]: ヒストグラムの透明度。0から1の範囲で指定。指定しない場合は0.4。
    density[bool]: ヒストグラムを確率密度で表示するかどうかを指定するブール値。Trueの場合は確率密度、Falseの場合はカウントで表示。指定しない場合はFalse。
    normed[bool]: ヒストグラムを確率[%]で表示するかどうかを指定するブール値。Trueの場合は確率[%]、Falseの場合はカウントで表示。densityがTrueの場合はnormedは無視される。指定しない場合はFalse。
    '''

    # xの要素数に基づいてx軸の位置を設定。y_dictの要素数に基づいて棒の幅を設定。
    x_num_max = max([len(x_dict[key_x]) for key_x in x_dict])
    x_max = max([max(x_dict[key_x]) for key_x in x_dict])
    x_min = min([min(x_dict[key_x]) for key_x in x_dict])

    # ヒストグラムのビンの数またはエッジを設定。bin_widthが指定されている場合はbin_widthに基づいてビンのエッジを設定。bin_widthが指定されていない場合はbinsに基づいてビンの数またはエッジを設定。どちらも指定されていない場合は、データの長さに基づいて自動でビンの数を設定。
    if (bin_width == None) and (bins == None):
        bins=int(1+np.log2(x_num_max))
    elif (bin_width != None):
        bins = range(int(x_min()), int(x_max())+bin_width, bin_width)
    else:
        pass
    
    # ヒストグラムの表示方法をdensityとnormedの値に基づいて設定。
    if density == True:
        plt.ylabel('確率密度')
        for key_x in x_dict:
            plt.hist(x_dict[key_x], bins=bins, density=True, alpha=alpha, label=key_x)
    elif (density == False) and (normed == True):
        plt.ylabel('確率[%]')
        for key_x in x_dict:
            weights = np.ones(len(x_dict[key_x])) / float(len(x_dict[key_x]))
            plt.hist(x_dict[key_x], bins=bins, weights=weights, alpha=alpha, label=key_x)
    else:
        plt.ylabel('カウント')
        for key_x in x_dict:
            plt.hist(x_dict[key_x], bins=bins, alpha=alpha, label=key_x)
    
    # グラフのタイトル、軸ラベルを設定。凡例も表示。
    plt.title(title)
    plt.xlabel(x_label)
    if legend_bottom:
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.11), ncol=ncol, fontsize=8)
    else:
        plt.legend(fontsize=8)

    # x_limとy_limがNoneでない場合は、グラフの範囲を設定。
    if x_lim is not None:
        plt.xlim(x_lim[0], x_lim[1])
    if y_lim is not None:
        plt.ylim(y_lim[0], y_lim[1])

    # グリッドを表示。グリッドのスタイルは、線の色を灰色、線のスタイルを点線、線の太さを0.7、透明度を0.7に設定。
    plt.grid(
        True,                # グリッド表示
        which='both',        # 'major', 'minor', 'both'
        axis='y',            # 'x', 'y', 'both'
        color='gray',        # 線の色
        linestyle='--',      # '--', '-.', ':', '-'
        linewidth=0.7,       # 線の太さ
        alpha=0.7            # 透明度
    )

    # グラフを保存するか表示するかをpathの内容から判断。
    if path == None:
        plt.tight_layout()
        plt.show()
    else:        
        plt.tight_layout()
        plt.savefig(path, bbox_inches='tight', pad_inches=0.1)
        plt.show()


