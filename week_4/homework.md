## Week 4 Homework 

In this homework, we'll use the models developed during the week 4 videos and enhance the already presented dbt project using the already loaded Taxi data for fhv vehicles for year 2019 in our DWH.

This means that in this homework we use the following data [Datasets list](https://github.com/DataTalksClub/nyc-tlc-data/)
* Yellow taxi data - Years 2019 and 2020
* Green taxi data - Years 2019 and 2020 
* fhv data - Year 2019. 

We will use the data loaded for:

* Building a source table: `stg_fhv_tripdata`
* Building a fact table: `fact_fhv_trips`
* Create a dashboard 

If you don't have access to GCP, you can do this locally using the ingested data from your Postgres database
instead. If you have access to GCP, you don't need to do it for local Postgres -
only if you want to.

> **Note**: if your answer doesn't match exactly, select the closest option 


**Preparation:** Using the files [etl_web_to_gcs.py](https://github.com/LadyTastingData/de-zoomcamp/blob/main/week_2/homework2/etl_web_to_gcs.py) and [fhv_clean_etl_web_to_gcs.py](https://github.com/LadyTastingData/de-zoomcamp/blob/main/week_2/homework2/fhv_clean_etl_web_to_gcs.py), I downloaded the data files to GC Storage:

```
prefect deployment build week_2/homework2/etl_web_to_gcs.py:etl_parent_flow --name test1 -sb github/gh-block --apply
prefect agent start --work-queue "default"
prefect deployment build week_2/homework2/fhv_clean_etl_web_to_gcs.py:fhv_etl_parent_flow --name test2 -sb github/gh-block --apply
prefect agent start --work-queue "default"
```

Then, I created the tables in BigQuery using the following codes: 

```
-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `high-tenure-375016.dezoomcamp.external_green_tripdata`
OPTIONS (
  format = 'parquet',
  uris = ['gs://ltd-zoom/data/green/green_tripdata_*.parquet']
);

-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `high-tenure-375016.dezoomcamp.external_yellow_tripdata`
OPTIONS (
  format = 'parquet',
  uris = ['gs://ltd-zoom/data/yellow/yellow_tripdata_*.parquet']
);

-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `high-tenure-375016.dezoomcamp.external_fhv_clean_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://ltd-zoom/data/fhv_clean/fhv_tripdata_2019-*.csv.gz']
);
```

dbt files can be found [here](https://github.com/LadyTastingData/de-zoomcamp/tree/main/week_4/dbt). 

## Question 1: 

**What is the count of records in the model fact_trips after running all models with the test run variable disabled and filtering for 2019 and 2020 data only (pickup datetime)?** 

You'll need to have completed the ["Build the first dbt models"](https://www.youtube.com/watch?v=UVI30Vxzd6c) video and have been able to run the models via the CLI. 
You should find the views and models for querying in your DWH.

- 41648442
- 51648442
- 61648442
- 71648442

### Answer: 

- 61648442 (~ 61567785)

### Code:

In dbt Cloud:
```
dbt run --select stg_green_tripdata --var 'is_test_run:false'
dbt run --select stg_yellow_tripdata --var 'is_test_run:false'
dbt build --select +fact_trips --var 'is_test_run:false'
```

In BQ:
```
SELECT COUNT(1) FROM `high-tenure-375016.dbt_ltd.fact_trips` WHERE pickup_datetime BETWEEN '2019-01-01' AND '2020-12-31';
```


## Question 2: 

**What is the distribution between service type filtering by years 2019 and 2020 data as done in the videos?**

You will need to complete "Visualising the data" videos, either using [google data studio](https://www.youtube.com/watch?v=39nLTs74A3E) or [metabase](https://www.youtube.com/watch?v=BnLkrA7a6gM). 

- 89.9/10.1
- 94/6
- 76.3/23.7
- 99.1/0.9

### Answer: 

- 89.9/10.1 (~ 89.8/10.2))

The plots generated in Google Data Studio can be found [here](https://github.com/LadyTastingData/de-zoomcamp/blob/main/week_4/looker_studio/dezoomcamp-week-4_Report.pdf).


## Question 3: 

**What is the count of records in the model stg_fhv_tripdata after running all models with the test run variable disabled (:false)?**  

Create a staging model for the fhv data for 2019 and do not add a deduplication step. Run it via the CLI without limits (is_test_run: false).
Filter records with pickup time in year 2019.

- 33244696
- 43244696
- 53244696
- 63244696

### Answer:

- 43244696 (~ 43183729)

### Code:

In dbt cloud:
```
dbt run --select stg_fhv_tripdata --var 'is_test_run:false'
```

In BQ:
```
SELECT COUNT(1) FROM `high-tenure-375016.dbt_ltd.stg_fhv_tripdata` WHERE pickup_datetime BETWEEN '2019-01-01' AND '2019-12-31';
```


## Question 4: 

**What is the count of records in the model fact_fhv_trips after running all dependencies with the test run variable disabled (:false)?**  

Create a core model for the stg_fhv_tripdata joining with dim_zones.
Similar to what we've done in fact_trips, keep only records with known pickup and dropoff locations entries for pickup and dropoff locations. 
Run it via the CLI without limits (is_test_run: false) and filter records with pickup time in year 2019.

- 12998722
- 22998722
- 32998722
- 42998722

### Answer:

- 22998722 (~ 22989750)

### Code:

In dbt cloud:
```
dbt build --select +fact_fhv_trips --var 'is_test_run:false'
```

In BQ:
```
SELECT COUNT(1) FROM `high-tenure-375016.dbt_ltd.fact_fhv_trips` WHERE pickup_datetime BETWEEN '2019-01-01' AND '2019-12-31';
```


## Question 5: 

**What is the month with the biggest amount of rides after building a tile for the fact_fhv_trips table?**

Create a dashboard with some tiles that you find interesting to explore the data. One tile should show the amount of trips per month, as done in the videos for fact_trips, based on the fact_fhv_trips table.

- March
- April
- January
- December

### Answer:

- March (For year 2019)

The barplot generated in Google Data Studio can be found [here](https://github.com/LadyTastingData/de-zoomcamp/blob/main/week_4/looker_studio/dezoomcamp-week-4_Report.pdf).
