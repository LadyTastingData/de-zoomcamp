### Setting up Google Cloud environment

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

- Now, let's configure Visual Studio Code to access this machine:
  - In VS Code, go to Extensions, search Remote - SSH and install it. Once installed, we see "Open a remote window" 
  in the bottom left corner. Click it then "Connect to Host", and we see de-zoomcamp (because we already created the config file).
  
  



 


### Docker + Postgres

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



Running postgres locally with docker

Putting some data for testing to local postres with Python

Packaging this script in Docker

Running postgres and the script in one network

Docker compose and running pgadmin and postres together with docker-compose


