""" This module is to test functions to preprocess reviews data """
import pandas as pd
import pytest

from src.preprocess_reviews import get_review_features


def test_get_review_features():
    """Test for getting review features"""
    # df_in = pd.read_csv("data/sample/sample_reviews.csv", index_col=False)
    df_true = pd.DataFrame([[4738517427, 3550379942, 4],
                            [4044625510, 3550379942, 4],
                            [3650759656, 3550379942, 4],
                            [4565004719, 7543788697, 4],
                            [3669255641, 7543788697, 4],
                            [2966695395, 7543788697, 4],
                            [4997399691, 9312209380, 4],
                            [4310700444, 9312209380, 4],
                            [4204349015, 9312209380, 4],
                            [4858045247, 5640404015, 4]],
                           index=pd.RangeIndex(start=0, stop=10, step=1),
                           columns=["cmtid", "itemid", "rating_star"])
    # compute test results
    df_results = get_review_features("data/sample/sample_reviews.csv",
                                     columns=["cmtid", "itemid", "rating_star"])

    # Test that the true and test are the same
    pd.testing.assert_frame_equal(df_true, df_results)


def test_get_review_features_invalid_input_path():
    """Test for getting review features with invalid input data path"""
    with pytest.raises(SystemExit) as err:
        get_review_features("data/sample/invalid_data.csv",
                            columns=["cmtid", "itemid", "rating_star"])
    assert err.type == SystemExit
    assert err.value.code == 1
