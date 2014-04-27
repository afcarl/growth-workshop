from __future__ import division
import matplotlib.pyplot as plt
from sqlalchemy import *
import numpy as np
from sklearn.linear_model import LogisticRegression
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sklearn.metrics import confusion_matrix
from sklearn.cross_validation import train_test_split
from churndata import *
from sklearn.preprocessing import StandardScaler
from pandas import DataFrame,Series
from pandas.core.groupby import GroupBy
from util import query_to_df,vectorize_index
from util import *
db = create_engine('sqlite:///forjar.db')
 
 
metadata = MetaData(db)
 
Session = sessionmaker(bind=db)
 
 
session = Session()

def vectorize(df,label_column):
    """
    Vectorize input features wrt a label column.
    """
    feature_names = {f for f in df.columns.values if f != label_column}
    inputs = df[feature_names].index
    return inputs

def vectorize_label(df,label_column,num_labels,target_outcome):
    """
    Vectorize input features wrt a label column.
    """
    inputs = df[label_column].apply(lambda x: x== target_outcome).values

    return inputs



 
"""
We only want events and users such that the user bought an item.
We count bought as $1 of revenue for simplicity.
"""
 
q = session.query(Users.Campaign_ID,Meal.Type,Event.Type).limit(300)
 
"""
Print out the counts by name.
This is a way of showing how to aggregate by campaign ids.
"""
df = query_to_df(session,q)

def binarize(x):
    if x == 'bought':
        return 1
    return 0

df['Event_Type'] = df['Event_Type'].map(binarize)

print df



transform_column(df,'Users_Campaign_ID',campaign_to_num.get)
transform_column(df,'Meal_Type',meal_to_num.get)



print df
"""
Prediction scores.
 
"""


def vectorize_feature_index(df,label_column):
    feature_names = {f for f in df.columns.values if f != label_column}
    X = df[feature_names].index
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    train_index,test_index = train_test_split(df.index)
    X = df[feature_names].as_matrix().as_type(np.float)
    y = df[label_column].index
    y_test = y[test_index].astype(float)


vectorize_index(df,'Event_Type')

print X