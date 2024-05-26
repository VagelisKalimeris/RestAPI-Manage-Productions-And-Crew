## Purpose
API that enables any tv/movie production company to shoot new shows. Hybrid between a working prototype & portfolio 
  project.
- Provides a way to manage crew, with operations like hire & fire. 
- Enables scheduling of show productions, ensuring that necessary crew is available for their duration, and no 
  personnel conflicts arise.


## Swagger
Run server and visit [this page][swagger].


## Design
Productions have specific start/end dates and crew role requirements. Crew members(employees), have a specific role, 
and can have a set fire date or not(fixed-term or indefinite contract). A crew member can only be working at one 
production, at any given time.

The main challenge with this project was to find an efficient way to relate crew members with production dates.

For instance: 
- To schedule a new production, there need to be available crew members during its date span, for each of role 
  requirements. These crew members must be bound for this timeframe, so they cannot be allocated elsewhere.
- To delete a production, its bound crew members must be released.
- To extend a production's duration, all of its bound crew members must be available during the new timeframe.

Similarly:
- To fire a crew member, they must not be bound by any production after their fire date.
- A crew member cannot be bound to any production after their fire date.
- To inquire crew availability for a specific timeframe, we must gather all crew members that are not bound to any 
  production.

Two main tables were used:

#### CREW

| id | full_name          | role          | hire_date | fire_date  |
|----|--------------------|---------------|-----------|------------|

#### PRODUCTION

| id | title             | start      | end        |
|----|-------------------|------------|------------|

Plus an association table binding crew to productions.  

Using just the association table entries, the dates from main tables, and performing interval overlap calculations, we 
infer validity and perform all required operations.

All complex operations including database writes, have been carefully wrapped in [transactions][sqlite transactions] 
to avoid race conditions.


## Testing
Test client uses an in-memory test database which is always structurally identical to the production database, so there 
is no need to create test database container. 
The test database is being created, pre-populated with specific test suite entries, and destroyed with each single or 
grouped test execution. This applies locally as well as in GitHub or Docker containers. 

Grouped test execution is prioritized by following order:

*Unit* &rarr; *Smoke* &rarr; *Sanity* &rarr; *Regression*. 

All tests are currently being executed in this order by default: 
- On GitHub pushes 
- Between Docker container initialization and server startup

Common route calls exist between sanity & regression layers, but execution through FastApi's TestClient is very 
performant, so there is no need for caching. Merging these 2 test groups would also be a valid approach.


## Limitations

### SQLite
Choosing *SQLite* as this project's database, carried the following drawbacks:
- Absense of nuanced locking mechanisms. To stay clear of race conditions under future concurrent execution 
  environments, serialized transactions were the only available choice.
- No respect for foreign key constraints. As such currently the prod_crew table accepts entries with production & crew 
  primary ids, that might not exist in the respective tables. This inconsistency though, cannot be achieved through
  current implementation, so we can regard this flaw as minor.
- No option of utilizing *asyncio*. The database does not support it.

### No Joins Implementation
No sql table joins were used in queries of the data access code implementation. This design was an experimentation and 
would not use in a production setting. The approach increased add/update production & fire crew member, data access 
code complexity, but extra care and effort was put into making sure time/space efficiency was not sacrificed. 

This choice also shifted weight towards integration testing, since doing dependency injection into current service 
code would be quite tedious.

### No repository layer
Service and repository layers are merged in this implementation. This choice resulted from the combination of the 
following two factors:
- *SQLite*'s lack of support for locking mechanisms(described above).
- No joins implementation(described above).


## Todos

- [ ] Add swagger return schemas
- [ ] User authentication


[swagger]: http://127.0.0.1:80/docs
[sqlite transactions]: https://www.sqlite.org/transactional.html