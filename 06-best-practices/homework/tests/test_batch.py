from datetime import datetime
import batch
import pandas as pd
from pprint import pprint
from deepdiff import DeepDiff


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def test_prepare_data():
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    
    actual_features = batch.prepare_data(df, columns[0:2]).to_dict(orient='records')
    
    expected_data = [
        ('-1', '-1', dt(1, 1), dt(1, 10), 9.0),
        ('1', '1', dt(1, 2), dt(1, 10), 8.0),
    ]
    
    expected_features = pd.DataFrame(expected_data, columns=columns + ['duration']).to_dict(orient='records')
    
    diff = DeepDiff(actual_features, expected_features)
    
    if diff:
        print('\n\ndiff = ')
        pprint(diff)
    
    assert actual_features == expected_features
    print(f"\n\nTest passed, Expected DataFrame is: ")
    pprint(expected_features)