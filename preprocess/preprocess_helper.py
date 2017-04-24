import pandas as pd
import preprocess_funcs

def preprocess_default(pathname):
    """
    Examples:
        >>> preprocess_default("data/train_sample_0.csv")
    """
    df = pd.read_csv(pathname)
    df = preprocess_funcs.add_times2categorical(df)
    df = preprocess_funcs.add_releaseyear(df)
    df = preprocess_funcs.add_ages2categorical(df)
    df = preprocess_funcs.drop_columns(df, ['ts_listen', 'release_date', 'user_id'])

    # test export!
    # df.to_csv("../data/testhaha.csv", index=False)

    return df

