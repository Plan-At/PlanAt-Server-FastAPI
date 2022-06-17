# Feature Specification

### Feature Information
| Key               | Value                                            |
|-------------------|--------------------------------------------------|
| Feature Name      | Plan-At Server                                   |
| Area              | Backend                                          |
| Related Features  | REST API                                         |
| Document Location | https://github.com/Plan-At/PlanAt-Server-FastAPI |
| Spec Status       | Draft                                            |

### Contact Information
| Role      | Name           |
|-----------|----------------|
| Manager   | Chad Magendanz |
| Developer ||

### Revision Summary
| Author | Date       | Version       | Comment                         |
|--------|------------|---------------|---------------------------------|
| -      | 04/19/2022 | Initial Draft | Created this page               |
| -      | 05/11/2022 |               | Update to add more major points |
| -      | 05/20/2022 |               | Add description for new module  |
| -      | 06/10/2022 |               | Finish most of them             |

## Functional Specification
backend server for Plan-At. Developed with the idea of "API First" to allow multiple variation of frontend/client

## Scenario Description


## Feature Description
Sections of the project:

1. Framework Selection:
    For the framework, we wanted a framework that's easy to use and shorten development cycle; 
    Python can produce some results with the fewest lines of code; 
    the FastAPI was created with the idea of "Asynchronous Server Gateway Interface", 
    and as its name, it has relative better performance than other Python based web framework, 
    and we don't really need this server to render actual HTML page. 
    As a result, the dev solely decide to choose FastAPI and set up an environment and repo to began development.
2. Project Breakdown: 
    Our next step was to break down our project into multiple packages, and the priority is to provide some mock data for the frontend team. 
3. Iteration:
    After developed several feature sets, we will teach the frontend how to use it, collect feedback and feature request to make the backend easier to use
4. After period of development, while we're getting more functionality, the code are getting messier, so we rewrite most of the code

## Modules
### User Profile:
Have the 
### Calendar Event:
### Login method:
While static password is the first and default method, after registration user can opt in other methods
- Time-Based OPT (Authenticator)
- GitHub OAuth (email)
### API Documentation:
The framework FastAPI we're using come with native support of [OpenAPI](https://www.openapis.org/),
which including interactive interface with minial amount of explanation about how to use the API like
[Swagger UI](https://swagger.io/tools/swagger-ui/) and [Redoc](https://github.com/Redocly/redoc)
and try-out these endpoints without worrying about CORS


## System Design
### Network Structure
To safeguard our infrastructure, we implemented multiple relay and firewall,
this design will slightly increase in response delay but likely unnoticeable
### Security Measurement
Since all of our operation are REST API based, 
each time interact will require send token,
if the token expired or being revoked, it's not going to work anymore.
### V2 Endpoint
After period of development, while we're getting more functionality, the code are getting messier, 
so it's time to rewrite some of these code
- Break code into smaller file by utilize the Router API
- New URL scheme that describe the action of this endpoint at the end; 
combined public and private endpoint, authenticate based on the token passed-in;
if the request modify any existing data then its POST request, GET is read-only
- Performance is the priority now;
using direct native connection to the database achieved resulted the lowest API latency 
to enjoy the benefit of within same cloud-region,
optimized query to reduce overhead

## Boneyard
### Delayed Features
#### Tagging
Might not a significant feature
#### Schedule Comparison
Since we're still struggling with calendar for just single user

### Permanently Death
#### SQL Database
Somewhat complicated to make SQL query for the data-structure I already made
but seamlessly works with Document-Base NotOnlySQL database, 
plus can immune common SQL-Injection attack
 
