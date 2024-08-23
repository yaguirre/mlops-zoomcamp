from batch import get_input_path, get_output_path, read_data
from datetime import datetime
import pandas as pd
import os

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def save_dataframe():
    data = [
            (None, None, dt(1, 1), dt(1, 10)),
            (1, 1, dt(1, 2), dt(1, 10)),
            (1, None, dt(1, 2, 0), dt(1, 2, 59)),
            (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
        ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)

    s3_endpoint_url = os.getenv("S3_ENDPOINT_URL", "http://localhost:4566")
    options = {"client_kwargs": {"endpoint_url": s3_endpoint_url}}

    input_file = get_input_path(2023, 1)
    df.to_parquet(input_file, engine="pyarrow", compression=None, index=False, storage_options=options,)

    print(f"File saved to S3 as {input_file}")

def test_saved_data(year, month):
    print("Checking saved data...")
    output_path = get_output_path(year, month)
    s3_endpoint_url = os.getenv("S3_ENDPOINT_URL", "http://localhost:4566")
    
    options = {"client_kwargs": {"endpoint_url": s3_endpoint_url}}
    
    # print(output_path)
    df = pd.read_parquet(output_path, storage_options=options)

    sum = df.predicted_duration.sum()
    print(f"The predicted duration sum is: {sum} ")
    
    
if __name__ == "__main__":
    print(50*'=','SAVE DATA FRAME TEST', 50*'=')
    save_dataframe()
    print(120*'=','\n')
    print(50*'=','READ DATAFRAME & VERIFY SUM OF PREDICTION', 50*'=')
    test_saved_data(2023, 1)
    print(130*'=','\n')
    
    

