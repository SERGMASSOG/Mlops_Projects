import pandas as pd

def load_data(df: pd.DataFrame, target: str) -> None:
    """
    Load the transformed data into a target destination.
    Parameters:
        df (pd.DataFrame): Clean data.
        target (str): Path or connection string to the destination.
    """
    # Ejemplo: guardar en CSV
    df.to_csv(target, index=False)
    print(f"Data successfully saved to {target}")