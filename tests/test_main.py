from fastapi.testclient import TestClient
from src.main import api

def test_root():
    with TestClient(api) as client:
        response = client.get('/')
        assert response.status_code == 404

def test_health():
    with TestClient(api) as client:
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json() == {'Status': 'Healthy'}

def test_single_predict_1():  # Unsuccessful Single Prediction: Missing Field
    with TestClient(api) as client:
        response = client.post('/single-predict', json={'HouseAge': 41.0, 'AveRooms': 6.98412698, 'AveBedrms': 1.02380952, 'Population': 322.0, 'AveOccup': 2.55555556, 'Latitude': 37.88, 'Longitude': -122.23})
        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == 'Field required'
        assert response.json()['detail'][0]['type'] == 'missing'

def test_single_predict_2():  # Unsuccessful Single Prediction: Invalid Type
    with TestClient(api) as client:
        response = client.post('/single-predict', json={'MedInc': 'Hello world', 'HouseAge': 41.0, 'AveRooms': 6.98412698, 'AveBedrms': 1.02380952, 'Population': 322.0, 'AveOccup': 2.55555556, 'Latitude': 37.88, 'Longitude': -122.23})
        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == 'Input should be a valid number, unable to parse string as a number'
        assert response.json()['detail'][0]['type'] == 'float_parsing'

def test_single_predict_3():  # Unsuccessful Single Prediction: Invalid MedInc
    with TestClient(api) as client:
        response = client.post('/single-predict', json={'MedInc': -8.3252, 'HouseAge': 41.0, 'AveRooms': 6.98412698, 'AveBedrms': 1.02380952, 'Population': 322.0, 'AveOccup': 2.55555556, 'Latitude': 37.88, 'Longitude': -122.23})
        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == 'Value error, MedInc Must Be Non-Negative'
        assert response.json()['detail'][0]['type'] == 'value_error'

def test_single_predict_4():  # Unsuccessful Single Prediction: Invalid Latitude
    with TestClient(api) as client:
        response = client.post('/single-predict', json={'MedInc': 8.3252, 'HouseAge': 41.0, 'AveRooms': 6.98412698, 'AveBedrms': 1.02380952, 'Population': 322.0, 'AveOccup': 2.55555556, 'Latitude': 200.0, 'Longitude': -122.23})
        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == 'Value error, Latitude Must Be Between -90 and 90'
        assert response.json()['detail'][0]['type'] == 'value_error'

def test_single_predict_5():  # Unsuccessful Single Prediction: Invalid Longitude
    with TestClient(api) as client:
        response = client.post('/single-predict', json={'MedInc': 8.3252, 'HouseAge': 41.0, 'AveRooms': 6.98412698, 'AveBedrms': 1.02380952, 'Population': 322.0, 'AveOccup': 2.55555556, 'Latitude': 37.88, 'Longitude': -200.0})
        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == 'Value error, Longitude Must Be Between -180 and 180'
        assert response.json()['detail'][0]['type'] == 'value_error'

def test_single_predict_6():  # Successful Single Prediction
    with TestClient(api) as client:
        response = client.post('/single-predict', json={'MedInc': 8.3252, 'HouseAge': 41.0, 'AveRooms': 6.98412698, 'AveBedrms': 1.02380952, 'Population': 322.0, 'AveOccup': 2.55555556, 'Latitude': 37.88, 'Longitude': -122.23})
        assert response.status_code == 200

def test_multiple_predict_1():  # Unsuccessful Multiple Prediction: Missing Field
    with TestClient(api) as client:
        response = client.post('/multiple-predict', json={'houses': [{'HouseAge': 41.0, 'AveRooms': 6.98412698, 'AveBedrms': 1.02380952, 'Population': 322.0, 'AveOccup': 2.55555556, 'Latitude': 37.88, 'Longitude': -122.23}, {'MedInc': 7.2574, 'HouseAge': 30.0, 'AveRooms': 5.86957656, 'AveBedrms': 1.07539683, 'Population': 500.0, 'AveOccup': 3.43209876, 'Latitude': 36.78, 'Longitude': -121.23}]})
        assert response.json()['detail'][0]['msg'] == 'Field required'
        assert response.json()['detail'][0]['type'] == 'missing'

