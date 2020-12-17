from app.bl.exc import FileFormatError
# from app.core.timer import timer


# @timer
def save_df(df, file, columns):
    file_format = None
    file = str(file)  # TODO temp workaround, refactor to use Path from pathlib
    if len(file.rsplit('.')) > 1:
        file_format = file.rsplit('.')[-1]

    if file_format == 'csv':
        df.to_csv(file, columns=columns, index=True)

    elif file_format == 'feather':
        df = df[columns]
        df.reset_index(inplace=True)
        df.to_feather(file)

    else:
        raise FileFormatError

    return
