from datetime import date
from dateutil.relativedelta import relativedelta

from models.data.sql_alchemy import Crew, Production


"""
Dummy crew member for sanity testing
"""
sanity_member = Crew(role='Photographer',
                     full_name='TEST MEMBER SANITY',
                     hire_date=date.today(),
                     fire_date=date.today() + relativedelta(years=2),
                     id=1)


"""
Dummy production for sanity testsing
"""
sanity_prod = Production(title='TEST PROD SANITY',
                         start=date.today() + relativedelta(years=1),
                         end=date.today() + relativedelta(years=2),
                         id=1)
