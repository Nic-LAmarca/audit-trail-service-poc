# audit-trail-service
This repository contains the completed code for the take-home assignment given to me in the Canonical Interview process. Based on the information provided to me, I have scoped out the work according to my understanding as follows:

**User Story:**

As a developer, I want to build an audit trail service capable of receiving, storing, and retrieving audit log events for other microservices, so that I can track audit events efficiently.

**Acceptance Criteria:**
- Build a POC HTTP server(in Python or Go) to receive, store, and retrieve audit log events for microservices
  - The server should expose endpoints to create and fetch audit events
  - Ensure that the server can handle concurrent requests
  
- Use a data storage mechanism that is concurrency-safe
  - for POC purposes, it can be an in-memory database
    
- Develop a schema for audit log events
  - Capture invariant data(event type, timestamp, client/service, eventId, etc.)
  - Capture variant data(app-specific)
  
- Document the microservice API
  - Provide clear API documentation with examples of request and response formats
  - Add TODO comments in the code for areas that need improvement or additional features
    
- Deploy the solution for testing
  - Provide a public URL for accessing the running instance of the service
  - Provide a private archive of the source code

**How to Use this Audit Trail Service:**

I have created 3 endpoints for this service, documentation and sample request values for which may be seen in the routes.py file. At a high level they are as follows:

- **POST /event**
  This API allows a user to add a new AuditLogEvent entry to the database.

- **GET /event/<event_id>** 
  This API allows a user to retrieve an AuditLogEvent entry by its unique event_id.

- **GET /events**
  This API allows a user to retreive all AuditLogEvent entries present in the database. 

Testing of the above may be complete at the following URL: https://audit-trail-service-8a163c91f080.herokuapp.com/
Note: You will want to create entries with the POST /event API first to then retrieve from. You can run the GET /events API to get the event_id value(s) for an existing event to then use
in the GET /event/<event_id> API. 
I will include the sample Postman API collection I created to test this deployed code. 

**Final Notes:**

I have left TODO comments throughout the code indicating items I would like to expand upon and discuss if I were to build out this service beyond a POC that meets the acceptance criteria. 
In addition to the TODOs, I have a few thoughts with respect to operability and scalability of this service that I would focus on given the time and resources to do so:

- I would want to implement some form of logging for the service to to improve ease of tracking and debugging issues.
- Integrating monitoring tools to observe application performance would also provide useful insight for areas of improvement.
- Adding more intensive error handling to prevent crashes, and more time invested in the consistency and quality of error messages presented.
- Developing with at least a 2 trunk flow- develop and master.
- Using Swagger/OpenAPI for generating interactive API documentation.
- Testing: unit tests, integration tests, end-to-end testing, automated tests in a CI/CD pipeline.
- Implementation of user authorization & authentication to enhance security.
- Utilizng configuration files for the management of sensitive information, environment variables, etc. 
- Indexing within the database and immplementing caches to improve performance.
- Use load balancers to evenly distribute incoming traffic.
- etc. 

Thanks for reading! 
