import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.misc.exceptions import CustomException
from src.misc.logger import logging


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")         ## Paths where we will save data
    raw_data_path: str = os.path.join("artifacts", "data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        
        logging.info("Initiating data ingestion")

        try:
            df=pd.read_csv('notebook/data/stud.csv')

            logging.info("Read the dataset")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)      ## Create the artifacts folder if it doesn't already exist
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)                ## Save the full raw data in the path we set (Artifacts Directory)

            logging.info("Initiating Train_test_split")

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)              ## Train test Split
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)       ## Save Training data in the path we set (Artifacts Directory)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)         ## Save Testing data in the path we set (Artifacts Directory)

            logging.info("Completed Train_test_split and saved data splits. Data ingestion complete")

            return(
                self.ingestion_config.train_data_path,          ## Return the paths for the training and testing data
                self.ingestion_config.test_data_path
            )


        except Exception as e:
            raise CustomException(e, sys)


if __name__=="__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    print(train_data, test_data)