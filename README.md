#Pumpkin-Empire: A data pipeline using Twitter API, Postgres, Jupyter Notebook, Pandas, and Docker
***

##About

A group project to better learn how to build a reproducible ETL data pipeline.

Docker is used to launch the ETL, though some set up is required (see below). Python is used to get tweets from Twitter API v2 and store them in a PostgreSQL database. This data is loaded in to a Jupyter Notebook for analysis by using the Pandas library for its DataFrames and various other analytics tools (nltk, Matplotlib, sns, Textblob...)


##Scenario
Pumpkin Spice season is no longer relegated to Autumn. Twitter has something to say about everything, and this should be no different. Find the sentiment across Twitter in regards to Pumpkin Spice products.

##Concepts
- Data Engineering
- ETL (Extract, Transform, Load)
- REST APIs
- Python scripts
- SQL & PostgreSQL
- Docker Containerization
- Jupyter Notebooks
- Pandas
- Data Analysis

##Prerequisites
- Docker (with CLI & Docker-Compose)

##Set-up
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
## Starting the Pipeline

**Note:**If you would like to build a database on a search for something other than 'pumpkin spice', update 'search' in the app/config.py file made earlier. Reference for making a query can be found here:
- [Building queries for Search Tweets](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query)

**First Pipeline**

The first query you wish to make a pipeline for is simple to get started. Navigate to the project's folder in the command line and enter the following command:
```
docker-compose up -d
```
![docker-compose up -d](/static/initialcompose.png)