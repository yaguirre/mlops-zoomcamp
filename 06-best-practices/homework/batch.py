#!/usr/bin/env python
# coding: utf-8

import sys
import pickle
import pandas as pd
import os

def get_input_path(year, month):
    default_input_pattern = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    default_output_pattern = 's3://nyc-duration-prediction-alexey/taxi_type=fhv/year={year:04d}/month={month:02d}/predictions.parquet'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern.format(year=year, month=month)

def read_data(filename):
    s3_endpoint_url = os.getenv("S3_ENDPOINT_URL", "http://localhost:4566")
    
    if s3_endpoint_url:
        options = {
            "client_kwargs": {
                "endpoint_url": s3_endpoint_url
            }
        }
        
        df = pd.read_parquet(filename, storage_options=options)
    else:
        df = pd.read_parquet(filename)
        
    return df


def prepare_data(df, categorical):
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def save_data(df_result, filename):
    s3_endpoint_url = os.getenv("S3_ENDPOINT_URL", "http://localhost:4566")
    
    if s3_endpoint_url:
        options = {
            'client_kwargs': {
                'endpoint_url': s3_endpoint_url
            }
        }
        
        df_result.to_parquet(filename, engine='pyarrow', compression=None, index=False, storage_options=options)
        print(f"The dataframe was saved to S3 bucket as {filename}")
    else:
        df_result.to_parquet(filename, engine='pyarrow', compression=None, index=False,)
        print(f"The dataframe was saved locally as {filename}")
        
def main(year, month):
    input_file = get_input_path(year, month)
    output_file = get_output_path(year, month)
    
    categorical = ['PULocationID', 'DOLocationID']
    
    df_raw = read_data(input_file)
    df = prepare_data(df_raw, categorical)
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    
    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)
        
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)
    print('predicted mean duration:', y_pred.mean())
    
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred
    
    save_data(df_result, output_file)


if __name__ == "__main__":
    main(year=int(sys.argv[1]), month=int(sys.argv[2]))
