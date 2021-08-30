# device-registry

This project is a REST API web service for registering smart devices.
A home could have multiple kinds of smart devices:
WiFi routers, voice assistants, thermostats, light switches, and even appliances.

This device registry is written in Python using Flask, and it stores data in a SQLite database.
It is the web service used for Chapter 6 in *The Way To Test Software* by Andrew Knight.


## TODO

* Docs
* Tests


## Tests

1. Basic request-response-validate test for '/status/'
   * Set up project
   * Write the test with hard-coding
   * Improve with config file and base URL builder
2. Authentication for '/devices/'
   * Demonstrate GET with and without auth & explain
   * Add credentials to config file
   * Write positive test with auth
   * Write negative test without auth
   * Show auth with tokens
   * Show how to reuse token
   * Discuss if every endpoint should test every type of auth or no-auth
3. CRUD tests with '/devices/<id>'
   * Include negative cases
4. Testing multiple objects with '/devices/'
   * Creating and deleting multiple objects
   * Query parameters for large data
   * Security tests with multiple users
5. Additional REST API factors
   * File downloads
   * HEAD and OPTIONS for GET
   * Invalid methods
   * Handling large bodies with templates
