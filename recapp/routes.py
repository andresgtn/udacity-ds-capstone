from recapp import app # import instantiated Flask environment from __init__.py

import pandas as pd
import numpy as np
import json

from flask import Flask
from flask import render_template, request, jsonify
from sklearn.neighbors import NearestNeighbors

# import data pre-processor
from data.process_data import et_pipeline
# import recommenders
from recommender.recommenders import show_k_uid, parametric_suggestions

# Read and preprocess data
model_df, base_df, raw_df = et_pipeline()
# Define the listing stats to display on the home page for the user
stats_df = base_df[['size','beds', 'price']] \
                  .agg(['min', 'max', 'median', 'std']).T # replaced mean with median
stats_by_beds_df = base_df.groupby('beds')[['price', 'size']] \
                          .agg(['min', 'max', 'median']) # replaced mean with median

# instantiate and train model
# instantiate model
model = NearestNeighbors(n_neighbors=20)
# transform dataframe with train data into array
model_df_arr = model_df.to_numpy()
# fit model
model.fit(model_df_arr)

# create a dictionary mapping a listing unique id to its position in model_df_arr
# to be used when making recommendations by unique_id
# {u_id: pos} e.g. {1720: 0}
listing_map = dict(zip(model_df.index.tolist(),
                   np.arange(0, len(model_df.index)).tolist()))
# swith k-v pairs: k->v, v->k
reverse_listing_map = {v:k for (k,v) in listing_map.items()}

# Render html dataframes
# Define this just once
# classes = 'w3-table w3-striped w3-border'
classes = 'table table-striped table-bordered table-hover table-sm'
def gen_dict(df, title):
    ''' Generate dictionary required to render a dataframe as html

    INPUTS:
    df: dataframe to be rendered
    title: dataframe title

    OUTPUTS:
    dictionary with title and the dataframe to be rendered in html,
    showing only 5 entries
    '''
    return {'title': title,
            'table': df.head(5).to_html(classes=classes)
            }

# render index webpage
@app.route('/')
@app.route('/index')
def index():

    d = {'df1': gen_dict(base_df.sample(n=5), 'Sample Listings'),
         'df2': gen_dict(stats_df, 'Marina Listing Stats'),
         'df3': gen_dict(stats_by_beds_df, 'Stats by #bedrooms'),
         }

    return render_template('master.html', **d)

@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query')

    # split user parameters
    choices = query.split(',')

    # check if 3 choices where given
    if ((len(choices) == 3) ):
        choices = pd.to_numeric(choices)
        # define parameters to make recommendations
        model_params = {'k':5, 'model':model, 'base_X':base_df,
                      'X':model_df_arr, 'listing_map':listing_map,
                      'reverse_listing_map':reverse_listing_map}
        # generate suggestions - knowledge based
        suggestions = parametric_suggestions(base_df=base_df,
                    price=choices[0],
                    beds=choices[1],
                    size=choices[2],
                    **model_params)
    else:
        # return an empty dataframe
        suggestions = base_df.head(0)

    d = {'df1': gen_dict(base_df.sample(n=5), 'Sample Listings'),
         'df2': gen_dict(stats_df, 'Marina Listing Stats'),
         'df3': gen_dict(stats_by_beds_df, 'Stats by #bedrooms'),
         'df4': gen_dict(suggestions, 'Recommendations by parameters')
         }

    # This will render the go.html See that file.
    return render_template(
        'go.html',
        query=query,
        **d,
        choices=choices,
    )

@app.route('/u_id')
def u_id():
    # save user input in query
    query = request.args.get('id_query')
    # check if the query is valid
    if query.isnumeric():
        # split user parameters
        identifier = pd.to_numeric(query)
        # generate suggestions through nearest neighboors
        model_params = {'k':5, 'model':model, 'base_X':base_df,
                      'X':model_df_arr, 'listing_map':listing_map,
                      'reverse_listing_map':reverse_listing_map}
        suggestions = show_k_uid(identifier, **model_params)
    else:
        # return an empty dataframe
        suggestions = base_df.head(0)
        identifier = -1

    d = {'df1': gen_dict(base_df.sample(n=5), 'Sample Listings'),
         'df2': gen_dict(stats_df, 'Marina Listing Stats'),
         'df3': gen_dict(stats_by_beds_df, 'Stats by #bedrooms'),
         'df4': gen_dict(suggestions, 'Recommendations by listing')
         }

    # This will render the go.html - See that file.
    return render_template(
        'u_id.html',
        query=query,
        **d,
        identifier=identifier
    )
