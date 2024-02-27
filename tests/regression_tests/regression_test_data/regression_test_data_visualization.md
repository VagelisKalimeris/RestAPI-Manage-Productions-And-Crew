# Regression Test Database Pre-populated Entries Visualisation


## Crew Table Contents

### Existing crew members

| id | full_name         | role     | hire_date | fire_date |
|----|-------------------|----------|-----------|-----------|
| 1  | Quentin Tarantino | Director | now       | end       |
| 2  | Steven Spielberg  | Director | now       | end       |
| 3  | Antony Hopkins    | Actor    | now       | end       |
| 4  | Jason Momoa       | Actor    | now       | end       |
| 5  | Brad Pit          | Actor    | now       | end       |

----


## Productions Table Contents

### Existing Productions

| id | title    | start      | end        |
|----|----------|------------|------------|
| 1  | Iron Man | now + 1yr  | now + 3yrs |
| 2  | Titanic  | now + 2yrs | now + 4yrs |

----


## ProdCrew Table Contents

### Members employed(bound) by existing productions

| prod_id | crew_id |
|---------|---------|
| 1       | 1       |
| 1       | 5       |
| 2       | 2       |
| 2       | 3       |
| 2       | 4       |

----
