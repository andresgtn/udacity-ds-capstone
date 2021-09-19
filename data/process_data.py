import pandas as pd
import numpy as np

def minMaxScaler(numArr):
    minx = np.min(numArr)
    maxx = np.max(numArr)
    numArr = (numArr - minx) / (maxx - minx)
    return numArr

def et_pipeline(preprocessed_data_path='data/clean_marina.csv',
                raw_data_path='data/raw_marina.csv'):
    # data to be cleaned
    model_df = pd.read_csv(preprocessed_data_path, index_col='identifier')
    model_df.sort_values(by=['price'], inplace=True)

    # keep this static, used to see summarized results,
    # contains the same base as marina but unmodified
    base_df = model_df.copy()

    # import original raw data to see full results at the end
    raw_df = pd.read_csv(raw_data_path, index_col=0)

    # transform data and prepare it for model
    # size
    model_df['size'] = minMaxScaler(pd.qcut(model_df['size'], 20, labels=False, duplicates='drop').values)
    # beds
    model_df['beds'] = minMaxScaler(model_df['beds'])
    # baths
    model_df['baths'] = minMaxScaler(model_df['baths'])
    # price
    model_df['price'] = minMaxScaler(pd.qcut(model_df['price'], 20, labels=False, duplicates='drop').values)

    # one-hot encode
    model_df = pd.get_dummies(model_df, prefix=['type'], columns=['type'], drop_first=True)

    # drop location, as it is ignored in the model for now
    model_df.drop(columns=['location'], inplace=True)

    return model_df, base_df, raw_df