def test_multiple_predict_2():  # Unsuccessful Multiple Prediction: Invalid Type
    with TestClient(api) as client:
        response = client.post('/multiple-predict', json={'houses': [{'MedInc': 'Hello world', 'HouseAge': 41.0, 'AveRooms': 6.98412698, 'AveBedrms': 1.02380952, 'Population': 322.0, 'AveOccup': 2.55555556, 'Latitude': 37.88, 'Longitude': -122.23}, {'MedInc': 7.2574, 'HouseAge': 30.0, 'AveRooms': 5.86957656, 'AveBedrms': 1.07539683, 'Population': 500.0, 'AveOccup': 3.43209876, 'Latitude': 36.78, 'Longitude': -121.23}]})
        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == 'Input should be a valid number, unable to parse string as a number'
        assert response.json()['detail'][0]['type'] == 'float_parsing'

def test_multiple_predict_3():  # Unsuccessful Multiple Prediction: Invalid MedInc
    with TestClient(api) as client:
        response = client.post('/multiple-predict', json={'houses': [{'MedInc': -8.3252, 'HouseAge': 41.0, 'AveRooms': 6.98412698, 'AveBedrms': 1.02380952, 'Population': 322.0, 'AveOccup': 2.55555556, 'Latitude': 37.88, 'Longitude': -122.23}, {'MedInc': 7.2574, 'HouseAge': 30.0, 'AveRooms': 5.86957656, 'AveBedrms': 1.07539683, 'Population': 500.0, 'AveOccup': 3.43209876, 'Latitude': 36.78, 'Longitude': -121.23}]})
        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == 'Value error, MedInc Must Be Non-Negative'
        assert response.json()['detail'][0]['type'] == 'value_error'

def test_multiple_predict_4():  # Unsuccessful Multiple Prediction: Invalid Latitude
    with TestClient(api) as client:
        response = client.post('/multiple-predict', json={'houses': [{'MedInc': 8.3252, 'HouseAge': 41.0, 'AveRooms': 6.98412698, 'AveBedrms': 1.02380952, 'Population': 322.0, 'AveOccup': 2.55555556, 'Latitude': 200, 'Longitude': -122.23}, {'MedInc': 7.2574, 'HouseAge': 30.0, 'AveRooms': 5.86957656, 'AveBedrms': 1.07539683, 'Population': 500.0, 'AveOccup': 3.43209876, 'Latitude': 36.78, 'Longitude': -121.23}]})
        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == 'Value error, Latitude Must Be Between -90 and 90'
        assert response.json()['detail'][0]['type'] == 'value_error'

def test_multiple_predict_5():  # Unsuccessful Multiple Prediction: Invalid Longitude
    with TestClient(api) as client:
        response = client.post('/multiple-predict', json={'houses': [{'MedInc': 8.3252, 'HouseAge': 41.0, 'AveRooms': 6.98412698, 'AveBedrms': 1.02380952, 'Population': 322.0, 'AveOccup': 2.55555556, 'Latitude': 37.88, 'Longitude': -200}, {'MedInc': 7.2574, 'HouseAge': 30.0, 'AveRooms': 5.86957656, 'AveBedrms': 1.07539683, 'Population': 500.0, 'AveOccup': 3.43209876, 'Latitude': 36.78, 'Longitude': -121.23}]})
        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == 'Value error, Longitude Must Be Between -180 and 180'
        assert response.json()['detail'][0]['type'] == 'value_error'

def test_multiple_predict_6():  # Successful Multiple Prediction
    with TestClient(api) as client:
        response = client.post('/multiple-predict', json={'houses': [{'MedInc': 8.3252, 'HouseAge': 41.0, 'AveRooms': 6.98412698, 'AveBedrms': 1.02380952, 'Population': 322.0, 'AveOccup': 2.55555556, 'Latitude': 37.88, 'Longitude': -122.23}, {'MedInc': 7.2574, 'HouseAge': 30.0, 'AveRooms': 5.86957656, 'AveBedrms': 1.07539683, 'Population': 500.0, 'AveOccup': 3.43209876, 'Latitude': 36.78, 'Longitude': -121.23}]})
        assert response.status_code == 200