## Week 1 Homework

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command

Which tag has the following text? - *Write the image ID to the file* 

- `--imageid string`
- `--iidfile string`
- `--idimage string`
- `--idfile string`

### Answer: 

 `--iidfile string` (Write the image ID to the file)
 
### Code:

```docker --help build```


## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use pip list). 
How many python packages/modules are installed?

- 1
- 6
- 3
- 7

### Answer:

There are 3 python modules installed: pip, setuptools, wheel

### Code:

```docker run -it -entrypoint=bash python:3.9```

```pip list```




# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from January 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)

I put the data into Postgres using [upload-data.ipynb](https://github.com/LadyTastingData/de-zoomcamp/blob/main/week_1/homework1/upload-data.ipynb).

Then, I ran command:

```pgcli -h localhost -U root -d ny_taxi```


## Question 3. Count records 

How many taxi trips were totally made on January 15?

Tip: started and finished on 2019-01-15. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 20689
- 20530
- 17630
- 21090

### Answer: 

20530

### Code: 

```select count(*) from green_taxi_data where lpep_pickup_datetime::date = '2019-01-15' and lpep_dropoff_dat etime::date = '2019-01-15';```

## Question 4. Largest trip for each day

Which was the day with the largest trip distance
Use the pick up time for your calculations.

- 2019-01-18
- 2019-01-28
- 2019-01-15
- 2019-01-10

### Answer: 

2019-01-15 00:00:00 (max_ditance=117.99)

### Code: 

```
select date_trunc('day',lpep_pickup_datetime) as pickup_day,
max(trip_distance) as max_distance
from green_taxi_data
group by pickup_day
order by max_distance desc
limit 1;
```

## Question 5. The number of passengers

In 2019-01-01 how many trips had 2 and 3 passengers?
 
- 2: 1282 ; 3: 266
- 2: 1532 ; 3: 126
- 2: 1282 ; 3: 254
- 2: 1282 ; 3: 274

### Answer: 

2:1282; 3:254

### Code: 

```select count() from green_taxi_data where lpep_pickup_datetime::date = '2019-01-01' and passenger_count = 2;``` 

```select count() from green_taxi_data where lpep_pickup_datetime::date = '2019-01-01' and passenger_count = 3;```


## Question 6. Largest tip

For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- South Ozone Park
- Long Island City/Queens Plaza

### Answer: 

Long Island City/Queens Plaza

### Code: 

```
select dozones."Zone" as result
from green_taxi_data as taxi
inner join zones as puzones
on taxi."PULocationID"=puzones."LocationID"
left join zones as dozones
on taxi."DOLocationID"=dozones."LocationID"
where puzones."Zone" ilike '%Astoria%'
order by taxi.tip_amount desc
limit 1;
```

# Terraform

In this homework we'll prepare the environment by creating resources in GCP with Terraform.

I installed Terraform in my VM on GCP and copied the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup/1_terraform_gcp/terraform) to my VM.

I Modified the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 1. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

Paste the output of this command into the homework submission form.

### Code:

```shell
# Refresh service-account's auth-token for this session
gcloud auth application-default login

# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
terraform plan 
```

```shell
terraform apply 
```

```shell
# Delete infra after your work, to avoid costs on any running services
terraform destroy
```

