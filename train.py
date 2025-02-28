import os
import joblib
import logging
from sklearn.datasets import fetch_california_housing
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.svm import SVR

logging.basicConfig(level=logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

def load_data():
    """Fetches Dataset and Splits Into Training and Test Sets"""

    data = fetch_california_housing()
    X, Y = data.data, data.target
    feature_names = data.feature_names

    logging.info(f'Features: {feature_names}')
    logging.info(f'Sample Data: {X[0]}, Target: {Y[0]}')

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.33, random_state = 42)
    return X_train, X_test, Y_train, Y_test

def build_pipeline():
    """Create ML Pipeline with Preprocessing and a SVR Model"""
    
    return make_pipeline(
        SimpleImputer(),
        RobustScaler(),
        SVR()
    )

def tune_hyperparameters(pipeline, X_train, Y_train, X_test, Y_test):
    "Tunes Hyperparameters Using GridSearchCV""" 

    param_grid = {
        'simpleimputer__strategy': ['mean', 'median'],
        'robustscaler__quantile_range': [(25.0, 75.0), (30.0, 70.0)],
        'svr__C': [0.1, 1.0],
        'svr__gamma': ['auto', 0.1],
    }

    grid_search = GridSearchCV(pipeline, param_grid = param_grid, n_jobs = -1, cv = 5, verbose = 1)
    grid_search.fit(X_train, Y_train)

    logging.info(f'Best Parameters: {grid_search.best_params_}')
    logging.info(f'Train R^2 Score: {grid_search.best_estimator_.score(X_train, Y_train):.3f}')
    logging.info(f'Test R^2 Score: {grid_search.best_estimator_.score(X_test, Y_test):.3f}')

    return grid_search.best_estimator_

def save_model(model, path):
    """Saves Trained Model to File"""

    joblib.dump(model, path)
    logging.info(f'Model Saved to {path}')

def load_model(path):
    """Loads Trained Model if Exists, else Returns None"""

    if os.path.exists(path):
        try:
            model = joblib.load(path)
            logging.info('Model Load Success')
            return model
        except Exception as e:
            logging.error(f'Model Load Fail: {e}')
            return None
        
    return None

def main():

    model_filename = 'model.pkl'
    model_path = os.path.join(os.getcwd(), model_filename)
    model = load_model(model_path)

    if model is None:
        X_train, X_test, Y_train, Y_test = load_data()
        pipeline = build_pipeline()
        model = tune_hyperparameters(pipeline, X_train, Y_train, X_test, Y_test)
        save_model(model, model_path)

if __name__ == '__main__':
    main()