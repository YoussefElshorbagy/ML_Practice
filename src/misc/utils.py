import os
import sys
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import r2_score

from src.misc.exceptions import CustomException
from src.misc.logger import logging


def save_object(file_path, obj):
    try:

        dir = os.path.dirname(file_path)
        os.makedirs(dir, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

        logging.info(f"Saved pickle object at: {file_path}")

    except Exception as e:
        raise CustomException(e, sys)
    

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

        logging.info(f"Loaded pickle object from {file_path}")

    except Exception as e:
        raise CustomException(e, sys)
    
def train_evaluate_models(x_train, y_train, x_test, y_test, models, params):
    try:

        train_report = {}
        test_report = {}
        best_params = {}

        for i in range(len(models)):
            model_name = list(models.keys())[i]
            logging.info(f'Training model: {model_name}')

            model = list(models.values())[i]
            model_params = params[list(models.keys())[i]]

            # search = GridSearchCV(model, model_params, cv=3)          ## Initializes and fits a Grid Search with 3-fold cross-validation on the training set to find the best hyperparameters.
            search = RandomizedSearchCV(model, model_params, cv=3)
            search.fit(x_train, y_train)

            best_model_params = search.best_params_                     ## Save the best parameters in a variable
            best_params[model_name] = best_model_params                 ## Save the variable in the dict for future use
            model.set_params(**best_model_params)                       ## Set the best parameters found by GridSearchCV/RandomizedSearchCV
            model.fit(x_train, y_train)                                 ## Retrains the model on the full training data with those best parameters.

            train_pred = model.predict(x_train)                         ## Use the model to predict on train data
            test_pred = model.predict(x_test)                           ## Use the model to predict on test data

            train_model_score = r2_score(y_train, train_pred)
            test_model_score = r2_score(y_test, test_pred)

            train_report[model_name] = train_model_score
            test_report[model_name] = test_model_score

        return (
            train_report,
            test_report,
            best_params,
        )

    except Exception as e:
        raise CustomException(e, sys)