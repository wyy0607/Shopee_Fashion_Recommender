"""This module is to process review data for recommendation"""
import sys
import logging.config
from typing import List

import pandas as pd

logger = logging.getLogger(__name__)


def get_review_features(input_path: str, columns: List[str]) -> pd.DataFrame:
    """
        Get features from product data, remove rows with missing values, and reset index

        Args:
            input_path (`str`): input path to the review data
            columns (:obj:`list` of `str`): list of column names

        Returns:
            kept_data (:obj:`pandas.DataFrame`): pandas dataframe
        """
    # read data
    try:
        data = pd.read_csv(input_path, index_col=False)
    except FileNotFoundError:
        logger.error("No such file or directory to load review data. Please try again.")
        sys.exit(1)
    else:
        logger.info("Review data is successfully loaded.")
    # acquire columns, drop na, and reset index
    try:
        kept_data = data[columns].dropna().reset_index(drop=True)
    except KeyError:
        logger.error("At least one of column in provided `columns` "
                     "is not included in provided data")
        sys.exit(1)
    else:
        logger.info("Columns are successfully acquired from the review data.")

    return kept_data


def save_review_data(data: pd.DataFrame, output_path: str) -> None:
    """
        Save processed review data
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
        logger.error("No such directory to save review data. Please try again.")
    else:
        logger.info("Processed review data is successfully saved to given output path")
