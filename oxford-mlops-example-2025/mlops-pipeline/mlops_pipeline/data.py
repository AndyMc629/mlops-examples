import os
import boto3
import pandas as pd
from io import StringIO
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_s3_path(path: str) -> bool:
    """
    Check if the provided path is an S3 URI.
    
    Args:
        path (str): The file path to check.
        
    Returns:
        bool: True if path is an S3 URI, False otherwise.
    """
    return path.startswith("s3://")

def read_csv_from_local(path: str) -> pd.DataFrame:
    """
    Read a CSV file from a local file system.
    
    Args:
        path (str): Local file path.
        
    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """
    if not os.path.isfile(path):
        logger.error(f"Local file not found: {path}")
        raise FileNotFoundError(f"Local file not found: {path}")

    logger.info(f"Reading local CSV file from: {path}")
    return pd.read_csv(path, delimiter=';', decimal=',')

def read_csv_from_s3(s3_path: str, aws_profile: str = None) -> pd.DataFrame:
    """
    Read a CSV file from an S3 bucket using boto3.
    
    Args:
        s3_path (str): S3 URI in the format s3://bucket/key
        aws_profile (str, optional): AWS profile to use. Defaults to None.
        
    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """
    parsed_url = urlparse(s3_path)
    bucket_name = parsed_url.netloc
    key = parsed_url.path.lstrip('/')

    session = boto3.Session(profile_name=aws_profile) if aws_profile else boto3.Session()
    s3 = session.client('s3')

    try:
        logger.info(f"Fetching file from S3: {s3_path}")
        obj = s3.get_object(Bucket=bucket_name, Key=key)
        data = obj['Body'].read().decode('utf-8')
        return pd.read_csv(StringIO(data), delimiter=';', decimal=',')
    except s3.exceptions.NoSuchKey:
        logger.error(f"The object {key} does not exist in bucket {bucket_name}.")
        raise
    except Exception as e:
        logger.error(f"An error occurred while reading from S3: {e}")
        raise

def read_csv_file(path: str, aws_profile: str = None) -> pd.DataFrame:
    """
    Determine the type of path (local or S3) and read the CSV accordingly.
    
    Args:
        path (str): File path, either local or S3.
        aws_profile (str, optional): AWS profile to use for S3 access. Defaults to None.
        
    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """
    if is_s3_path(path):
        return read_csv_from_s3(path, aws_profile)
    else:
        return read_csv_from_local(path)

# Example Usage
if __name__ == "__main__":
    file_path = "s3://mlops-pipeline-example/landing/bank.csv"  # Replace with your S3 path or local path
    try:
        df = read_csv_file(file_path)
        print(df.head())
    except Exception as e:
        logger.error(f"Failed to read CSV: {e}")