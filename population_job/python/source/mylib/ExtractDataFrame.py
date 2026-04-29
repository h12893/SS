import pandas as pd



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



