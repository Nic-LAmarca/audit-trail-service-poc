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
