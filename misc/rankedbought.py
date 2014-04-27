from sqlalchemy import *
import numpy as np
from sqlalchemy.orm import sessionmaker
from churndata import *
from pandas import DataFrame
from util import query_to_df
db = create_engine('sqlite:///forjar.db')
 
def query_to_df(session,query):
    """
    Convert an sql query to a pandas data frame
    """
    result = session.execute(query)
    d = DataFrame(result.fetchall())
    d.columns = result.keys()
    return d
 
metadata = MetaData(db)
 
Session = sessionmaker(bind=db)
 
 
session = Session()
 
 
"""
Counts the users by campaign id
"""
user_dist = session.query(Users)
user_df = query_to_df(session,user_dist)
 


q = session.query(Users.Campaign_ID,Event.Type,Users.id,Event.User_Id).filter(Event.Type == 'bought')
d = query_to_df(session,q)
grouped = d.groupby('Users_Campaign_ID')
print grouped.groups
#result = grouped.agg({'Event_Type' : np.count_nonzero}).sort('Event_Type')
#print result