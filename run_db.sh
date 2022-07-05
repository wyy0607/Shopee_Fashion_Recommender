python3 run.py s3 --s3_path=s3://2022-msia423-wu-yuyan/raw/2021June-July_product_data.csv --local_path=data/external/2021June-July_product_data.csv
python3 run.py s3 --s3_path=s3://2022-msia423-wu-yuyan/raw/2021June-July_review_data.csv --local_path=data/external/2021June-July_review_data.csv
python3 run.py s3 --download --s3_path=s3://2022-msia423-wu-yuyan/raw/2021June-July_product_data.csv --local_path=data/external/2021June-July_product_data.csv
python3 run.py s3 --download --s3_path=s3://2022-msia423-wu-yuyan/raw/2021June-July_review_data.csv --local_path=data/external/2021June-July_review_data.csv
python3 run.py create_db
python3 run.py ingest_data