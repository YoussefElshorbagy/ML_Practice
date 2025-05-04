# main.py
from src.components import data_ingestion

if __name__ == "__main__":
    obj = data_ingestion.DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    print(train_data, test_data)
