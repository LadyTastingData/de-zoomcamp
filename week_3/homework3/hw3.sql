-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `high-tenure-375016.dezoomcamp.external_fhv_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://ltd-zoom/data/fhv/fhv_tripdata_2019-*.csv.gz']
);
-- Check fhv trip data
SELECT * FROM high-tenure-375016.dezoomcamp.external_fhv_tripdata limit 10;

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE high-tenure-375016.dezoomcamp.fhv_tripdata_non_partitoned AS
SELECT * FROM high-tenure-375016.dezoomcamp.external_fhv_tripdata;

---Question 2:
-- Scanning 0 B of data
SELECT COUNT(DISTINCT affiliated_base_number) AS disctinct_num_abn
FROM high-tenure-375016.dezoomcamp.external_fhv_tripdata;

-- Scanning 317.94 MB of data
SELECT COUNT(DISTINCT affiliated_base_number) AS disctinct_num_abn
FROM high-tenure-375016.dezoomcamp.fhv_tripdata_non_partitoned;

--- Question 3:
SELECT COUNT(*)
FROM high-tenure-375016.dezoomcamp.external_fhv_tripdata
WHERE PUlocationID IS NULL AND DOlocationID IS NULL;
--- OR
SELECT COUNT(*)
FROM high-tenure-375016.dezoomcamp.fhv_tripdata_non_partitoned
WHERE PUlocationID IS NULL AND DOlocationID IS NULL;

-- Question 5:
-- Create a partitioned table from external table
CREATE OR REPLACE TABLE high-tenure-375016.dezoomcamp.fhv_tripdata_partitoned
PARTITION BY
  DATE(pickup_datetime) AS
SELECT * FROM high-tenure-375016.dezoomcamp.external_fhv_tripdata;

-- Impact of partition
-- Scanning 647.87 MB of data
SELECT DISTINCT(affiliated_base_number)
FROM high-tenure-375016.dezoomcamp.fhv_tripdata_non_partitoned
WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31';

-- Scanning ~23.05 MB of DATA
SELECT DISTINCT(affiliated_base_number)
FROM high-tenure-375016.dezoomcamp.fhv_tripdata_partitoned
WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31';

