"""Creates, ingests data into, and enables querying of a table of
 products for the Fashion Recommender app to query from and display results to the user."""
import logging.config
import typing
import sys

import flask
import pandas as pd
from sqlalchemy import Column, Integer, String, Float, BigInteger, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)

Base: typing.Any = declarative_base()


class Product(Base):
    """Creates a data model for the database to be set up for capturing products"""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    input_itemid = Column(BigInteger, unique=False, nullable=False)
    rank = Column(Integer, unique=False, nullable=False)
    product_itemid = Column(BigInteger, unique=False, nullable=False)
    product_category = Column(String(100), unique=False, nullable=False)
    product_name = Column(String(100), unique=False, nullable=False)
    avg_price = Column(Float, unique=False, nullable=False)
    avg_discount = Column(Float, unique=False, nullable=False)
    like_count = Column(Integer, unique=False, nullable=False)
    comment_count = Column(Integer, unique=False, nullable=False)
    product_views = Column(Integer, unique=False, nullable=False)
    avg_rating = Column(Float, unique=False, nullable=False)
    units_sold = Column(Integer, unique=False, nullable=False)

    def __repr__(self):
        return f"<Products {self.input_itemid}>"


class ProductManager:
    """Creates a SQLAlchemy connection to the product table.

    Args:
        app (:obj:`flask.app.Flask`): Flask app object for when connecting from within a Flask app.
        engine_string (`str`): SQLAlchemy engine string specifying which database to write to.
    """
    def __init__(self, app: typing.Optional[flask.app.Flask] = None,
                 engine_string: typing.Optional[str] = None):
        if app:
            self.database = SQLAlchemy(app)
            self.session = self.database.session
        elif engine_string:
            engine = create_engine(engine_string)
            session_maker = sessionmaker(bind=engine)
            self.session = session_maker()
        else:
            raise ValueError(
                "Need either an engine string or a Flask app to initialize")

    def close(self) -> None:
        """Closes SQLAlchemy session

        Returns: None

        """
        self.session.close()

    def add_products(self, input_path: str) -> None:
        """Add all the data in a csv file into the database

        Args:
            input_path (`str`): path to the input csv file

        Returns:
              None
        """
        session = self.session
        # transform data into list of element {column -> value} for easy ingest
        data_list = pd.read_csv(input_path).to_dict(orient="records")
        product_list = [Product(**data) for data in data_list]
        try:
            session.add_all(product_list)
            session.commit()
        except OperationalError as err:
            error_message = "Error page returned. Not able to add products to MySQL database. " \
                            "Please check engine string and connection to Northwestern VPN."
            logger.error(error_message, "\n Error:", err)
            sys.exit(1)
        else:
            logger.info("records are added to the table")


def create_db(engine_string: str) -> None:
    """Create database with Products() data model from provided engine string.

    Args:
        engine_string (`str`): SQLAlchemy engine string specifying which database
            to write to

    Returns: None

    """
    engine = create_engine(engine_string)
    try:
        Base.metadata.create_all(engine)
    except OperationalError as err:
        error_message = "Error page returned. Not able to create database." \
                        "Please check engine string and connection to Northwestern VPN."
        logger.error(error_message, "\n Error:", err)
        sys.exit(1)
    else:
        logger.info("Database created.")
