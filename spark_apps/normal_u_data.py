"""Spark module for reading data."""

from time import time

import Path
import pandas as pd
import polars as pl
import tqdm


def main() -> None:
    """Main function reading u.data."""
    with Path.open("/opt/spark-data/ml-100k/u.data") as f:
        data = f.readlines()

    data_df = {"client_id": [], "movie_id": [], "rating": [], "timestamp": []}
    for line in tqdm.tqdm(data):
        split_line = line.split()
        data_df["client_id"].append(split_line[0])
        data_df["movie_id"].append(split_line[1])
        data_df["rating"].append(split_line[2])
        data_df["timestamp"].append(split_line[3])

    start_time = time()
    df_pd = pd.DataFrame.from_dict(data_df)
    end_time = time()
    print("Time to create Pandas  Dataframe in seconds:", end_time - start_time)
    start_time = time()
    df_pl = pl.from_dict(data_df)
    end_time = time()
    print("Time to create Polars  Dataframe in seconds:", end_time - start_time)

    start_time = time()
    df_pd_count = df_pd.groupby("rating")["rating"].count()
    end_time = time()
    print("Time to create Pandas Dataframe count in seconds:", end_time - start_time)
    print(df_pd_count.head())
    start_time = time()
    df_pl_count = df_pl.groupby("rating", maintain_order=True).count()
    end_time = time()
    print("Time to create Polars Dataframe count in seconds:", end_time - start_time)
    print(df_pl_count.head())
