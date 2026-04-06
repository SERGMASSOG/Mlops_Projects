from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load import load_data

def run_pipeline(source: str, target: str) -> None:
    """
    Orchestrates the ETL pipeline: Extract, Transform, Load.
    Parameters:
        source (str): Input data source.
        target (str): Output destination.
    """
    print("Starting pipeline...")

    # Extract
    raw_data = extract_data(source)
    print("Data extracted.")

    # Transform
    clean_data = transform_data(raw_data)
    print("Data transformed.")

    # Load
    load_data(clean_data, target)
    print("Pipeline completed successfully.")
