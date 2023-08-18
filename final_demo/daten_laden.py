import os
import pandas as pd

def list_csv_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.csv')]

def load_csv_file(file_path):
    return pd.read_csv(file_path)
