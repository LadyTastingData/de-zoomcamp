## Week 3 Homework
<b><u>Important Note:</b></u> <p>You can load the data however you would like, but keep the files in .GZ Format. 
If you are using orchestration such as Airflow or Prefect do not load the data into Big Query using the orchestrator.</br> 
Stop with loading the files into a bucket. </br></br>
<u>NOTE:</u> You can use the CSV option for the GZ files when creating an External Table</br>

<b>SETUP:</b></br>
Create an external table using the fhv 2019 data. </br>
Create a table in BQ using the fhv 2019 data (do not partition or cluster this table). </br>
Data can be found here: https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv </p>

### Codes for Setup: 
For this exercise, I continued using the same conda environment that I created for last week's exercises. For loading the fhv 2019 data to Google Cloud Storage bucket, I used Prefect and run the flow in the file [fhv_etl_web_to_gcs.py](https://github.com/LadyTastingData/de-zoomcamp/blob/main/week_3/homework3/fhv_etl_web_to_gcs.py). Then, I run the following commands:

```prefect deployment build ./fhv_etl_web_to_gcs.py:fhv_etl_parent_flow -n "Parameterized ETL"```

Inside the generated yaml file, I edited the parameters:

```parameters: {"months": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "year": 2019}```

Then, 

```prefect deployment apply fhv_etl_parent_flow-deployment.yaml```

```prefect agent start --work-queue "default"```

Now, we can see the fhv data files for the year 2019 inside GCS bucket. 

For creating an external table using the fhv data in GCS Bucket, I have run the following SQL code in Google Cloud BigQuery (BQ):

```
-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `high-tenure-375016.dezoomcamp.external_fhv_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://ltd-zoom/data/fhv/fhv_tripdata_2019-*.csv.gz']
);
```

Then, I created a non-partitioned table in BQ using the fhv 2019 data, with the code below:

```
-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE high-tenure-375016.dezoomcamp.fhv_tripdata_non_partitoned AS
SELECT * FROM high-tenure-375016.dezoomcamp.external_fhv_tripdata;
```

## Question 1:
What is the count for fhv vehicle records for year 2019?
- 65,623,481
- 43,244,696
- 22,978,333
- 13,942,414

### Answer:

- 43,244,696

(We can find this information in the details of the non-partitioned table: high-tenure-375016.dezoomcamp.fhv_tripdata_non_partitoned)


## Question 2:
Write a query to count the distinct number of affiliated_base_number for the entire dataset on both the tables.</br> 
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

- 25.2 MB for the External Table and 100.87MB for the BQ Table
- 225.82 MB for the External Table and 47.60MB for the BQ Table
- 0 MB for the External Table and 0MB for the BQ Table
- 0 MB for the External Table and 317.94MB for the BQ Table 

### Answer:

- 0 MB for the External Table and 317.94MB for the BQ Table 

### Code:
```
-- Scanning 0 B of data
SELECT COUNT(DISTINCT affiliated_base_number) AS disctinct_num_abn
FROM high-tenure-375016.dezoomcamp.external_fhv_tripdata;

-- Scanning 317.94 MB of data
SELECT COUNT(DISTINCT affiliated_base_number) AS disctinct_num_abn
FROM high-tenure-375016.dezoomcamp.fhv_tripdata_non_partitoned;
```

## Question 3:
How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset?
- 717,748
- 1,215,687
- 5
- 20,332

### Answer: 

- 717,748

### Code:
```
SELECT COUNT(*)
FROM high-tenure-375016.dezoomcamp.fhv_tripdata_non_partitoned
WHERE PUlocationID IS NULL AND DOlocationID IS NULL;
```


## Question 4:
What is the best strategy to optimize the table if query always filter by pickup_datetime and order by affiliated_base_number?
- Cluster on pickup_datetime Cluster on affiliated_base_number
- Partition by pickup_datetime Cluster on affiliated_base_number
- Partition by pickup_datetime Partition by affiliated_base_number
- Partition by affiliated_base_number Cluster on pickup_datetime

### Answer: 

- Partition by pickup_datetime Cluster on affiliated_base_number

## Question 5:
Implement the optimized solution you chose for question 4. Write a query to retrieve the distinct affiliated_base_number between pickup_datetime 2019/03/01 and 2019/03/31 (inclusive).</br> 
Use the BQ table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values? Choose the answer which most closely matches.
- 12.82 MB for non-partitioned table and 647.87 MB for the partitioned table
- 647.87 MB for non-partitioned table and 23.06 MB for the partitioned table
- 582.63 MB for non-partitioned table and 0 MB for the partitioned table
- 646.25 MB for non-partitioned table and 646.25 MB for the partitioned table

### Answer: 

- 647.87 MB for non-partitioned table and 23.06 MB for the partitioned table

### Code:
```
-- Create a partitioned table from external table and cluster by affiliated_base_number
CREATE OR REPLACE TABLE high-tenure-375016.dezoomcamp.fhv_tripdata_partitoned
PARTITION BY DATE(pickup_datetime)
CLUSTER BY affiliated_base_number AS
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
```


## Question 6: 
Where is the data stored in the External Table you created?

- Big Query
- GCP Bucket
- Container Registry
- Big Table

### Answer:

- GCP Bucket


## Question 7:
It is best practice in Big Query to always cluster your data:
- True
- False

### Answer:

- False


## (Not required) Question 8:
A better format to store these files may be parquet. Create a data pipeline to download the gzip files and convert them into parquet. Upload the files to your GCP Bucket and create an External and BQ Table. 


Note: Column types for all files used in an External Table must have the same datatype. While an External Table may be created and shown in the side panel in Big Query, this will need to be validated by running a count query on the External Table to check if any errors occur. 
 
