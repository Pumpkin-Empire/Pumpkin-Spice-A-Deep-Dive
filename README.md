# <p style="text-align: center;">Pumpkin-Empire:</p>
### A reproducible, modular data pipeline with automatic analytics using Twitter API, Postgres, Streamlit, and Docker
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
- Python Scripts
- SQL & PostgreSQL
- Docker Containerization
- Streamlit
- Jupyter Notebooks
- Data Analysis

## Prerequisites
- Docker (with CLI tools & Docker-Compose)

## Set-up
-  Download or pull this repository to your desired location.
-  Get Twitter API access keys & tokens (total of 5) [Twitter API](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api)
- Create a file called 'config.py' in the app/ folder of this project. This file will hold your Twitter API access information and postgres connection. The only fields that need to be filled out are: 

	- consumer\_key
	- consumer\_secret 
	- access\_token 
	- access\_token\_secret 
	- bearer\_token

	

>config.py

```
# Twitter API Access
consumer_key = "<your consumer key>"
consumer_secret = "<your consumer secret"
access_token = "<your access token>"
access_token_secret = "<you access token secret"
bearer_token = "<your bearer token>"

# Search
search='pumpkin spice'
```


***
## Starting the Pipeline


> **Note:**If you would like to build a database on a search for something other than 'pumpkin spice', update 'search' in the app/config.py file made earlier. Reference for making a query can be found here:
> [Building queries for searching Tweets](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query)

**First Pipeline**
---

The first query you wish to make a pipeline for is simple to get started. Navigate to the project's folder in the command line and enter the following command:

```
docker-compose up -d
```
![docker-compose up -d](/static/initialcompose.png)

>**Note:** To give this pipeline a different name than the default use:
>
>```
>docker-compose -p <name> up -d
>```
>
>Replace \<name> with a name of your choosing.

With that, your pipeline is running. 

**Docker Dashboard**

On the containers tab the pipeline can be seen. 4/4 containers should be running. Once the API request has been completed and written to the database, it waits fifteen minutes before making another request (due to limitations of Twitter's free API access).

![docker dashboard](/static/dockerdashboard.png)

Clicking on the running container shows the processes individually.

![docker containers](/static/dockercontainers.png)

We can check the result of the API request and writing to postgres by clicking on the container ending in 'api 1'. This is usually the 4th container in the list.

![docker response](/static/dockerresponse.png)

**Adminer**

Adminer is one of the containers inside our docker-compose. This allows us to view the database in a browser. 

To check if your database has been populated, open a browser and enter ```localhost:8080``` in the address bar.

> **Note:**Be sure to change the dropdown box from MySQL to PostgreSQL.

Login info:

```
server  : 	database
username: 	postgres
password: 	docker
database: 	database

```

The database page shows us the tables that were created. Either can be selected for further options.

![adminer tables](/static/adminertables.png)

Adminer features a GUI for executing SQL queries. It was mainly used in this project for debugging and ease of access to our database.

**Stremlit Analysis**

Analysis of the database is done automatically by the analysis container. It utilizes Streamlit and is available for viewing in your browser by navigating to:  ```localhost:8501```

![streamlit analysis](/static/streamlit.png)


**Creating Another Pipeline**


To create another pipeline using another search string is easy.

First, be sure to stop any running containers in the first pipeline. The new one will use the same ports, so it cannot run concurrently. You can do this by clicking the project in the Docker dashboard, then pressing the stop button for any running containers.

![Docker stop](/static/dockerstop.png)

Open config.py and update the search to a string of your choosing (comparison operators and 'AND' will throw errors, so please refer to the query building link earlier in this README for infomration on how to implement them).

![other search](/static/othersearch.png)

Then, from the command line in the project's main folder enter the following command: 
```docker-compose -p <name> up --build -d```

> **Note:** Not designating a name with the -p flag will overwrite the original pipeline.


After the image builds, it will be viewable in the Docker dashboard, and have available to it all the same features of the first pipeline.

![Multiple pipelines](/static/multiplepipelines.png)

> **Note:** To restart another pipeline: First, stop the containers in the one currently running. Then, on Docker Dashboard's Containers tab, hit the play button on the pipeline you wish to continue working with.

## Learning Resources

