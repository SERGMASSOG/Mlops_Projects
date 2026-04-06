import pandas as pd

def extract_data(source: str) -> pd.DataFrame:
    """
    Extract data from a given source.
    Parameters:
        source (str): Path or connection string to the data source.
    Returns:
        pd.DataFrame: Raw data extracted.
    """
    df = pd.read_csv(source)
    return df # Se puede modificar para que la extraccion sea de una base de datos u otro formato si es necesario.