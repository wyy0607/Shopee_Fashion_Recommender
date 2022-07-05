""" This module is to test functions to preprocess products data """
import pandas as pd
import pytest

from src.preprocess_products import get_product_features, get_aggregated_features


def test_get_product_features():
    """Test for getting product features"""
    # df_in = pd.read_csv("data/sample/sample_products.csv", index_col=False)
    df_true = pd.DataFrame([[9440747987, "Zanzea Women Korean Casual Back Puff Sleeve Tops",
                             "Long Sleeves", 822.0, 46, 0, 2, 13, 5.0, 2],
                            [5452669710,
                             "Long Sleeve Blouse Long Sleeve Crop top Trendy Tops Loose Shirt "
                             "for Women Long Sleeve "
                             "Shirt Korean Style Tops Ulzzang Tops for Women T-Shirt Fashion "
                             "Women Clothes Casual Tops "
                             "Loose Tshirt Round Neck T Shirts",
                             "Long Sleeves", 398.0, 50, 1861, 137, 2680, 4.95, 275],
                            [4771111702,
                             "M-5XL Mens Cotton Linen Long Sleeve Yoga Button Down Shirts Summer "
                             "Cotton and Linen "
                             "Three-Quarter Sleeve Shirt Men's Linen plus Size Shirt Solid Color "
                             "Half Sleeves Korean "
                             "Style Top Fashion Short Sleeve Shirt",
                             "Top", 1120.0, 58, 41, 5, 402, 5.0, 11],
                            [3861115290,
                             "[COD Ready Stock] Women Blouse Korean Top Chiffon Puff Sleeve "
                             "Crop Top Blouse Floral "
                             "Croptop Long Sleeve T-Shirts Tops Square Collar Pleated Shirt Women",
                             "Crop Top", 452.0, 90, 13455, 2446, 134994, 4.89, 6453],
                            [8528691619,
                             "women button down knitted knit lettuce top strawberry floral "
                             "short sleeves "
                             "women bangkok korean B032",
                             "Short Sleeves", 299.0, 74, 666, 204, 7779, 4.92, 493],
                            [3590133563,
                             "Women's T-shirt Short Sleeve Round Neck Cotton 30% Solid Color  "
                             "Korean Fashion",
                             "Short Sleeves", 284.0, 27, 23, 1, 659, 5.0, 2],
                            [5560472579,
                             "LALUNA Korean Fashion Erich Basic Printed Floral Daily "
                             "Polo Tie Top 1104",
                             "Short Sleeves", 147.0, 7, 4, 5, 161, 5.0, 43],
                            [9312209380,
                             "7-color Korean version elegant retro Polo knit V-neck slim short "
                             "open navel Short Sleeve T-Shirt Top",
                             "Short Sleeves", 200.0, 26, 1161, 295, 9943, 4.88, 670]],
                           index=pd.RangeIndex(start=0, stop=8, step=1),
                           columns=["product_itemid", "product_name", "product_category",
                                    "product_price", "product_discount", "product_like_count",
                                    "product_comment_count", "product_views",
                                    "product_total_rating", "units_sold"])
    # compute test results
    df_results = get_product_features("data/sample/sample_products.csv",
                                      columns=["product_itemid", "product_name", "product_category",
                                               "product_price", "product_discount",
                                               "product_like_count", "product_comment_count",
                                               "product_views", "product_total_rating",
                                               "units_sold"])

    # Test that the true and test are the same
    pd.testing.assert_frame_equal(df_true, df_results)


def test_get_review_features_invalid_input_path():
    """Test for getting product features with invalid input data path"""
    with pytest.raises(SystemExit) as err:
        get_product_features("data/sample/invalid_data.csv",
                             columns=["product_itemid", "product_name", "product_category",
                                      "product_price", "product_discount",
                                      "product_like_count", "product_comment_count",
                                      "product_views", "product_total_rating", "units_sold"])
    assert err.type == SystemExit
    assert err.value.code == 1


