### Setting up Google Cloud environment
Video: https://www.youtube.com/watch?v=ae-CV2KfoN0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=13&ab_channel=DataTalksClub%E2%AC%9B

We will run a virtual machine (VM) on Google Cloud. For this,
 - Enable Compute Engine API (New customers get $300 in free credits to spend on Google Cloud).
 - Before creating a VM instance, we need to generate a ssh key that we will use to log in to the VM instance.
 - [Generating ssh key] (https://cloud.google.com/compute/docs/connect/create-ssh-keys)
  - cd .ssh/
  - ssh-keygen -t rsa -f KEY_FILENAME -C USERNAME -b 2048
  - KEY_FILENAME: the name for SSH key file 
  - USERNAME: username on the VM
  - Two files created: FILENAME contains the private key; FILENAME.pub contains the public key.
  - We will put the public key to Google cloud: On Google Cloud, Settings -> Metadata -> SSH KEYS
- Go back to VM instances and create instance
  - e2-standard-4 (4 vCPU, 16 GB memory)
  - We can change boot disk: For example, set OS Ubuntu 20.04 LTS and size to 30 GB.
- Once the VM instance has been created, copy external IP
- Go to terminal and type following to access the instance:
  - ssh -i ~/.ssh/KEY_FILENAME USERNAME@EXTERNAL_IP
  - htop
  - gcloud --version
- In order to simplify ssh login, let us create config file under ~/.ssh/ for configuring ssh
  - touch config
  - Copy the following inside config file:

| Host de-zoomcamp  <br />
|    HostName EXTERNAL_IP <br />
|    User USERNAME <br />
|    IdentityFile /Users/xxx/.ssh/gcp <br />

- Now, we can simply write: ssh de-zoomcamp
  
- Next, we need to configure the instance.
  - Download and install Anaconda for Linux: 
    - wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
    - bash Anaconda3-2022.10-Linux-x86_64.sh
  - Install anaconda3
  - less .bashrc (We can see anaconda has been installed)
  - logout and log in again; or simply: source .bashrc 
  
- Now, we see that anaconda works (we see (base))
  - which python
  - python
    - import pandas as pd
    - pd.__version__

- Having installed anaconda, next we will install Docker:
  - sudo apt-get update
  - sudo apt-get install docker.io
  - docker run hello-world
  - In order to give the permissions, execute commands given at https://github.com/sindresorhus/guides/blob/main/docker-without-sudo.md
  - sudo groupadd docker
  - sudo gpasswd -a $USER docker
  - Log out and log back 
  - sudo service docker restart
  - docker run hello-world
  - docker run -it ubuntu bash
  - ls
  - exit

- Next, we will install docker compose.
 - Go to github docker compose latest release: https://github.com/docker/compose/releases/tag/v2.15.1
 - Copy the link for docker-compose-linux-x86_64
 - mkdir bin
 - cd bin
 - wget https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-linux-x86_64 -O docker-compose
 - Make it executable: chmod +x docker-compose
 - ./docker-compose version
 - In order to make it visible from any directory; add the following line to the end of .bashrc: export PATH="${HOME}/bin:${PATH}"
 - nano .bashrc (To save; press CTRL+o and to exit; CTRL+x)
 - source .bashrc
 - which docker-compose
 - docker-compose version

- cd data-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql
- ls
- To download the images for pgadmin and postgres: docker-compose up -d
- docker ps
- docker kill CONTAINER_ID (for killing)

Now, let's get back to home directory and install pgcli
- cd
- pip install pgcli
- pgcli -h localhost -U root -d ny_taxi % This did not work, let's try to install it with Conda to download the compiled version:
- pip uninstall pgcli
- conda install -c conda-forge pgcli
- pip install -U mycli
- pgcli -h localhost -U root -d ny_taxi % Password for the root: root (See: https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_1_basics_n_setup/2_docker_sql/docker-compose.yaml)
- \dt
- Exit by pressing Ctrl+d

- cd data-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql
- docker ps
- 

Now we see that postgres:13 is running on port 5432 and pgadmin4 on port 8080. We would like to forward this port to our local machine so that we can interact with postgres instance locally.
- In VS Code, go to ports -> forward a port, and add the port number 5432.
Now, we should be able to access this port from our local machine. So, if we just open a new terminal on our computer and type
pgcli -h localhost -U root -d ny_taxi, it should work.
- Similarly, we add port number 8080 in VS code. Then, we go to browser and go to address localhost:8080
Pgadmin login: admin@admin.com (Pswd:root)

Now, let us start jupyter in the VM:
- cd cd data-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql
-jupyter notebook
We see port 8888, add this port number in VS code. And copy the localhost link and paste it in our browser: http://localhost:8888/?token=5d5974af6ba774f5b465318e3eb2a6a281c1d6c4f56e713c

Open upload_data.ipynb (Also load the data: wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv) and try running the codes...

- pgcli -h localhost -U root -d ny_taxi
- \dt
- select count(1) from green_taxi_data

select count(*) from green_taxi_data where lpep_pickup_datetime::date = '2019-01-15' and lpep_dropoff_dat
 etime::date = '2019-01-15';
 Answer: 20530
 
select date_trunc('day',lpep_pickup_datetime) as pickup_day,
max(trip_distance) as max_distance
from green_taxi_data
group by pickup_day
order by max_distance desc
limit 1;

Answer: 2019-01-15 00:00:00 (max_ditance=117.99)

select count(*) from green_taxi_data where lpep_pickup_datetime::date = '2019-01-01' and passenger_count = 2;
select count(*) from green_taxi_data where lpep_pickup_datetime::date = '2019-01-01' and passenger_count = 3;

Answer: 2:1282; 3:254


select dozones."Zone" as result
from green_taxi_data as taxi
inner join zones as puzones
on taxi."PULocationID"=puzones."LocationID"
left join zones as dozones
on taxi."DOLocationID"=dozones."LocationID"
where puzones."Zone" ilike '%Astoria%'
order by taxi.tip_amount desc
limit 1;

Answer: Long Island City/Queens Plaza






Next, we will install Terraform
Copy the link for Linux binary download Amd64 for Terraform: https://releases.hashicorp.com/terraform/1.3.7/terraform_1.3.7_linux_amd64.zip
- cd
- cd bin
- wget https://releases.hashicorp.com/terraform/1.3.7/terraform_1.3.7_linux_amd64.zip
- sudo apt-get install unzip
- unzip terraform_1.3.7_linux_amd64.zip
- rm terraform_1.3.7_linux_amd64.zip
- cd 
- terraform -version
- cd data-engineering-zoomcamp/week_1_basics_n_setup/1_terraform_gcp/terraform/

Now we need the json credentials. We need to put the json file from our google cloud account to here. [Add it later]
- export GOOGLE_APPLICATION_CREDENTIALS myfile.json

# Refresh service-account's auth-token for this session
gcloud auth application-default login

# Initialize state file (.tfstate)
terraform init

ls -la

# Check changes to new infra plan
terraform plan -var="project=<your-gcp-project-id>"
terraform plan  (enter project id)

 terraform apply
 
 Answer: 
 var.project
  high-tenure-375016

  Enter a value: h


Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the
following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.dataset will be created
  + resource "google_bigquery_dataset" "dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "trips_data_all"
      + delete_contents_on_destroy = false
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + labels                     = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "europe-north1-a"
      + project                    = "h"
      + self_link                  = (known after apply)

      + access {
          + domain         = (known after apply)
          + group_by_email = (known after apply)
          + role           = (known after apply)
          + special_group  = (known after apply)
          + user_by_email  = (known after apply)

          + dataset {
              + target_types = (known after apply)

              + dataset {
                  + dataset_id = (known after apply)
                  + project_id = (known after apply)
                }
            }

          + routine {
              + dataset_id = (known after apply)
              + project_id = (known after apply)
              + routine_id = (known after apply)
            }

          + view {
              + dataset_id = (known after apply)
              + project_id = (known after apply)
              + table_id   = (known after apply)
            }
        }
    }

  # google_storage_bucket.data-lake-bucket will be created
  + resource "google_storage_bucket" "data-lake-bucket" {
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "EUROPE-NORTH1-A"
      + name                        = "dtc_data_lake_h"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + uniform_bucket_level_access = true
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "Delete"
            }

          + condition {
              + age                   = 30
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }

      + versioning {
          + enabled = true
        }

      + website {
          + main_page_suffix = (known after apply)
          + not_found_page   = (known after apply)
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.dataset: Creating...
google_storage_bucket.data-lake-bucket: Creating...
 
 
 


Next, we will configure our google cloud cli & Run Terraform commands [Add it later]

To close ssh connections,
- sudo shutdown now



FAQ: https://docs.google.com/document/d/19bnYs80DwuUimHM65UV3sylsCn2j1vziPOwzBwQrebw/edit#



- Now, let's configure Visual Studio Code to access this machine:
  - In VS Code, go to Extensions, search Remote - SSH and install it. Once installed, we see "Open a remote window" 
  in the bottom left corner. Click it then "Connect to Host", and we see de-zoomcamp (because we already created the config file).
  
  



 


### Docker + Postgres
Video: https://www.youtube.com/watch?v=EYNwNlOrpr0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=4&ab_channel=DataTalksClub%E2%AC%9B

- Docker is a platform which allows us to deliver software in packages called containers. Each container has its own configuration (operating system, 
software packages, libraries, dependencies, etc.) and is isolated from other
containers. However, containers can communicate with each other through well-defined channels.

- For example, a container may look like this: 

---
- Ubuntu 20.04                    
- Data pipeline[^1]                  
  - Python 3.9                    
  - Pandas                       
  - Postgres connection library   

[^1]: Data pipeline gets in data and produces more data. E.g. Source data file (e.g. csv file) -> Data Pipeline -> Table in Postgres (dest)
---

- As long as we have Docker, we don't need to install each specific requirement separately on our own. This allows us to 
take a docker image and run it on another environment such as Google Cloud (Kubernetes) and AWS Batch.

- Docker is very useful for reproducibility, setting up local experiments and performing integration tests. 

- Also , platforms like Spark and Serverless (AWS Lambda, Google functions) let us define the environment as a docker image.

- docker run hello-world
- docker run -it ubuntu bash

- docker run -it python:3.9
We need to get to bash to be able to install a command. Then instead of a python prompt we will have bash prompt.
- docker run -it --entrypoint=bash python:3.9
- pip install pandas

To create a new image which contains python:3.9 with pandas, create a Dockerfile and write:
FROM python:3.9
RUN pip install pandas
ENTRYPOINT [ "bash" ]

- cd data-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql
- docker build -t test:pandas .
- docker run -it test:pandas
- python
- import pandas
- pandas.__version__

We can also create a pipeline.py and write our Python code....


## Ingesting NY Taxi Data to Postgres

Now we will run Postgres in Docker and we will put some data to Postgres by using a Python script.
To run Postgres, we need the Docker image for Postgres
- docker pull postgres


- sudo chmod a+rwx ny_taxi_postgres_data
- docker run -it -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" -e POSTGRES_DB="ny_taxi" -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data -p 5432:5432 postgres:13




pip install pgcli (pgcli is a Python library)




We will use python in order to read the dataset, load it and put it in postgres.




Running postgres locally with docker

Putting some data for testing to local postres with Python

Packaging this script in Docker

Running postgres and the script in one network

Docker compose and running pgadmin and postres together with docker-compose


