# <p align="center">Pumpkin-Empire:</p>
### A reproducible, modular data pipeline with automatic analytics using Twitter API, Postgres, Streamlit, and Docker
***

## About

A group project to better learn how to build a reproducible ETL data pipeline.

Docker is used to launch the ETL, though some set up is required (see below). Python is used to get tweets from Twitter API v2 and store them in a PostgreSQL database. This data is loaded in to a Jupyter Notebook for analysis by using the Pandas library for its DataFrames and various other analytics tools (nltk, Matplotlib, sns, Textblob...)


## Scenario
Pumpkin Spice season is no longer relegated to Autumn, but how soon is too soon? Twitter has something to say about everything, and this topic is no different. We built a tool to find the sentiment across Twitter in regards to Pumpkin Spice products. 

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
- [Docker](https://docs.docker.com/desktop/install/mac-install/)
- [Twitter API Access](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api)

## Set-up

Download or pull this repository to your desired location.


Create a file called 'config.py' in the app/ folder of this project. This file will hold your Twitter API access information.

![config.py](/static/configpy.png)

Copy the text in the box below to your config.py file and fill out the required fields.


```
# Twitter API Access
consumer_key = "<your consumer key>"
consumer_secret = "<your consumer secret"
access_token = "<your access token>"
access_token_secret = "<you access token secret"
bearer_token = "<your bearer token>"

```



***


**Starting the Pipeline**
---

First, open Docker Dashboard on your computer. 

Getting started is easy. Navigate to the project's folder in the command line and enter the following command:

```
docker-compose up -d
```


> **Note:** The first time you run docker-compose will take a few minutes. This is due to Docker downloading the requirements for each image. If you were to re-compose the image, it would complete much faster.

With that, your pipeline is running. 


**Docker Dashboard**

On the containers tab the pipeline can be seen. 3/3 containers should be running.

![docker dashboard](/static/dockerdashboard.png)

Clicking on the running container shows the processes individually.

![docker containers](/static/dockercontainers.png)


**Adminer**

Adminer is one of the containers inside our docker-compose. This allows us to view the database in a browser. For now it can be used to confirm the creation of our database and tables. After you have populated the database, it can be used to view and search tweets via SQL.

To check if your database has been created, open a browser and enter ```localhost:8080``` in the address bar.

> **Note:** Be sure to change the dropdown box from MySQL to PostgreSQL.

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

**Streamlit Before the First Search**

Designating a search and viewing analytics is done via Streamlit. It runs on your localhost. To start making searches and view analytics open a browser and navigate to: ```localhost:8501```

The database has not yet been populated, so there are no prior topics or tweets for analysis. 

![streamlit start](/static/streamlitstart.png)

Enter your search in the sidebar and click 'Search'. After doing this, Twitter's API will be called, using the credentials that were added to config.py. If you receive an error, please check your credentials. There is also a chance there are no matching tweets for the prior week (the timeline Twitter's free version pulls from).

> **Note:** For this project we search tweets via strings. Using words like AND / OR have special rules. For details on building a query, please refer to:
> 
> [Building queries for searching Tweets](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query)


After you've made an initial search, the database will now have some topics & tweets for analytics. Your most recent search will automatically be passed for analysis.

![Streamlit Analysis](/static/streamlit.png)

Your first search is now listed in the topics select box. Subsequent searches will also be added, so you can access your past searches easily.

![Past search](/static/streamlitpastsearch.png)

We've included various plots, charts, and wordclouds. At the bottom of the page is also an option to view the raw data in table form


From here you can make further searches or explore the data on the Streamlit page or via Adminer.

> **Note:** To add more tweets to a previous topic, search for it again via the search box. The new search results will be added for analysis when that topic is chosen.

**Closing the Pipeline**

To close the pipeline, open Docker Dashboard and click on the Containers tab. From there you can see all running containers, hovering over the pipeline you will see a stop button.


![Docker stop](/static/dockerstop.png)



## Learning Resources

- [Data Engineering](https://www.coursera.org/articles/what-does-a-data-engineer-do-and-how-do-i-become-one)
- [Rest API](https://restfulapi.net)
- [Introduction to SQL](https://www.w3schools.com/sql/sql_intro.asp)
- [Jupyter Notebooks | Pandas](https://towardsdatascience.com/exploratory-data-analysis-with-pandas-and-jupyter-notebooks-36008090d813)
- [Exploratory Analysis](https://towardsdatascience.com/exploratory-data-analysis-8fc1cb20fd15)
- [Streamlit](https://www.analyticsvidhya.com/blog/2020/10/create-interactive-dashboards-with-streamlit-and-python/)
- [Pumpkin Spice](https://www.allrecipes.com/recipe/20476/pumpkin-spice/)