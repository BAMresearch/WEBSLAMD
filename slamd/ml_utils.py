import pandas as pd


def concat(df_1, df_2):
    return pd.concat([df_1, df_2], ignore_index=True)


def from_list_of_dicts(list_of_dicts):
    return pd.DataFrame(list_of_dicts)
