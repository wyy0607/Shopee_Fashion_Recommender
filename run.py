""" Receives command-line arguments from the user
and delegates instructions to the appropriate module in `src/`.
"""
import argparse
import logging.config
import sys

import yaml

from src import preprocess_products, preprocess_reviews, truncate_reviews
from src.get_csr_matrix import get_csr_matrix, save_csr_matrix
from src.fit_model import fit_model
from src.recommend_products import recommend_items, save_recommendations
from src.add_products import ProductManager, create_db
from src.s3 import download_file_from_s3, upload_file_to_s3
from config.flaskconfig import SQLALCHEMY_DATABASE_URI

logging.config.fileConfig("config/logging/local.conf")
logger = logging.getLogger("model-pipeline")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Model Pipeline for Recommending Fashion Products")
    parser.add_argument("--config_file",
                        help="path to configuration file",
                        default="config/model_config.yaml")
    subparsers = parser.add_subparsers(dest="subparser_name")

    # Sub-parser for uploading/downloading data to/from s3
    sb_s3 = subparsers.add_parser("s3", description="Upload/Download raw data")
    sb_s3.add_argument("--download", default=False, action="store_true",
                       help="If used, will load data via pandas")
    sb_s3.add_argument("--s3_path",
                       default="s3://2022-msia423-wu-yuyan/raw/2021June-July_product_data.csv",
                       help="If used, will load data via pandas")
    sb_s3.add_argument("--local_path", default="data/external/2021June-July_product_data.csv",
                       help="Where to load data to in S3")

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database")
    sb_create.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    # Sub-parser for ingesting new data from a csv file
    sb_ingest = subparsers.add_parser("ingest_data", description="Add data to database")
    sb_ingest.add_argument("--input_path", default="models/recommendations.csv",
                           help="path to the file that store product data to be added")
    sb_ingest.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    # Sub-parser for model pipeline
    sb_model = subparsers.add_parser("model",
                                     description="Model pipeline to recommend fashion products")
    actions = ["preprocess_products", "preprocess_reviews", "truncate_reviews",
               "get_csr_matrix", "fit_model", "recommend"]
    sb_model.add_argument("action",
                          help="action to take",
                          choices=actions)
    sb_model.add_argument("--config_file", default="config/model_config.yaml",
                          help="path to the file that store product data to be added")

    args = parser.parse_args()
    sp_used = args.subparser_name

    if sp_used == "s3":
        if args.download:
            download_file_from_s3(args.local_path, args.s3_path)
        else:
            upload_file_to_s3(args.local_path, args.s3_path)
    elif sp_used == "create_db":
        create_db(args.engine_string)
    elif sp_used == "ingest_data":
        product_manager = ProductManager(engine_string=args.engine_string)
        product_manager.add_products(args.input_path)
        product_manager.close()
    elif sp_used == "model":
        # process configuration file
        try:
            with open(args.config_file, "r", encoding="ASCII") as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
        except FileNotFoundError:
            logger.error("Cannot find input configure file")
            sys.exit(1)
        else:
            logger.info("Successfully loaded configuration file from %s", args.config_file)

        if args.action == "preprocess_products":
            product_df = preprocess_products.get_product_features(
                **config["preprocess_products"]["get_product_features"])
            processed_product_df = preprocess_products.get_aggregated_features(
                product_df, **config["preprocess_products"]["get_aggregated_features"])
            preprocess_products.save_product_data(
                processed_product_df, **config["preprocess_products"]["save_product_data"])

        if args.action == "preprocess_reviews":
            review_df = preprocess_reviews.get_review_features(
                **config["preprocess_reviews"]["get_review_features"])
            preprocess_reviews.save_review_data(
                review_df, **config["preprocess_reviews"]["save_review_data"])

        if args.action == "truncate_reviews":
            truncated_review_df = truncate_reviews.truncate_reviews(
                **config["truncate_reviews"]["truncate_reviews"])
            truncate_reviews.save_truncated_review_data(
                truncated_review_df, **config["truncate_reviews"]["save_truncated_review_data"])

        if args.action == "get_csr_matrix":
            csr_matrix = get_csr_matrix(**config["get_csr_matrix"]["get_csr_matrix"])
            save_csr_matrix(csr_matrix, **config["get_csr_matrix"]["save_csr_matrix"])

        if args.action == "fit_model":
            fit_model(**config["fit_model"]["fit_model"])

        if args.action == "recommend":
            RECOMMEND = recommend_items(
                **config["recommend_products"]["recommend_items"])
            save_recommendations(
                RECOMMEND, **config["recommend_products"]["save_recommendations"])

    else:
        parser.print_help()
