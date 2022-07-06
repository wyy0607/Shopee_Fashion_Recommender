# Shopee Fashion Recommender

Author: Yuyan Wu

# Table of Contents
* [Project charter](#Project-Charter)
    * [1. Vision ](#1.-Vision)
    * [2. Mission ](#2.-Mission)
    * [3. Success Criteria ](#3.-Success-Criteria)
* [Directory structure ](#Directory-Structure)
* [Instruction on running the project ](#Instruction-on-Running-the-Project)
  * [1. Setup ](#1.-Setup)
  * [2. Acquire raw data ](#2.-Acquire-Raw-Data)
  * [3. Model pipeline ](#3.-Model-Pipeline)
  * [4. Store results in database ](#4.-Store-Results-in-Database)
  * [5. Run the app](#5.-Run-the-app)
  * [6. Testing](#6.-Testing)

## Project Charter

### 1. Vision

When shopping online for clothes, many people can be overwhelmed by the enormous options they get or get discouraged when they could not find their desired pieces after scrolling for a long while. This app is therefore designed to recommend users fashion garments that suit their needs and preferences. It hopefully could find users the right items they need without taking away their joy of searching for clothes.

### 2. Mission

The app uses data from [Shopee Philippines - Korean Inspired Clothing dataset](https://www.kaggle.com/datasets/jaepin/shopeeph-koreantop-clothing?select=2021June-July_shop_data.csv) from Kaggle to build a recommendation system that suggests relevant items to users with their specifications. Users will input the item id of the product they like. The app uses KNN algorithm to find items that resemble users' specifications. 

### 3. Success Criteria

#### Machine Learning Performance Metrics

Since the recommendation system uses KNN algorithm, the app cannot be evaluated based on distances of between-cluster and within-cluster points, such as the Silhouette score and the Davies-Bouldin Index. 

Once the app goes live, we could collect user data and use accuracy metrics like precision and recall scores to evaluate the success of the app in recommending users items that they may like. 

#### Business Metrics

Once the app is launched, business metrics including acquisition rate, retention rate, and sales conversion rate will be monitored to evaluate the success of the app from business perspectives. 

## Directory Structure 

```
├── README.md                         <- You are here
├── app
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs   
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that **do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── interim/                      <- Intermidiate data generated during model pipeline
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── dockerfiles/                      <- Directory for all project-related Dockerfiles 
│   ├── Dockerfile.app                <- Dockerfile for building image to run web app
│   ├── Dockerfile.run                <- Dockerfile for building image to execute run.py  
│   ├── Dockerfile.test               <- Dockerfile for building image to run unit tests
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs) that ** do not sync** , model predictions, and/or model summaries
│
├── notebooks/
│   ├── recommendations.ipynb         <- Template notebook for analysis with useful imports and helper functions 
│
├── src/                              <- Source data for the project. No executable Python files should live in this folder
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the web app 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## Instruction on Running the Project

### 1. Setup

#### Connection to the Northwestern Network

If you want to run commands beside building the model pipeline locally, connection to Northwestern Network is required. 

#### Environment Variable

##### AWS Credential

You need to have two environment variables - `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`  setup in your computer to run the following commands with S3. A simple way to do this run the following two lines in your terminal shell. Note that you need to replace "YOUR_ACCESS_KEY_ID" and "YOUR_SECRET_ACCESS_KEY" to your real id and secret access key. 

```bash
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
```

##### RDS Credential

###### Database Connection URI

You need to define an environment variable call `SQLALCHEMY_DATABASE_URI` to create database and ingest data into the remote database. The format for this URI is described below.  

```bash
export SQLALCHEMY_DATABASE_URI = "YOUR_DATABASE_URI"
```

A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). 

###### Database Information 

The URI above should be sufficient to run most of the docker commands in this project. However, as we will discuss later, we need to be able to enter the interactive session for the remote mysql database. Thus, you also need to define these environment variables. Note that you need to replace these with your actual connection credentials. 

```bash
export MYSQL_USER="YOUR_SQL_USER_NAME"
export MYSQL_PASSWORD="YOUR_SQL_PASSWORD"
export MYSQL_HOST="YOUR_SQL_HOST"
export MYSQL_PORT="YOUR_SQL_PORT"
export MYSQL_DATABASE="YOUR_DATABASE_NAME"
```

You could save all above commands in the ~/.profile file through:

```bash
vi ~/.profile
```

If you have already saved all above commands in the ~/.profile file, you could source the file directly to finish all environment variables and credentials settings in one single command though:

```bash
source ~/.profile
```

#### Docker Image

This project relies on four Docker image to run the command.  You can build these four images with the following command.

```bash
docker build -f dockerfiles/Dockerfile -t shopee-recommender .
docker build -f dockerfiles/Dockerfile.app -t shopee-recommender-app .
docker build -f dockerfiles/Dockerfile.model -t shopee-recommender-model .
docker build -f dockerfiles/Dockerfile.test -t shopee-recommender-test .
```

The `docker build -f dockerfiles/Dockerfile -t shopee-recommender .` will produce a Docker image called `shopee-recommender`, which are used to get the raw data, run the model pipeline, and interact with database. 
The `docker build -f dockerfiles/Dockerfile.app -t shopee-recommender-app .` will produce a Docker image called `shopee-recommender-app`, which are used to launch the flask app. 
The `docker build -f dockerfiles/Dockerfile.model -t shopee-recommender-model .` will produce a Docker image called `shopee-recommender-model`, which are used to run the whole model pipeline. 
The `docker build -f dockerfiles/Dockerfile.test -t shopee-recommender-test .` will produce a Docker image called `shopee-recommender-test`, which are used to run unit tests.

### 2. Acquire Raw Data 

The dataset used for this app comes from Kaggle. To download the data, you can go to this [website](https://www.kaggle.com/datasets/jaepin/shopeeph-koreantop-clothing?select=2021June-July_shop_data.csv) and click the Download button at the top of the page. 

Note that you will need to register a Kaggle account in order to download dataset if you do not have one. Because the dataset is relatively small, we also save a copy in `data/raw/*`. Only product and review information are used in this project, so only the copy of csv files related to the information is saved. Another copy is also uploaded to S3.

You can use the following command to download the data from S3. 

```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY shopee-recommender s3 --download --s3_path=s3://2022-msia423-wu-yuyan/raw/2021June-July_product_data.csv --local_path=data/external/2021June-July_product_data.csv
docker run --mount type=bind,source="$(pwd)",target=/app/ -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY shopee-recommender s3 --download --s3_path=s3://2022-msia423-wu-yuyan/raw/2021June-July_review_data.csv --local_path=data/external/2021June-July_review_data.csv
```

If you want to upload this data to your own S3 bucket, see this optional section below.

#### [Optional] Upload Data to S3


To upload the data to S3 with docker, you can run the following command. You need to specify your local data path and S3 data path by replacing the `{your_local_path}` and `{your_s3_path}` below. The default `s3_path` is `s3://2022-msia423-wu-yuyan/raw/2021June-July_product_data.csv` and the default `local_path` is `data/external/2021June-July_product_data.csv`.

```bash
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY shopee-recommender s3 --s3_path={your_s3_path} --local_path={your_local_path}
```

### 3. Model Pipeline

#### Run the Whole Model Pipeline:

```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ shopee-recommender-model run_model.sh
```

#### Preprocess Product Data

```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ shopee-recommender model preprocess_products
```

#### Preprocess Review Data

```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ shopee-recommender model preprocess_reviews
```

#### Truncate Review Data 

```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ shopee-recommender model truncate_reviews
```

#### Get CSR Matrix

```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ shopee-recommender model get_csr_matrix
```

#### Fit Model

```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ shopee-recommender model fit_model
```

#### Recommend Items

```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ shopee-recommender model recommend
```

### 4. Store Results in Database

#### Local Database configuration 

##### SQLite Path

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file: 

```python
engine_string='sqlite:///data/products.db'
```

The three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory). You can also define the absolute path with four `////`.


##### Create Database Locally

You can create the database locally with the following command. 

```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ shopee-recommender create_db 
```

By default, the sqlite engine string is `sqlite:///data/products.db`. You can configure your own sqlite engine by setting the environment variable `SQLALCHEMY_DATABASE_URI` as follows. 

```bash
export SQLALCHEMY_DATABASE_URI = "sqlite:///data/{your_db_name}"
```

##### Add information to the Databases Locally

You can ingest the recommendation result to the local database with the following command. 

```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ shopee-recommender ingest_data 
```

By default, this code ingests the csv file located in `models/recommendations.csv`. If you need to specify an alternative data path, you can do the following by replacing the `{your_data_path}` below.

```
docker run --mount type=bind,source="$(pwd)",target=/app/ shopee-recommender ingest_data --input_path={your_data_path}
```

##### Examine the Added Information in Local

If you create the database locally, you can view your result by using any sqlite client, such as [DB Browser](https://sqlitebrowser.org/), to open the `.db` file created after running the commands above.  

#### Remote Database Connection

##### Prerequisites

In order to proceed with the following command, you need to satisfy the following requirements:

1. You need to **connect to the Northwestern VPN**.

2. You set up your environment variable correctly as described in the section: [RDS Credential](#rds-credential). 


##### Test Connection to Database

You can run the following to test whether you can connect to the database. 

```bash
docker run -it --rm \
		mysql:5.7.33 \
		mysql \
		-h$$MYSQL_HOST \
		-u$$MYSQL_USER \
		-p$$MYSQL_PASSWORD
```

If succeeded, you should be able to enter an interactive mysql session, and you can show all databases you have with the command: `show databases;`.

##### Create Databases Remotely

You can create a new database with the following command. Note that the engine string is configured by the `SQLALCHEMY_DATABASE_URI` environment variable. You should specify this variable to decide where to create the database.

```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ -e SQLALCHEMY_DATABASE_URI shopee-recommender create_db 
```

##### Add Information to the Databases Remotely

Similar to the section in the local database, this command ingest a csv file into the table.  The `SQLALCHEMY_DATABASE_URI` variable again determines the engine string for the database. Note that this command might take few minutes to complete.

```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ -e SQLALCHEMY_DATABASE_URI shopee-recommender create_db 
```

#### Examine the Added Information in Remote

You can reenter the mysql interactive session by using the command under section [Test Connection to Database](#test-connection-to-database). Then you can type the following command to examine whether the table was created by replacing `<your_database_name>`. 

```sql
show databases;
use <your_target_database_name>;
show tables; 
select * from products;
```

### 5. Run the app 

To run the Flask app, run the following command. Note that the `SQLALCHEMY_DATABASE_URI` environment variable will determine which database the app connects to.   

```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ -e SQLALCHEMY_DATABASE_URI -p 5000:5000 shopee-recommender-app
```

Then, you should be able to access the app at http://0.0.0.0:5000/ if you are not using a Windows machine. For Windows users, you can access the app at http://127.0.0.1:5000/ instead.

### 6.Testing

Use the following command to run all the unit tests.

```bash
docker run shopee-recommender-test
```
