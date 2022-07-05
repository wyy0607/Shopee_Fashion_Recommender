"""This module is to truncate review data for recommendation"""
import sys
import logging.config

import pandas as pd

logger = logging.getLogger(__name__)


def truncate_reviews(review_path: str, review_col: str,
                     product_path: str, product_col: str) -> pd.DataFrame:
    """Truncate df2 with df2_col only in df1_col

    Args:
        review_path (`str`): path to review data
        review_col (`str`): product id column name in review data
        product_path (`str`): path to product data
        product_col (`str`): product id column in product data

    Returns:
        review_data (:obj:`pandas.DataFrame`): truncated review data with only existing products
    """
    # read review data
    try:
        review_data = pd.read_csv(review_path, index_col=False)
    except FileNotFoundError:
        logger.error("No such file or directory to load review data. Please try again.")
        sys.exit(1)
    else:
        logger.info("Review data is successfully loaded.")

    # read product data
    try:
        product_data = pd.read_csv(product_path, index_col=False)
    except FileNotFoundError:
        logger.error("No such file or directory to load product data. Please try again.")
        sys.exit(1)
    else:
        logger.info("Product data is successfully loaded.")

    # truncate review data
    try:
        review_data = review_data[review_data[review_col].isin(product_data[product_col])]
    except KeyError:
        logger.error("Either `review_col` and/or `product_col` does not exist "
                     "in its corresponding data.")
        sys.exit(1)
    else:
        logger.info("Review data is successfully truncated.")

    return review_data


def save_truncated_review_data(data: pd.DataFrame, output_path: str) -> None:
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
