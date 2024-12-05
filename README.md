# LFU based Web Cache

### Instruction

1. Run `python3 server.py` to execute local server

2. Run `python3 cache.py` to execute web cache

3. Run `python3 client.py` to start the client

4. Enter the file name that you are looking for

    - If file exists, you will see the content on your terminal directly, either provided by cache or server

    - If not, you will receive notification that the file doesn't exists

### Introduction

This simulation helps user to understand the model of cache design by creating a simplified model demonstrating how this architecture works through a **client-cache-server** model.

#### Server
Server is connected to the database where all the original files are stored. Server will accept connection from cache and forward the content to cache.

#### Cache
Cache is connected to the file "cache", which serves as cache storage. 

1. Cache accepts connection from client and search for the required file locally. 

2. If the file does not exists locally, cache will forward the request to server, fetch content and store locally.

#### Client
Client works as a browser behavior, which you can enter your desired content and directly view it on your terminal


 
