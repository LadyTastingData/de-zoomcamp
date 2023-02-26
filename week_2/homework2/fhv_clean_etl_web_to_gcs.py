from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint


@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    # if randint(0, 1) > 0:
    #     raise Exception

    df = pd.read_csv(dataset_url)
    return df


 @task(log_prints=True)
 def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns"""
    df.rename({'dropoff_datetime':'dropOff_datetime'}, axis='columns', inplace=True)
    df.rename({'PULocationID':'PUlocationID'}, axis='columns', inplace=True)
    df.rename({'DOLocationID':'DOlocationID'}, axis='columns', inplace=True)

    """Fix dtype issues"""
    df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
    df["dropOff_datetime"] = pd.to_datetime(df["dropOff_datetime"])

    # See https://pandas.pydata.org/docs/user_guide/integer_na.html
    df["PUlocationID"] = df["PUlocationID"].astype('Int64')
    df["DOlocationID"] = df["DOlocationID"].astype('Int64')
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df


@task()
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    #path = Path(f"data/fhv/{dataset_file}.parquet")
    #df.to_parquet(path, compression="gzip")
    path = Path(f"data/fhv_clean/{dataset_file}.csv.gz")
    df.to_csv(path, compression="gzip")
    return path


@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return
#from prefect_gcp.cloud_storage import GcsBucket
#gcp_cloud_storage_bucket_block = GcsBucket.load("zoom-gcs")

@flow()
def fhv_etl_web_to_gcs(year: int, month: int) -> None:
    """The main ETL function"""
    #year = 2020 #2020
    #month = 1
    dataset_file = f"fhv_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, dataset_file)
    write_gcs(path)

@flow()
def fhv_etl_parent_flow(
    months: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], year: int = 2019
):
    for month in months:
        fhv_etl_web_to_gcs(year, month)


if __name__ == "__main__":
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    year = 2019
    fhv_etl_parent_flow(year, months)

#if __name__ == "__main__":
#    etl_web_to_gcs()


