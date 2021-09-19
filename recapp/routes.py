from recapp import app

import pandas as pd
import numpy as np
import json

from flask import Flask
from flask import render_template, request, jsonify
from sklearn.neighbors import NearestNeighbors

from data.process_data import et_pipeline
# import recommenders
from recommender.recommenders import show_k_uid, parametric_suggestions

# Read and preprocess data
model_df, base_df, raw_df = et_pipeline()
# listing stats to display on first webpage
stats_df = base_df[['size','beds', 'price']] \
                  .agg(['min', 'max', 'mean', 'std']).T
stats_by_beds_df = base_df.groupby('beds')[['price', 'size']] \
                          .agg(['min', 'max', 'mean'])

# instantiate and train model
# instantiate model
model = NearestNeighbors(n_neighbors=20)
# transform dataframe with train data into array
model_df_arr = model_df.to_numpy()
# fit model
model.fit(model_df_arr)

# dictionary mapping listing unique id to its position in the array
# to be used when calling the recommender
# {u_id: pos} {1720: 0}
listing_map = dict(zip(model_df.index.tolist(),
                   np.arange(0, len(model_df.index)).tolist()))
# reverse it
reverse_listing_map = {v:k for (k,v) in listing_map.items()}

# to render html dataframes
# Just define this once
#classes = 'w3-table w3-striped w3-border'
classes = 'table table-striped table-bordered table-hover table-sm'
def gen_dict(df, title):
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
        # define parameters
        model_params = {'k':5, 'model':model, 'base_X':base_df,
                      'X':model_df_arr, 'listing_map':listing_map,
                      'reverse_listing_map':reverse_listing_map}
        # generate suggestions
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

    # This will render the go.html Please see that file.
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
        # generate suggestions
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

    # This will render the go.html Please see that file.
    return render_template(
        'u_id.html',
        query=query,
        **d,
        identifier=identifier
    )
