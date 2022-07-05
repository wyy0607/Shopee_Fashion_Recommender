"""This module is to generate recommendations"""
import logging.config
import sys

import pandas as pd
import numpy as np
import joblib

logger = logging.getLogger(__name__)


def recommend_items(k: int, item_col: str, product_path: str,
                    csr_mat_path: str, model_path: str) -> pd.DataFrame:
    """Get product info for neighbors found by model

    Args:
        k (`int`): number of recommendations
        item_col (`str`): column name for item id in product data
        product_path (`str`): path to the product data
        csr_mat_path (`str`): path to csr matrix
        model_path (`str`): path to the model

    Returns:
        recommendations (:obj:`pd.DataFrame`): pandas dataframe for recommendations
    """
    # load product data
    try:
        product_data = pd.read_csv(product_path, index_col=False)
    except FileNotFoundError:
        logger.error("No such file or directory to load product data. Please try again.")
        sys.exit(1)
    else:
        logger.info("Product data is successfully loaded.")
    # load csr matrix
    try:
        mat = np.load(csr_mat_path)
    except FileNotFoundError:
        logger.error("No such directory or file to load the csr matrix. Please try again.")
        sys.exit(1)
    else:
        logger.info("csr matrix is successfully loaded.")

    # load model
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        logger.error("No such file or directory to load model. Please try again.")
        sys.exit(1)
    else:
        logger.info("Fitted model is successfully loaded.")

    # map index to item id
    try:
        item_inv_mapper = dict(zip(list(range(len(np.unique(product_data[item_col])))),
                                   np.unique(product_data[item_col])))
    except KeyError:
        logger.error("Provided `item_col` is not in product data.")
        sys.exit(1)

    # construct pandas dataframe to store recommendations
    recommendations = pd.DataFrame(columns=["input_itemid", "rank"] + list(product_data.columns))

    # check k
    if not (str(k).isdigit() and k > 0):
        logger.warning("The input `k` is not a positive integer. k = 7 is used.")
        k = 7

    # get product info for each recommendation
    for i, items in enumerate(model.kneighbors(mat, return_distance=False)):
        for j in range(1, k+1):
            neighbor = items[j]
            # locate product info and add to recommendation dataframe
            product_info = product_data.loc[product_data[item_col] == item_inv_mapper[neighbor]] \
                .values.tolist()[0]
            recommendations.loc[j + k * i] = [item_inv_mapper[i], j] + product_info
    # reset index for recommendations
    recommendations = recommendations.reset_index(drop=True)

    logger.info("Recommendations are successfully obtained.")
    return recommendations


def save_recommendations(data: pd.DataFrame, output_path: str) -> None:
    """Save recommendations to given output path

    Args:
        data (:obj:`pd.DataFrame`): pandas dataframe
        output_path (`str`): output path to save recommendations

    """
    # save recommendations to given output path
    try:
        data.to_csv(output_path, index=False)
    except FileNotFoundError:
        logger.error("No such directory to save recommendations. Please try again.")
    else:
        logger.info("Recommendations are successfully saved to given output path")
