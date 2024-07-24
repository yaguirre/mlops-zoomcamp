# Homework

# Answers

## Q1. Install MLflow

Once you installed the package, run the command `mlflow --version` and check the output. What's the version that you have?

* mlflow, version 2.14.3

## Q2. Download and preprocess the data

Download the Green Taxi Trip Records dataset for January, February and March 2023 in parquet format and then execute this command

`python preprocess_data.py --raw_data_path <TAXI_DATA_FOLDER> --dest_path ./output`

How many files were saved to `OUTPUT_FOLDER?

* 4 (`dv.pkl`, `test.pkl`, `train.pkl`, `val.pkl`)

## Q3. Train a model with autolog

Modify the `train.py` script to enable **autologging** with MLflow, execute the script and then launch the MLflow UI to check that the experiment run was properly tracked.

What is the value of the `min_samples_split` parameter?

* 2 

## Q4. Launch the tracking server locally

Launch the tracking server on your local machine, Select a SQLite DB for the backend store and a folder called artifacts for the artifacts store. 

In addition to `backend-store-uri`, what else do you need to pass to properly configure the server?

* `default-artifact-root`

## Q5. Tune model hyperparameters

Modify the script `hpo.py` and make sure that the validation RMSE is logged to the tracking server for each run of the hyperparameters optimization. 

What's the best validation RMSE that you got?

* 5.335

## Q6. Promote the best model to the model registry

Promote the best model to the model registry. Update the `register_model.py` so that it selects the model with the lowest RMSE on the test set and registers it to the model registry

What is the test RMSE of the best model?

* 5.567