# Imports
import pandas as pd
import seaborn as sns
import seaborn.objects as so
from db_config import get_redis_connection
import secrets1
import redis as r
import json
import requests
import yaml
from redis.commands.json.path import Path
import csv
import matplotlib.pyplot as plt

# Color codes for plotting data
red = '#ef4444'
green = '#84cc16'
orange = '#fb923c'
blue = '#22d3ee'
gray = '#475569'

class Redis:

    def __init__(self):

        self.redisConnection = get_redis_connection()
        self.flushAllFromRedis()
    
    def insertDataIntoRedis(self,key,value):

        self.redisConnection.json().set(key,'.',json.dumps(value))
        
    def flushAllFromRedis(self):

        self.redisConnection.flushall()

    def getDataFromRedis(self,key):
        
        json_data = self.redisConnection.json().get(key)
        return json.loads(json_data)
    
    def keys(self):

        return self.redisConnection.keys()    
    

def main():
    '''
    Main
    '''

    # Make CSV into Pandas
    df = pd.read_csv("Movies (1970-2023).csv",names=['movie title', 'director', 'rating', 'genres', 'language cinema', 'votes', 'year', 'runtime'])

    # Filter out only what we want
    df.dropna()

    list_of_dicts = df.to_dict(orient='records')

    print(list_of_dicts)

    localRedis = Redis()

    for movie in range(len(list_of_dicts)):
        key = f"movie:{movie}"
        localRedis.insertDataIntoRedis(key,list_of_dicts[movie])

    keys = localRedis.keys()

    redisData = []
    for key in keys:
        redisInstance = localRedis.getDataFromRedis(key)
        redisData.append(redisInstance)

    df = pd.DataFrame().from_dict(redisData)

    processing1(df)
    
    processing2(df)
    
    processing3(df)

def processing1(df):
    # Rating vs Year
    plt.figure(figsize=(10, 6))
    plt.scatter(df['year'], df['rating'], color='blue')
    plt.title('Rating vs Year')
    plt.xlabel('Year')
    plt.ylabel('Rating')
    plt.grid(True)
    plt.show()

def processing2(df):
    # Votes vs Runtime
    plt.figure(figsize=(10, 6))
    plt.scatter(df['runtime'], df['votes'], color='green')
    plt.title('Votes vs Runtime')
    plt.xlabel('Runtime')
    plt.ylabel('Votes')
    plt.grid(True)
    plt.show()

def processing3(df):
    # Bar chart for number of movies per director
    plt.figure(figsize=(10, 6))
    df['director'].value_counts().plot(kind='bar', color='purple')
    plt.title('Number of Movies per Director')
    plt.xlabel('Director')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

main()