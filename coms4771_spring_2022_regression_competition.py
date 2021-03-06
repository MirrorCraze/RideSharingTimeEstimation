# -*- coding: utf-8 -*-
"""COMS4771 Spring 2022 Regression Competition

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MbYDAkuljeRKbMdOR6JNuhER9SEtJKL-
"""

from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor
from sklearn.model_selection import cross_val_score,RepeatedKFold,GridSearchCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

import numpy as np
import pandas as pd
import xgboost as xgb
import os

def addDateTime(data):
    data["feature_0"] = data["feature_0"] = pd.to_datetime(data["feature_0"],format = "%m-%d %H:%M:%S")
    data["dayOfWeek"] = (data["feature_0"].dt.dayofweek).astype("float64")
    data["day"] = (data["feature_0"].dt.day).astype("float64")
    data["month"] = data["feature_0"].dt.month.astype("float64")
    data["hour"] = data["feature_0"].dt.hour.astype("float64")
    data["minute"] = data["feature_0"].dt.minute.astype("float64")
    data = data.drop("feature_0",axis = 1)
    return data
def removeCor(data,corrLabel):
    if not corrLabel is None:
        data.drop(labels = corrLabel,axis = 1, inplace = True)
        return data,corrLabel
    else:
        corrMat = data.corr()
        print(corrMat)
        corrLabel = set()
        for i in range(len(corrMat.columns)):
            for j in range(i):
                if abs(corrMat.iloc[i, j]) > 0.8:
                    corrLabel.add(corrMat.columns[i])
        data.drop(labels=corrLabel, axis=1, inplace=True)
        return data,corrLabel
def prepData(data,corrLabel = None):
    data = addDateTime(data)
    #drop ID
    data = data.drop("id",axis = 1)
    data,corrLabel = removeCor(data,corrLabel)
    return data,corrLabel

#preprocessing
train_x = pd.read_csv("train_examples.csv")
train_y = pd.read_csv("train_labels.csv")
test_x = pd.read_csv("test_examples.csv")
train_x,corrLabel = prepData(train_x)
test_x,corrLabel = prepData(test_x,corrLabel)
print(train_x.head())
train_y = train_y.drop("id",axis = 1).values.ravel()
min_max_scaler = preprocessing.MinMaxScaler()
train_x = min_max_scaler.fit_transform(train_x)
test_x = min_max_scaler.transform(test_x)

#model
xg_reg = xgb.XGBRegressor(objective ='reg:squarederror', colsample_bytree= 0.7, learning_rate= 0.4, max_depth= 5, min_child_weight= 4, n_estimators= 300, nthread= 4, silent= 1, subsample= 0.7)
#model = AdaBoostRegressor(base_estimator=DecisionTreeRegressor(max_depth=10) ,n_estimators=100)
#model2 = RandomForestRegressor()
#cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
#n_scores = cross_val_score(model, train_x, train_y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1, error_score='raise')
#print(n_scores)
#model.fit(train_x,train_y)
#model2.fit(train_x,train_y)
#cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
# evaluate model
#scores = cross_val_score(xg_reg, train_x, train_y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
#scores = np.absolute(scores)
#print('Mean MAE: %.3f (%.3f)' % (scores.mean(), scores.std()) )

#print("Fit success!")

#GridSearchCV to find best hyperparameter
"""
xgb1 = xgb.XGBRegressor()
parameters = {'nthread':[4], #when use hyperthread, xgboost may become slower
              'objective':['reg:linear','reg:squarederror','reg:squaredlogerror',],
              'learning_rate': [.03, 0.05, .07], #so called `eta` value
              'max_depth': [5, 6, 7],
              'min_child_weight': [4],
              'silent': [1],
              'subsample': [0.7],
              'colsample_bytree': [0.7],
              'n_estimators': [300,500,1000]}

xgb_grid = GridSearchCV(xgb1,
                        parameters,
                        cv = 3,
                        n_jobs = -1,
                        verbose=True)

xgb_grid.fit(train_x,
         train_y)
print(xgb_grid.best_score_)
print(xgb_grid.best_params_)
"""

xg_reg.fit(train_x,train_y)
test_y = xg_reg.predict(test_x).ravel()
#test_y = model.predict(test_x).ravel()
#test2_y = model2.predict(test_x).ravel()
df_y = pd.DataFrame(data = test_y)
df_y.columns = ["duration"]
df_y.to_csv("test_labels.csv",index=True,index_label="id")
#df2_y = pd.DataFrame(data = test2_y)
#df2_y.columns = ["duration"]
#df2_y.to_csv("test2_labels.csv",index=True,index_label="id")