from datetime import date
from dateutil.relativedelta import relativedelta

from app.models.data.sql_alchemy_models import Crew, Production, ProdCrew


"""
Dummy crew members for regression testing.
"""
regression_crew = [
    Crew(role='Director',
         full_name='Quentin Tarantino',
         hire_date=date.today(),
         fire_date=date.max,
         id=1),
    Crew(role='Director',
         full_name='Steven Spielberg',
         hire_date=date.today(),
         fire_date=date.max,
         id=2),
    Crew(role='Actor',
         full_name='Antony Hopkins',
         hire_date=date.today(),
         fire_date=date.max,
         id=3),
    Crew(role='Actor',
         full_name='Jason Momoa',
         hire_date=date.today(),
         fire_date=date.max,
         id=4),
    Crew(role='Actor',
         full_name='Brad Pitt',
         hire_date=date.today(),
         fire_date=date.max,
         id=5)
]


"""
Dummy productions for regression testing.
"""
regression_prods = [
    Production(title='Iron Man',
               start=date.today() + relativedelta(years=1),
               end=date.today() + relativedelta(years=3),
               id=1),
    Production(title='Titanic',
               start=date.today() + relativedelta(years=2),
               end=date.today() + relativedelta(years=4),
               id=2)
]

"""
Dummy prod/crew bindings for regression testing.
"""
regression_bindings = [
    # First prod bindings
    ProdCrew(prod_id=1, crew_id=1),
    ProdCrew(prod_id=1, crew_id=5),
    # Second prod bindings
    ProdCrew(prod_id=2, crew_id=2),
    ProdCrew(prod_id=2, crew_id=3),
    ProdCrew(prod_id=2, crew_id=4)
]
