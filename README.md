# Property Listings Recommender

A property listing recommendation system which also provides summary statistics of a particular neighborhood to help users make informed decisions in a more efficient way.

It can be accessed via a [webapp](https://marina-dxb-listing-recommender.herokuapp.com/) or run locally (instructions below). Note that when accessing the webapp for the first time, it needs about 10 seconds to load, which will be fixed in a future version.

## To run locally

Open ```run.py``` and add ```app.run(host='0.0.0.0', port=3001, debug=True)``` at the bottom.
Then open a terminal, run ```$python3 run.py``` and copy the address show in the terminal to your local browser.

# Definition

## Project Overview

Dubai Marina has over 100 buildings. Pricing and features vary depending on the building age, location and quality. At any given time, a property listing website will have a few thousand listing for rent and a few thousand for sale in an area like Marina, and around 100,000 listings for the entire city. People unfamiliar with an area will need to spend a while shifting through listings to be able to get an idea of the price ranges for each class of property, and more time picking out listings that meet specific criteria.  Yes, knowledge based recommendations are common for properties, but even a refined search can yield hundreds or thousands of options in a place like Dubai, proving overwhelming for a user. Having a tool that summarizes apartment classes by number of bedrooms and prices in a location such as Marina allows a user to more quickly determine whether this is the place for them or not. This tool agreggates all of the supply's statistics and presents them in a small table that a user can wrap his head around. Furthermore, it allows a user to get back a few top recommendations based on a knowledge-based search, and extends this to find similar properties using nearest-neighboors for any chosen property. The nearest neighboors are chosen such that an option in any specific building is presented only once per batch, allowing for serendipity by recommending buildings the user might not have heard of but which have apartments that fit the user's required parameters.

Current listing platforms do not present usable statistics for users to learn about price/features of areas in a digestable manner - we want the 30,000 feet view before zooming in. They also don't provide recommendations in a user friendly manner. A knowledge-based system requires some prior knowledge about a product from the user, but when a user wants to do a broad exploration, it is not the best tool; a summary table works best in combination with targeted recommendations provided in digestable batches. This tool was built as a result of dozens of conversations with new property investors and homebuyers and their struggles with selecting locations and learning about the different options available in the market.

This tool is easily extendable to cover the entire city, but we have focused on a single area (Dubai Marina) as scrapping data and creating a pipeline to clean it requieres extra manual work for each new location. The listing scrapper was created in collaboration with another person so I will not include it as part of this submission.

## Problem Statement

The goal is to present summary statistics about a particular community, and to provide recommendations that help users discover new buildings. The tasks involved are the following:
1. Scrap property listings from online portals into a csv file, and clean the data.
2. Preprocess clean data for model ingestion
3. Train model: nearest neighboors
4. Create a webapp to serve the model and area summary statistics to users
5. Serve the model to the user through a webapp

## Metrics

I found no specific metrics to automatically test the results of the nearest neighboors algorithm - testing will be done by visually inspecting results and output validity by choosing different inputs from the dataset and determining if the outputs make sense.

# Analysis

## Algorithms and Techniques

The model used is [Sklearn's NearestNeighboors](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html) which as the page describes, is an unsupervised learner for implementing neighboor searches. This library was chosen rather than implementing the algorithm from scratch as was done during the course - sklearn has a simple interface, is well documented and maintained well.

# Methodology

## Data Preprocessing

Note. Step 1 in the Problem Statement section was a project in and of itself which is kept on a private repository and which I do not inted to make public at this stage as I will continue to build on it. However, I have added sample code so reviewers can see some of the work done there. It can be found in the data directory and in the file sample_preprocessing.py.

Data was collected from multiple sources, agreggated into a single csv file, cleaned and standarized. The fields used for the webapp are: listing identifier,type,size,beds,baths,price,location. The model uses a subset of these to find neighbors: size,beds,baths,price. An extension to this recommender will be to include location and give recommendations based on proximity to predetermined areas, for instance, apartments near downtown, or near certain schools. To do this, we will need to collect more data from other locations which is not something I have yet done.

## Implementation

The implementation can be split into three stages:
1. Data collection and post-processing
2. Model training and data formatting for user display
3. Webapp development

Data collection and preprocessing formed an extensive part of the project. Collecting online data and getting it into usable form was messy and required a lot of manual work, especially when websites change and you need to adjust the code collecting the data. Not all data is read perfectly, so some post processing needs to be done to prepare the data for the model.

For the webapp, it was interesting to learn how much one can reuse code from previous exercises as long as it is well documented and properly structured.  I took what we learned in the [World Bank](https://github.com/andresgtn/ud-worldbank-dashboard) project and repurposed the code to fit this project. I had to extend it but the basic skeleton helped me get started and save time.

# Results

## Program and User Flow

This section covers how the app is structured and how a user interacts with it.

run.py : launches the program through app, which is imported from the recapp directory

recapp:
__init__.py : instantiates a Flask environment named app and imports routes.py.

routes.py : imports the instantiated Flask app and handles control of the user interface and its interactions with it. It generates the required data and handles data preprocessing and model instantiation, and training. Caveat: the model is trained when the page is launched for the first time. A better way to do it would be to train the model offline once, save it and pass it to the program to speed up the launch. Launch currently takes about 10 seconds on the first run, but after that, inference runs fast.

On launch, the user will see two input fields at the top - one to generate suggestions based on [price, bedrooms, square footage], and another to generate suggestions based on a particular listing by its unique identifier. Below, three tables appear; the first shows a random sample of listings, the second provides a high-level summary of the area, and the third shows stats by the number of bedrooms. The first table helps the users start their search by giving them a few prompts. The other two help the user get a broad idea of what to expect from this particular community. The median is used instead of the mean as there are outliers that would skew the mean towards a higher value. E.g. even though the median price is 1.5m, there is one apartment priced at 49m.

Some questions that a user can answer by looking at the Listing Stats tables are:
- If I wanted a 3 bedroom in this area, what kind of budget should I have? The answer would be around 2.7m.
- If my budget is 2m, what is the max number of bedrooms could I afford? Between 2-3 bedrooms, and maybe a cheap 4br. 
- If I want a 2,500 Sqft 2-bedroom apartment, could I find any options here? The answer is yes, but I might not find too many options since the median size for a 2br is 1,350 sqft.

Some extensions to 'stats by #bedrooms' could be:
- Show a listing count for each row to give a sense of the number of options available.
- Calculate price/size as investors use this metric a lot.

Next, a user can choose to generate suggestions. It inputs a combination of [price, bedrooms, square footage] and a new table with recommendations shown right under the input fields. The first row corresponds to the closest match to the query, and the other five rows correspond to its nearest neighbors. Below that, the other three tables shown at launch are displayed to help the user with relevant information to complete new queries. If the user sees a listing she likes, she can copy the listing identifier and enter it into the second query field which returns the nearest neighbors of that particular listing. If a user wants to explore options without choosing a specific [price, bedrooms, square footage] combination, he can pick a listing identifier from the Sample Listings table and generate recommendations from it. If a user wants to generate a new batch of Sample Listings, all he has to do is reload the page.

If a user clicks Generate without providing any data into the fields, the program returns an empty set of recommendations but includes a table with random sample listings. The same happens if the user provides a combination of parameters or a listing identifier that does not match any listings.

The user interface is quite simple and work could be done to increase its usability. For instance, instead of having to copy and paste the listing identifier into the input field, a user should be able to just click on the identifier to generate recommendations. Also, a user should be able to generate new random listings by clicking on a button instead of having to reload the page. Furthermore, some styling of the figures could be added to separate values with commas and make them more human-readable. These are extensions for the next version.

## Model Evaluation and Validation

There is not much validation to be done other than inspecting the results visually and making sure they make sense. I work in the real estate industry so I can quickly browse through the results and see whether they make sense or not.

# Conclusion

## Reflection

During the nanodegree, we had the opportunity both to implement solutions from scratch and used libraries with algorithm implementations. I though about implementing the nearest neighboors algorithm from scraths as we did during the course, but decided against it as it made no sense to build from scratch something that already exists (sklearn). What I wanted to take out of this project was the ability to put together different components and make them work together. I tried doing this in the most efficient way by choosing to repurpose code and use third-party libraries where possible instead of building everything from scratch. There are some modifications that have to be done to make the part work together, but it saved a lot of time. Other parts of the project, like data collection and processing, had to be built from scratch entirely.

## Improvements

Major improvements can be done in to fronts:
1. User experience and application design
2. More neighboors data for better recommendations





