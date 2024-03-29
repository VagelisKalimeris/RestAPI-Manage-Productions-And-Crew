## Purpose

- API that enables any tv/movie production company to shoot new shows. 
- Hybrid between a working prototype & portfolio project.
- Provides a way to manage crew, with operations like hire & fire. 
- Enables scheduling of show productions, ensuring that necessary crew is available for their duration, and no 
  personnel conflicts arise.


---
### Requires Python 3.11

--- 
## Design Choices & Limitations

### SQLite
Choosing *SQLite* as the database, carried the following:

#### Benefits
- Lightweight execution & no need for separate *Docker* container.
- Fast and trusted integration testing. See dedicated section below for more info.

#### Drawbacks
- Absense of nuanced locking mechanisms. To ensure db integrity under concurrent execution environments, transactions 
  were the only available choice. See dedicated section below for how this further affected design. 
- No respect for foreign key constraints. As such currently the prod_crew table accepts entries with production & crew 
  primary ids, that might not exist in the respective tables. This inconsistency though, cannot be achieved through
  current implementation, so we can regard this flow as minor.
- No option of utilizing *asyncio*, since the database does not support it.  

### Role of BL
Initial design intention was for DAL to not contain any complex logic, but only simple queries. The BL was meant to 
implement the complexity of operations such as production scheduling, by reusing some of DAL's simple functionality. 

The intention clashed with *SQLite*'s lack of support for locking mechanisms(described above). Since transactions were 
the only way to ensure safety under concurrency, to achieve this design, the DAL functions would in some cases need to 
return without committing. It was chosen to avoid this design, to not heavily break separation between the 2 layers. 

As such, at this point BL has no functional role, and could easily be removed, but since it adds no complexity or 
performance hit, is left available for future use.  

### No Joins
No sql table joins were used in queries of this DAL implementation, mostly as a challenge! The approach increased 
add/update production & fire crew member, DAL code complexity, but extra care and effort was put into making sure 
time/space efficiency was not sacrificed. 

This choice also shifted weight towards integration testing, since doing dependency injection into current DAL would be
quite tedious.


## API Documentation
Run server and visit [this page](http://127.0.0.1:8000/docs).


## Testing
Test client uses an in-memory test database which is always structurally identical to the production database, so there 
is no need to worry about any divergence or sql incompatibilities between production and test databases. The test 
database is being created, populated according to test type, and destroyed with each single or grouped test execution.

Grouped test execution is prioritized by following order:

*Unit* &rarr; *Smoke* &rarr; *Sanity* &rarr; *Regression*. 

All tests are being executed in this order by default: 
- On GitHub pushes 
- At Docker container startup.

There exist common route calls between the sanity & regression layers but execution through FastApi TestClient is very 
performant, so there is no need for design with a more complex solution like caching, in this case. Merging these 2 
layers would also be a valid approach.