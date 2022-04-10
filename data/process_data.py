import pandas as pd
import numpy as np

def minMaxScaler(numArr):
    ''' A minmaxscaler to transform features by scaling each
    feature to a given range. Improves model performance.

    INPUTS:
    numArr: a datframe column to be scaled

    OUTPUTS:
    numArr: the scaled column
    '''
    minx = np.min(numArr)
    maxx = np.max(numArr)
    numArr = (numArr - minx) / (maxx - minx)
    return numArr

def et_pipeline(preprocessed_data_path='data/clean_marina.csv',
                raw_data_path='data/raw_marina.csv'):
    ''' Extract-transform pipeline to prepare listing data for
    the model while keeping a copy of the full data set to present
    summary statistics.

    INPUTS
    preprocessed_data_path: path to preprocessed and cleaned data
    raw_data_path: path to raw data which contains listing titles

    OUTPUTS
    model_df: dataframe to be used for learning in the model
    base_df: dataframe with preprocessed data for summary statistics
    raw_df: original data which contains listing titles
    '''
    # data to be cleaned and processed for the model to ingest
    model_df = pd.read_csv(preprocessed_data_path, index_col='identifier')
    model_df.sort_values(by=['price'], inplace=True)

    # keep an unmodified version of the data to present summary statistics
    # which include building names
    base_df = model_df.copy()

    # import original raw data to see full results
    # which include listing titles
    raw_df = pd.read_csv(raw_data_path, index_col=0)

    # transform data and prepare it for the model
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