def test_get_aggregated_features():
    """Test for getting aggregated product features"""
    df_in = pd.DataFrame([[9440747987, "Zanzea Women Korean Casual Back Puff Sleeve Tops",
                           "Long Sleeves", 822.0, 46, 0, 2, 13, 5.0, 2],
                          [5452669710,
                           "Long Sleeve Blouse Long Sleeve Crop top Trendy Tops Loose Shirt"
                           " for Women Long Sleeve "
                           "Shirt Korean Style Tops Ulzzang Tops for Women T-Shirt Fashion"
                           " Women Clothes Casual Tops "
                           "Loose Tshirt Round Neck T Shirts",
                           "Long Sleeves", 398.0, 50, 1861, 137, 2680, 4.95, 275],
                          [4771111702,
                           "M-5XL Mens Cotton Linen Long Sleeve Yoga Button Down Shirts"
                           " Summer Cotton and Linen "
                           "Three-Quarter Sleeve Shirt Men's Linen plus Size Shirt Solid"
                           " Color Half Sleeves Korean "
                           "Style Top Fashion Short Sleeve Shirt",
                           "Top", 1120.0, 58, 41, 5, 402, 5.0, 11],
                          [3861115290,
                           "[COD Ready Stock] Women Blouse Korean Top Chiffon Puff Sleeve"
                           " Crop Top Blouse Floral "
                           "Croptop Long Sleeve T-Shirts Tops Square Collar Pleated"
                           " Shirt Women",
                           "Crop Top", 452.0, 90, 13455, 2446, 134994, 4.89, 6453],
                          [8528691619,
                           "women button down knitted knit lettuce top strawberry floral"
                           " short sleeves "
                           "women bangkok korean B032",
                           "Short Sleeves", 299.0, 74, 666, 204, 7779, 4.92, 493],
                          [3590133563,
                           "Women's T-shirt Short Sleeve Round Neck Cotton 30% Solid Color"
                           "  Korean Fashion",
                           "Short Sleeves", 284.0, 27, 23, 1, 659, 5.0, 2],
                          [5560472579,
                           "LALUNA Korean Fashion Erich Basic Printed Floral Daily"
                           " Polo Tie Top 1104",
                           "Short Sleeves", 147.0, 7, 4, 5, 161, 5.0, 43],
                          [9312209380,
                           "7-color Korean version elegant retro Polo knit V-neck slim"
                           " short open navel Short Sleeve T-Shirt Top",
                           "Short Sleeves", 200.0, 26, 1161, 295, 9943, 4.88, 670]],
                         index=pd.RangeIndex(start=0, stop=8, step=1),
                         columns=["product_itemid", "product_name", "product_category",
                                  "product_price", "product_discount", "product_like_count",
                                  "product_comment_count", "product_views",
                                  "product_total_rating", "units_sold"])
    df_true = pd.DataFrame([[3590133563, "Short Sleeves",
                             "Women's T-shirt Short Sleeve Round Neck Cotton 30% Solid Color"
                             "  Korean Fashion",
                             284.0, 27, 23, 1, 659, 5.0, 2],
                            [3861115290, "Crop Top",
                             "[COD Ready Stock] Women Blouse Korean Top Chiffon Puff Sleeve"
                             " Crop Top Blouse Floral Croptop Long Sleeve T-Shirts Tops "
                             "Square Collar Pleated Shirt Women",
                             452.0, 90, 13455, 2446, 134994, 4.89, 6453],
                            [4771111702, "Top",
                             "M-5XL Mens Cotton Linen Long Sleeve Yoga Button Down Shirts"
                             " Summer Cotton and Linen Three-Quarter Sleeve Shirt Men's Linen"
                             " plus Size Shirt Solid Color Half Sleeves Korean Style Top Fashion"
                             " Short Sleeve Shirt",
                             1120.0, 58, 41, 5, 402, 5.0, 11],
                            [5452669710, "Long Sleeves",
                             "Long Sleeve Blouse Long Sleeve Crop top Trendy Tops Loose"
                             " Shirt for Women Long Sleeve Shirt Korean Style Tops Ulzzang"
                             " Tops for Women T-Shirt Fashion Women Clothes Casual Tops"
                             " Loose Tshirt Round Neck T Shirts",
                             398.0, 50, 1861, 137, 2680, 4.95, 275],
                            [5560472579, "Short Sleeves",
                             "LALUNA Korean Fashion Erich Basic Printed Floral Daily"
                             " Polo Tie Top 1104",
                             147.0, 7, 4, 5, 161, 5.0, 43],
                            [8528691619, "Short Sleeves",
                             "women button down knitted knit lettuce top strawberry floral"
                             " short sleeves women bangkok korean B032",
                             299.0, 74, 666, 204, 7779, 4.92, 493],
                            [9312209380, "Short Sleeves",
                             "7-color Korean version elegant retro Polo knit V-neck slim"
                             " short open navel Short Sleeve T-Shirt Top",
                             200.0, 26, 1161, 295, 9943, 4.88, 670],
                            [9440747987, "Long Sleeves",
                             "Zanzea Women Korean Casual Back Puff Sleeve Tops", 822.0, 46,
                             0, 2, 13, 5.0, 2]],
                           index=pd.Int64Index([0, 1, 2, 3, 4, 5, 6, 7], dtype="int64"),
                           columns=["product_itemid", "product_category", "product_name",
                                    "avg_price", "avg_discount", "like_count",
                                    "comment_count", "product_views", "avg_rating", "units_sold"])
    print(df_in.dtypes)
    # compute test results
    df_results = get_aggregated_features(df_in, ["product_itemid", "product_category",
                                                 "product_name"],
                                         ["product_price", "product_discount",
                                          "product_like_count", "product_comment_count",
                                          "product_views", "product_total_rating",
                                          "units_sold"],
                                         ["avg_price", "avg_discount", "like_count",
                                          "comment_count", "product_views", "avg_rating",
                                          "units_sold"],
                                         ["mean", "mean", "sum", "sum", "sum", "mean", "sum"])
    # Test that the true and test are the same
    pd.testing.assert_frame_equal(df_true, df_results)


def test_get_aggregated_features_no_df():
    """Test for getting aggregated product features with invalid data"""
    df_in = "This is not a pandas dataframe"
    with pytest.raises(SystemExit) as err:
        get_aggregated_features(df_in,
                                ["product_itemid", "product_category", "product_name"],
                                ["product_price", "product_discount", "product_like_count",
                                 "product_comment_count", "product_views", "product_total_rating",
                                 "units_sold"],
                                ["avg_price", "avg_discount", "like_count",
                                 "comment_count", "product_views", "avg_rating",
                                 "units_sold"],
                                ["mean", "mean", "sum", "sum", "sum", "mean", "sum"])
    assert err.type == SystemExit
    assert err.value.code == 1
