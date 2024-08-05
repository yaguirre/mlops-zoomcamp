import pickle
import mlflow
from mlflow.tracking import MlflowClient
from flask import Flask, request, jsonify

MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'
mlflow.set_tracking_uri("http://127.0.0.1:5000")

RUN_ID = 'c04e5f484e4142109de7d3107bdea86d'
logged_model = f'runs:/{RUN_ID}/model'
model = mlflow.pyfunc.load_model(logged_model)

def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride["PULocationID"], ride["DOLocationID"])
    features['trip_distance'] = ride['trip_distance']
    return features

def predict(features):
    preds = model.predict(features)
    return preds[0]

app = Flask('duration-prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()

    features = prepare_features(ride)
    pred = predict(features)

    result = {
        'duration': pred,
        'model_version': RUN_ID
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
