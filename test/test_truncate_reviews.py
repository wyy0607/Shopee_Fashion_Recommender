"""This module is to test functions to truncate review data"""

import pandas as pd
import pytest

from src.truncate_reviews import truncate_reviews


def test_truncate_reviews():
    """Test for truncating review data"""
    # df_product_in = pd.read_csv("data/sample/sample_products.csv", index_col=False)
    # df_review_in = pd.read_csv("data/sample/sample_reviews.csv", index_col=False)
    df_true = pd.DataFrame([[202106134997399691, "2021-06-13", 4997399691, 9312209380,
                             130651949, "m*****3", 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0],
                            [202106134310700444, "2021-06-13", 4310700444, 9312209380,
                             130651949, "marynicolejucovelasquez", 4, 1, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0],
                            [202106134204349015, "2021-06-13", 4204349015, 9312209380,
                             130651949, "k*****z", 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0]],
                           index=pd.Int64Index([6, 7, 8], dtype="int64"),
                           columns=["pk_review", "date_collected", "cmtid", "itemid", "shopid",
                                    "author_username", "rating_star", "no_tag", "pos_good_quality",
                                    "pos_excellent_quality", "pos_very_accomodating",
                                    "pos_well_packaged", "pos_item_shipped_immediately",
                                    "pos_will_order_again", "neg_defective",
                                    "neg_did_not_receive_item", "neg_damaged_packaging",
                                    "neg_will_not_order_again", "neg_rude_seller",
                                    "neg_item_shipped_late", "neg_item_different_from_picture"])
    df_results = truncate_reviews("data/sample/sample_reviews.csv", "itemid",
                                  "data/sample/sample_products.csv", "product_itemid")
    pd.testing.assert_frame_equal(df_true, df_results)


def test_truncate_reviews_invalid_review_path():
    """Test for getting product features with invalid input review data path"""
    with pytest.raises(SystemExit) as err:
        truncate_reviews("data/sample/invalid_reviews.csv", "itemid",
                         "data/sample/sample_products.csv", "product_itemid")
    assert err.type == SystemExit
    assert err.value.code == 1
