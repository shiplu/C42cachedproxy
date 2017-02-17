Its a GET endpoint `/events-with-subscriptions/` that combines two separate calls towards the C42 API into one response that contains the event title and the first names of its attendees.

How to start
------------

1. Go to the project directory
2. Create a ini file `config.ini` using following template
    ```
    [DEFAULT]
    user_id = ....
    email = ...
    password = ...
    api_token = ...
    service_id = ...
    event_id = ...
    cache_driver = redis

    [local]
    cache_host = 127.0.0.1
    cache_port = 6379

    ```
3. Create a virtual environment with python 3 as python binary
4. Install requirements `pip install -r requirements.txt`
5. Run the server `python -m cachedproxy.main`. You can find additional options by passing `--help` switch.

Design Consideration
====================

The main cached proxy server is written in Tornado. It stores the external api response in redis.


1. **tornado:**
    tornado is a good framework to build REST api quickly. Its fast. Also it has asynchronous feature. Though we are not going to use it. Creating an API in tornado is dead simple. It uses non-blocking IO. It can scale to tens of thousands of open connections, making it ideal for long polling, WebSockets. It helps mobile platform to save latency and bandwidth.
2. **redis:**
    For caching api response from calendar42 we are storing them in redis. There are other chaching engines as well. But I am choosing redis because we can keep object in it. For other caching engine we either need to serialize our objects or we need a database. Redis has the combination of both.

3. **Consul:**
    We need a configuration server that can change the configuration on the fly. We can do it with file also. But for that we need to write code to update the file every now and then. Consul uses consensus protocol that make sure any node in the cluster has the latest configuration and its distributed to others.

4. **JSON Logging:**
    All the logging in the application code should be machine readable. In this case I prefer JSON lines as its human readable too. JSONlines stays at the middle of the human and machine readability


Process
-------
Each HTTP call to external api should be cached for `4.2` minutes (`252` seconds).
After `4.2` minutes successive calls will maintain `If-Modified-Since` and `If-None-Match` header.
If we get new responose then cache it. If not, then extend the time of cache by
`4.2` minutes. Instead of extending the external api can be called again to get the latest content.
This will save some bandwidth as there may not be updated content. But it'll add latency. 


Todo
====

Caching External API
--------------------
To make the server horizontally scalable we need a distributed cache server.
To save the computation time we can directly save the parsed external api response.
Usually the api will provide response as json text. The json is parsed to dictionary.
Then only the data required for client's response should be kept in the cache server.
Redis will be better choice as every entity we save is a response of an api with some
timing information with it. Like `Last-modified`, `Etag` etc.


Caching Client
--------------
There should be necessary headers so that client can cache it properly.
Dont make it too complex.


Configuration Server
--------------------
All the configuration should be loaded from consul server. If server is not reachable or
not provided it'll fall back to `config.ini` file. The path to `config.ini` should be `/etc/cachedproxy`,
project directory where its found first.


Tests
-----
The code is written tests in mind. So they are testable. All we need is to add tests.


Configuration
-------------
We are mainly reading config from either config.ini or from consul server.
But we are also reading some values from command line. We should only use the command line config when the config is necessary to start the app. Like consul server address