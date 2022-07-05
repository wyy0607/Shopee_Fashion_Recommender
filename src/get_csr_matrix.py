"""This module is to get csr matrix for ratings"""
import logging.config
import sys

import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix


logger = logging.getLogger(__name__)


def get_csr_matrix(review_data_path: str, item_col: str,
                   user_col: str, rating_col: str) -> np.ndarray:
    """Get sparse matrix for recommendation

    Args:
        review_data_path (`str`): path to review data
        item_col (`str`): column name for item id in review data
        user_col (`str`): column name for user id in review data
        rating_col (`str`): column name for ratings in review data

    Returns:
        mat (:obj:`numpy.ndarray`): numpy ndarray
    """
    # load review data
    try:
        review_data = pd.read_csv(review_data_path, index_col=False)
    except FileNotFoundError:
        logger.error("No such file or directory to load product data. Please try again.")
        sys.exit(1)
    else:
        logger.info("Review data is successfully loaded.")

    # pivot review data to get rating per user per item, fill na with 0
    try:
        pivot_df = review_data.pivot_table(index=item_col, columns=user_col,
                                           values=rating_col, fill_value=0)
    except KeyError:
        logger.error("At least one of provided columns is not in provided data")
        sys.exit(1)
    else:
        logger.info("Review data is successfully pivoted")
    # transform csr matrix to numpy ndarray
    mat = csr_matrix(pivot_df).toarray()
    return mat


def save_csr_matrix(mat: np.ndarray, output_path: str) -> None:
    """Save csr matrix

    Args:
        mat (:obj:`numpy.ndarray`): csr matrix
        output_path (`str`): output path to save csr matrix

    Returns:
        None
    """
    # save the array
    try:
        np.save(output_path, mat)
    except FileNotFoundError:
        logger.error("No such directory to save the results. Please try again.")
        sys.exit(1)
    else:
        logger.info("csr matrix is successfully saved.")
