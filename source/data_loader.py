import pandas as pd

def load_dataset(path="../data/ayurvedic_dataset.csv"):
    """
    Loads the ayurvedic dataset from CSV.
    """
    df = pd.read_csv(path)
    return df
