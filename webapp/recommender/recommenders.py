import pandas as pd
from sklearn.neighbors import NearestNeighbors


#def show_k_uid(idx, k=5, model=model, base_X=base_df,
#               X=model_df_arr, listing_map=listing_map,
#               reverse_listing_map=reverse_listing_map):
def show_k_uid(idx, **model_params):
    '''Return n neighboors for a given entry in the original
    listing dataframe.

    Inputs
    idx: int: row in original dataframe to compare against,
              by original unique id
    model: sklearn.neighbors.NearestNeighbors: pre-trained model
    base_X: pandas dataframe: has pre-transformed data
    X: np array: base_X after pre-processing and in array form

    Returns
    dataframe: first entry is the reference listing; the rest are
    its k neighboors
    {'k':5, 'model':model, 'base_X':base_df,
                  'X':model_df_arr, 'listing_map':listing_map,
                  'reverse_listing_map':reverse_listing_map}
    '''
    k = model_params['k']
    model = model_params['model']
    base_X = model_params['base_X']
    X = model_params['X']
    listing_map = model_params['listing_map']
    reverse_listing_map = model_params['reverse_listing_map']



    # map idx encoded as unique is into positional index
    try:
        idx = listing_map[idx]
    except KeyError:
        #print('Listing does not exist')
        # retun an empty dataframe
        return base_X.head(0)

    # compute neighboring indices
    k_neighbors_idx = model.kneighbors(X[idx].reshape(1,-1))[1][0]
    # get neighbors from listing frame
    k_neighbors = base_X.iloc[k_neighbors_idx].copy()

    try:
        # drop initial selection if it appears in results
        k_neighbors.drop(reverse_listing_map[idx], inplace=True)
    except KeyError:
        #print('Initial choice not present in results.')
        pass


    # keep the first instance results by location,
    # to enforce breath of choice
    k_neighbors.drop_duplicates(subset=['location'], inplace=True)

    # append initial selection on top and return 5 other results
    return pd.concat([base_X.iloc[[idx]], k_neighbors], axis=0).head(k+1)

def parametric_suggestions(base_df, price, beds, size, **model_params):
#def parametric_suggestions(price= 2000000, beds=2, size=1500, base_df=base_df):
    '''Parametric recommender'''
    rough_suggestions = base_df.loc[(base_df.beds == beds)
                                     & ((base_df.price > price*0.93)
                                     & (base_df.price < price*1.07))
                                     & ((base_df['size'] > size*0.9)
                                     & (base_df['size'] < size*1.1))]
    if len(rough_suggestions) == 0:
        #print('No matching listings, with this set of choices.')
        # retun an empty dataframe
        return model_params['base_X'].head(0)
    else:
        idx = rough_suggestions.sample(1).index[0]
        #idx, k=5, model=model, base_X=base_df,
        #               X=model_df_arr, listing_map=listing_map,
        #               reverse_listing_map=reverse_listing_map)
        return show_k_uid(idx, **model_params)
