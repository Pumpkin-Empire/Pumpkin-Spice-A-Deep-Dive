# Pumpkin-Empire: A data pipeline using Twitter API, Postgres, Jupyter Notebook, Pandas, and Docker
***

## About

A group project to better learn how to build a reproducible ETL data pipeline.

Docker is used to launch the ETL, though some set up is required (see below). Python is used to get tweets from Twitter API v2 and store them in a PostgreSQL database. This data is loaded in to a Jupyter Notebook for analysis by using the Pandas library for its DataFrames and various other analytics tools (nltk, Matplotlib, sns, Textblob...)


## Scenario
Pumpkin Spice season is no longer relegated to Autumn. Twitter has something to say about everything, and this should be no different. Find the sentiment across Twitter in regards to Pumpkin Spice products.

## Concepts
- Data Engineering
- ETL (Extract, Transform, Load)
- REST APIs
- Python scripts
- SQL & PostgreSQL
- Docker Containerization
- Jupyter Notebooks
- Pandas
- Data Analysis

## Prerequisites
- Docker (with CLI & Docker-Compose)

## Set-up
-  Download or pull this repository to your desired location.
-  Get Twitter API access keys & tokens (total of 5)[Twitter API](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api)
- Create a file called 'config.py' in the app/ folder of this project. This file will hold your Twitter API access information and postgres connection. The only fields that need to be filled out are: 
	- consumer\_key
	- consumer\_secret 
	- access\_token 
	- access\_token\_secret 
	- bearer\_token

```
# Twitter API Access
consumer_key = "<your consumer key>"
consumer_secret = "<your consumer secret"
access_token = "<your access token>"
access_token_secret = "<you access token secret"
bearer_token = "<your bearer token>"

# Search
search='pumpkin spice'

# postgres connection
hostname='database'
port='5432'
dbname='database'
uname='postgres'
pwd='docker'
```
***
## Starting the Pipeline


> **Note:**If you would like to build a database on a search for something other than 'pumpkin spice', update 'search' in the app/config.py file made earlier. Reference for making a query can be found here:
> - [Building queries for Search Tweets](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query)

**First Pipeline**
---

The first query you wish to make a pipeline for is simple to get started. Navigate to the project's folder in the command line and enter the following command:
```
docker-compose up -d
```
![docker-compose up -d](/static/initialcompose.png)

From here there are a few things that can be looked at:

**Docker Dashboard**

On the containers tab the pipeline can be seen. 2/3 or 3/3 processes may be running. Once the API request has been completed and written to the database, that process closes.

![docker dashboard](/static/dockerdashboard.png)

Clicking on the running container shows the processes individually.

![docker containers](/static/dockercontainers.png)

We can check the result of the API request and writing to postgres by clicking on the container ending in 'app 1'.

![docker response](/static/dockerresponse.png)

**Adminer**

Adminer is one of the containers inside our docker-compose. This allows us to view the database in a browser. 

To check if your database has been populated, open a browser and enter ```localhost:8080``` in the address bar.

> **Note:**Be sure to change the dropdown box from MySQL to PostgreSQL.

Login info:

```
server 		database
username 	postgres
password 	docker
database 	database

```

The database page shows us the tables that were created. Either can be selected for further options.

![adminer tables](/static/adminertables.png)

#ANALYSIS INSTRUCTIONS HERE

**Creating Another Pipeline**


To create another pipeline using another search string is easy.

First, be sure to stop any running containers in the first pipeline. The new one will use the same ports, so it cannot run concurrently. You can do this by clicking the project in the Docker dashboard, then pressing the stop button for any running processes.

Open config.py and update the search to a string of your choosing (comparison operators and 'AND' will throw errors, so please refer to the early query building link on how to implement them).

![other search](/static/othersearch.png)

Then, from the command line in the project's main folder enter the following command: 
```docker-compose -p <name> up --build -d```

> **Note:** not designating a name with the -p flag will overwrite the original pipeline.

Replace \<name> with a name of your choosing for the new image.

After the image builds, it will be viewable in the Docker dashboard, and have available to it all the same features of the first pipeline.

