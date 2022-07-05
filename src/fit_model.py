"""This module is to build recommendation system"""
import logging.config
import sys

import numpy as np
from sklearn.neighbors import NearestNeighbors
import joblib

logger = logging.getLogger(__name__)


def fit_model(k: int, metric: str, csr_mat_path: str, output_path: str) -> None:
    """Fit a KNN model for recommendations

    Args:
        k (`int`): number of neighbors to use
        metric (`str`): distance metric used for finding neighbors
        csr_mat_path (`str`): path to csr matrix
        output_path (`str`): output path to save model

    Returns:
        None
    """
    # load csr matrix
    try:
        mat = np.load(csr_mat_path)
    except FileNotFoundError:
        logger.error("No such directory or file to load the csr matrix. Please try again.")
        sys.exit(1)
    else:
        logger.info("csr matrix is successfully loaded.")

    # check input k
    if not (str(k).isdigit() and k > 0):
        logger.error("The input k has to be a positive integer.")
        raise ValueError("The input k has to be a positive integer.")

    # fit model
    try:
        model = NearestNeighbors(n_neighbors=k+1, algorithm="brute", metric=metric)
    except ValueError:
        logger.error("The input metric is not valid")
        sys.exit(1)
    model.fit(mat)

    # save model
    try:
        joblib.dump(model, output_path)
    except FileNotFoundError:
        logger.error("No such directory to save the model. Please try again.")
        sys.exit(1)
    else:
        logger.info("KNN model is successfully loaded.")
