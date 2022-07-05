"""This module is to test functions to generate csr matrix for reviews"""

import numpy as np
import pytest

from src.get_csr_matrix import get_csr_matrix


def test_get_csr_matrix():
    """Test for generating csr matrix"""
    mat_true = np.array([[0, 4, 0, 4, 0, 0, 0, 4, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
                         [4, 0, 4, 0, 0, 0, 4, 0, 0, 0],
                         [0, 0, 0, 0, 4, 4, 0, 0, 0, 4]])
    mat_results = get_csr_matrix("data/sample/sample_reviews.csv", "itemid",
                                 "cmtid", "rating_star")
    assert np.array_equiv(mat_results, mat_true)


def test_get_csr_matrix_invalid_review_path():
    """Test for getting csr matrix with invalid input review data path"""
    with pytest.raises(SystemExit) as err:
        get_csr_matrix("data/sample/invalid_reviews.csv", "itemid", "cmtid", "rating_star")
    assert err.type == SystemExit
    assert err.value.code == 1
