# Property Listings Recommender

# Definition

## Project Overview

Dubai Marina has over 100 buildings. Pricing and features vary depending on the building age, location and quality. At any given time, a property listing website will have a few thousand listing for rent and a few thousand for sale in an area like Marina, and around 100,000 listings for the entire city. People unfamiliar with an area will need to spend a while shifting through listings to be able to get an idea of the price ranges for each class of property, and more time picking out listings that meet specific criteria.  Yes, knowledge based recommendations are common for properties, but even a refined search can yield hundreds or thousands of options in a place like Dubai, proving overwhelming for a user. Having a tool that summarizes apartment classes by number of bedrooms and prices in a location such as Marina allows a user to more quickly determine whether this is the place for them or not. This tool agreggates all of the supply's statistics and presents them in a small table that a user can wrap his head around. Furthermore, it allows a user to get back a few top recommendations based on a knowledge-based search, and extends this to find similar properties using nearest-neighboors for any chosen property. The nearest neighboors are chosen such that an option in any specific building is presented only once per batch, allowing for serendipity by recommending buildings the user might not have heard of but which have apartments that fit the user's required parameters.

Current listing platforms do not present usable statistics for users to learn about price/features of areas in a digestable manner - we want the 30,000 feet view before zooming in. They also don't provide recommendations in a user friendly manner. A knowledge-based system requires some prior knowledge about a product from the user, but when a user wants to do a broad exploration, it is not the best tool; a summary table works best in combination with targeted recommendations provided in digestable batches. This tool was built as a result of dozens of conversations with new property investors and homebuyers and their struggles with selecting locations and learning about the different options available in the market.

This tool is easily extendable to cover the entire city, but we have focused on a single area (Dubai Marina) as scrapping data and creating a pipeline to clean it requieres extra manual work for each new location. The listing scrapper was created in collaboration with another person so I will not include it as part of this submission.

## Problem Statement

The goal is to present summary statistics about a particular community, and to provide recommendations that help users discover new buildings. The tasks involved are the following:
1. Scrap property listings from an online portal into a csv file (ignore photos)
2. Clean data: missing prices, incorrect sizes, standarize locations across duplicates, preprocess for model ingestion
3. Train a model 

## Metrics

# Analysis

## Data Exploration

## Exploratory Visualization

## Algorithms and Techniques

## Benchmark

# Methodology

## Data Preprocessing

## Implementation

## Refinement

# Results

## Model Evaluation and Validation

## Justification

# Conclusion

## Free-Form Visualization

## Reflection

## Improvement




To run locally, first open ```run.py``` and add ```app.run(host='0.0.0.0', port=3001, debug=True)``` at the bottom.
Then run ```$python3 run.py``` and copy the address show in the terminal to your local browser.

