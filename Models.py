# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 15:35:50 2023

@author: Yousha
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dython import nominal

df = pd.read_csv('data/naukri_final_data.csv')

df.columns
df.drop('Unnamed: 0',axis=1,inplace=True)
columns= ['avg_experience','title', 'company', 'ratings', 'reviews', 'experience', 'salary',
         'location', 'days_posted', 'tags', 'job_simp', 'post','top_20_comp',
         'salary_mentioned', 'reviews_int', 'min_experience', 'max_experience',
         'days_posted_int', 'bangalore', 'delhi', 'kolkata',
         'mumbai', 'remote', 'gurgaon', 'hyderabad', 'noida', 'pune', 'python',
         'sql', 'deep_learning', 'big_data', 'r', 'nlp', 'sas', 'git',
         'tensorflow', 'pytorch', 'tableau', 'power_bi', 'apache', 'c++'
         ]

df = df.reindex(columns, axis='columns')

#cont_corr
plt.figure(figsize=(25,25))
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
sns.heatmap(df.corr(),annot=True,square=True,linewidth=2,cbar_kws={'shrink':0.823})
plt.savefig('plots/Cont_correlation.png',dpi=800,bbox_inches='tight')

# avg_experience
avg_exp = pd.DataFrame(df.corr()['avg_experience'].sort_values(ascending=False))
plt.figure(figsize=(25,25))
sns.heatmap(avg_exp,square=True,linewidth=2,cbar=True,annot=True,annot_kws={'rotation':90})
plt.xticks(fontsize=12,rotation=90)
plt.yticks(fontsize=12,rotation=130)
plt.savefig('plots/avg_exp_correlation.png',dpi=800,bbox_inches='tight')

features =  ['avg_experience','ratings','salary','job_simp', 'post','top_20_comp',
             'salary_mentioned', 'reviews_int','days_posted_int', 'bangalore', 'delhi', 
             'kolkata','mumbai', 'remote', 'gurgaon', 'hyderabad', 'noida', 'pune', 'python',
             'sql', 'deep_learning', 'big_data', 'r', 'nlp', 'sas', 'git',
             'tensorflow', 'pytorch', 'tableau', 'power_bi', 'apache', 'c++'
             ]

ax = plt.figure()
ax = nominal.associations(df[features],figsize=(20,20),title='Feature Correlations')
plt.show()

X = pd.get_dummies(df[features].drop('avg_experience',axis=1))
y = df.avg_experience.values


# Models

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

X_trans = scaler.fit_transform(X)


# Linear Regression
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr2 = LinearRegression()

lr.fit(X,y)
y_pred = lr.predict(X)

lr2.fit(X_trans,y)
y_pred2 = lr2.predict(X_trans)

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error

print(mean_absolute_error(y, y_pred))   # 1.86
print(mean_absolute_error(y, y_pred2))  # 1.86
print(r2_score(y,y_pred))               # 0.27


# train test split for ensemble
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X_trans,y,test_size=.2,random_state=1)


# Random forest
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(random_state=1)

rf.fit(X_train,y_train)  #performs better on unscaled data
y_pred_rf = rf.predict(X_test)

print("rf mae",mean_absolute_error(y_test, y_pred_rf))              # 1.97
print("rf mse",mean_squared_error(y_test,y_pred_rf))                # 7.05
print("rf mae",mean_absolute_percentage_error(y_test,y_pred_rf))    # 0.54
print("rf r2",r2_score(y_test,y_pred_rf))                           # 0.11
print('variance y:',np.var(y))                                      # 8.34
print('variance test set:',np.var(y_test))                          # 7.95

#plot confusion matrix


# Tried using a neural netwrok ... I have no clue how to make this work at the moment.
from sklearn.neural_network import MLPRegressor
mlp = MLPRegressor(hidden_layer_sizes=(100,50), activation='relu', solver='adam', alpha=0.001,max_iter=10000,random_state=1) 

mlp.fit(X_train,y_train)
y_pred_mlp = mlp.predict(X_test)

print("mlp mae",mean_absolute_error(y_test, y_pred_mlp)) # 2.51
print("mlp r2",r2_score(y_test,y_pred_mlp))              # -0.33
print('variance y:',np.var(y))




















