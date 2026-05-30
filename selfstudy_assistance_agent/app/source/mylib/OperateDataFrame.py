import pandas as pd
import itertools

######################################################################################################################################################

# データフレームを縦持ちから横持ちに変換
def Vertical_to_horizontal_df(df, primary_key_list, move_column_list, use_column_list):
    '''
    データフレームを指定したキーだけを主キーにして、それ以外のキーはカラムを複製・区別することで横持ちに変換する。
    【引数】
    df[pandas.DataFrame]：横持ちに変換するデータフレーム。
    primary_key_list[list]：変換後に主キーとして残すカラム名のリスト。
    move_column_list[list]：主キーからカラムに変換するカラム名のリスト。
    use_column_list[list]：変換で複製する対象のカラム名のリスト。
    【戻り値】
    df_horizontal[pandas.DataFrame]：横持ちに変換したデータフレーム。
    '''

    # 横持ちにするカラムの値の組み合わせを取得
    move_column_value_list = []
    for move_column in move_column_list:
        move_column_value_list.append([value for value in df[move_column].unique()])
    move_value_pattern_list = list(itertools.product(*move_column_value_list))
    
    for move_value_pattern_number, move_value_pattern in enumerate(move_value_pattern_list):
        # 横持ちにするカラムの組みわせに該当する部分だけをdfから抽出
        df_part = df.copy()
        for column_number, move_column in enumerate(move_column_list):
            df_part = df_part[df_part[move_column]==move_value_pattern[column_number]]
        df_part = df_part[primary_key_list+use_column_list].reset_index(drop=True)

        # カラム名の変更用の辞書作成
        column_rename_dict = {}
        # 元々のカラム名を辞書に格納
        for use_column in use_column_list:
            column_rename_dict[use_column] = use_column
        # 変更後のカラム名は、末尾に縦持ちにするカラム全て分の'_{カラム名}{値}'を付けていく（値部分は横持カラムの組み合わせの内容が該当）
        for move_column, move_value in zip(move_column_list, move_value_pattern):
            # '_{カラム名}'部分から"_code"を削除
            move_column_suffix = move_column.replace("_code", "")
            for use_column in use_column_list:
                column_rename_dict[use_column] = column_rename_dict[use_column]+f'_{move_column_suffix}{move_value}'
        # カラム名変更
        df_part = df_part.rename(columns=column_rename_dict)

        # 組み合わせが最初のパターンの場合はそれを戻り値のデータフレームの基準にする。
        if move_value_pattern_number == 0:
            df_horizontal = df_part.copy()
        else:
            df_horizontal = pd.merge(df_horizontal, df_part, on=primary_key_list)
        
    return df_horizontal

######################################################################################################################################################

# データフレーム内のコードに対応する内容を取得
def Code_to_content(df, code_column, code, content_column):
    """
    データフレーム内で指定したコード値に対応する内容を取得。
    【引数】
    df[pandas.DataFrame]：コードと内容を含むデータフレーム。
    code_column[str]：コードを含むカラム名。
    code[int]：内容を取得するコード値。数値型を想定するため、念のため整数型に変換。
    content_column[str]：内容を含むカラム名。複数行が該当する場合に備えて、最初の1行のみを取得。
    【戻り値】
    content[str]：指定したコードに対応する内容。
    """

    # codeが数値型でない場合に備えて、整数型に変換。
    code = int(code)

    # codeに対応する内容をデータフレームから取得。複数行該当する可能性があるため、最初の1行のみを取得。
    content = df[df[code_column] == code][content_column][:1].values[0]

    return content

######################################################################################################################################################

# データフレーム内の内容に対応するコード値を取得
def Content_to_code(df, content_column, content, code_column):
    """
    データフレーム内で指定したコード内容に対応するコード値を取得。
    【引数】
    df[pandas.DataFrame]：コードと内容を含むデータフレーム。
    content_column[str]：内容を含むカラム名。
    content[str]：コード内容。複数行が該当する場合に備えて、最初の1行のみを取得。
    code_column[str]：コードを含むカラム名。
    【戻り値】
    code[int]：指定した内容に対応するコード値。
    """

    # contentに対応するコード値をデータフレームから取得。複数行該当する可能性があるため、最初の1行のみを取得。
    code = df[df[content_column] == content][code_column][:1].values[0]

    # codeが数値型でない場合に備えて、整数型に変換。
    code = int(code)

    return code



