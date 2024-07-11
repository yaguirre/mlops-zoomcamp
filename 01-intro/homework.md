# Homework

I followed the instructions on using "**Yellow** Taxi Trip Records" instead of Green ones

# Answers

## Q1. Downloading the Data

How many columns are there for January 2023 Data?

* 19

## Q2. Computing duration

What's the standard deviation of the trips duration in January?

* 42.594351241920904

## Q3. Dropping outliers

What fraction of the records left after dropping the outliers from `duration` variable

* 98.1220282212598

## Q4. One-hot encoding

Let's apply one-hot encoding to the pickup and dropoff location IDs. We'll use only these two features for our model.

* Turn the dataframe into a list of dictionaries (remember to re-cast the ids to strings - otherwise it will 
  label encode them)
* Fit a dictionary vectorizer 
* Get a feature matrix from it

What's the dimensionality of this matrix (number of columns)?

* 2

## Q5. Training a model

Now let's use the feature matrix from the previous step to train a model.

* Train a plain linear regression model with default parameters, where duration is the response variable
* Calculate the RMSE of the model on the training data

What's the RMSE on train?

* 7.64926195987998

## Q6. Evaluating the model

Now let's apply this model to the validation dataset (February 2023). 

What's the RMSE on validation?
* 7.811832638273232