
# A Simulation of Cache/P2P Node Behavior

Meng Li & Ziyi Xin

## Objective
Write a program to simulate the behavior of the cache. In which the cache should be able to:
1. Establish connection between clients and target server
2. Retrieve content that is requried by client from server.
3. Save a copy of the content locally. 
4. Whenvever the content that is stored locally is being requested by the client, directly deliver the content without reaching server. 
5. Dynamicaly sort the content stored locally by visit frequency and delete least frequently used content when cache is fully occupied (LFU Method). 

## Significance:
This simulation helps user to understand the model of cache design by creating a simplified model demonstrating how this architecture works. Users are also able to investigate how cache manage its content dynamicaly by tracing the content inside the cache. 

## Methodology
This model will be designed using socekt programming through python. We will implement a cache that can listen and forward the request between client and server while store data locally. 

The data will be simulated through dictionaries. We will create a large dictionary with various elements. Users will requrie specific elements inside dictionary and cache will be able to retrieve it from server and store it in a sub-dictionary locally for future use. 

## Delivery
We will handin a code of our cache proxy and its corresponding test client and server for the simulation. README file will also be provided that include the detail instruction on how to test and explanation of the cache behavior.

