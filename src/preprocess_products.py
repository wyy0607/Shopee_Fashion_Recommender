"""This module is to process product data for recommendation"""
import sys
import logging.config
from typing import List

import pandas as pd

logger = logging.getLogger(__name__)


def get_product_features(input_path: str, columns: List[str]) -> pd.DataFrame:
    """
    Get features from product data, remove rows with missing values, and reset index

    Args:
        input_path (`str`): input path to the product data
        columns (:obj:`list` of `str`): list of column names

    Returns:
        kept_data (:obj:`pandas.DataFrame`): pandas dataframe
    """
    # read data
    try:
        data = pd.read_csv(input_path, index_col=False)
    except FileNotFoundError:
        logger.error("No such file or directory to load product data. Please try again.")
        sys.exit(1)
    else:
        logger.info("Product data is successfully loaded.")
    # acquire columns, drop na, and reset index
    try:
        kept_data = data[columns].dropna().reset_index(drop=True)
    except KeyError:
        logger.error("At least one of column in provided `columns` "
                     "is not included in provided data")
        sys.exit(1)
    else:
        logger.info("Columns are successfully acquired from the product data.")

    return kept_data


def get_aggregated_features(data: pd.DataFrame, group_by: List[str], cols: List[str],
                            agg_cols: List[str], agg_funs: List[str]) -> pd.DataFrame:
    """
    Aggregate product data so that each row represents a unique product

    Args:
        data (:obj:`pandas.DataFrame`): pandas dataframe
        group_by (:obj:`list` of `str`): list of column names for group by
        cols (:obj:`list` of `str`): list of column names to be aggregated
        agg_cols (:obj:`list` of `str`): list of column names for aggregated columns
        agg_funs: (:obj:`list` of `str`): list of aggregation functions to perform

    Returns:
        agg_df (:obj:`pandas.DataFrame`): pandas dataframe with aggregated features
    """
    # check if input data is a pandas dataframe
    if not isinstance(data, pd.DataFrame):
        logger.error("Input `data` is not a pandas DataFrame.")
        sys.exit(1)
    # map columns to be aggregated to aggregation functions
    if len(cols) != len(agg_funs):
        logger.error("Input `cols` and input `agg_funs` have differnent length.")
        sys.exit(1)
    else:
        aggregation_dict = dict(zip(cols, agg_funs))
    # map columns to be aggregated to aggregated column names
    if len(cols) != len(agg_cols):
        logger.error("Input `cols` and input `agg_cols` have differnent length.")
        sys.exit(1)
    else:
        columns_dict = dict(zip(cols, agg_cols))
    # aggregate data with no duplicates
    try:
        agg_df = data.groupby(group_by, as_index=False) \
            .agg(aggregation_dict) \
            .rename(columns=columns_dict) \
            .drop_duplicates(group_by[0])
    except KeyError:
        logger.error("At least one of column in provided `group_by` "
                     "or `cols` is not included in provided data")
        sys.exit(1)
    else:
        logger.info("Data is successfully aggregated.")

    return agg_df


def save_product_data(data: pd.DataFrame, output_path: str) -> None:
    """
    Save processed product data
    Args:
        data(:obj:`pandas.DataFrame`): pandas dataframe
        output_path(`str`): path to output file

    Returns:
        None
    """
    # save product data to given output path
    try:
        data.to_csv(output_path, index=False)
    except FileNotFoundError:
        logger.error("No such directory to save product data. Please try again.")
    else:
        logger.info("Processed product data is successfully saved to given output path")
