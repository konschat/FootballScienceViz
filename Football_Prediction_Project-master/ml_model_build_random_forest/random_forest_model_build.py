# -*- coding: utf-8 -*-
"""
Created on Sun May 10 15:59:55 2020

@author: mhayt
"""


print('\n\n ---------------- START ---------------- \n')

#-------------------------------- API-FOOTBALL --------------------------------

#!/usr/bin/python
from os.path import dirname, realpath, sep, pardir
import sys
sys.path.append(dirname(realpath(__file__)) + sep + pardir + sep)

import time
start=time.time()

from ml_functions.ml_model_eval import pred_proba_plot, plot_cross_val_confusion_matrix, plot_learning_curve
from ml_functions.data_processing import scale_df
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, plot_confusion_matrix, accuracy_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, cross_val_predict
import pandas as pd

plt.close('all')


#------------------------------- INPUT VARIABLES ------------------------------

df_5_saved_name = '2019_2020_2021_2022_prem_df_for_ml_5_v2.txt'
df_10_saved_name = '2019_2020_2021_2022_prem_df_for_ml_10_v2.txt'

grid_search = False

pred_prob_plot_df10 = False
save_pred_prob_plot_df10 = False
pred_prob_plot_df5 = False
save_pred_prob_plot_df5 = False

save_conf_matrix_df10 = False
save_conf_matrix_df5 = False

save_learning_curve_df10 = False
save_learning_curve_df5 = False

create_final_model = True


#------------------------------- ML MODEL BUILD -------------------------------

#importing the data and creating the feature dataframe and target series

with open(f'../prem_clean_fixtures_and_dataframes/{df_5_saved_name}', 'rb') as myFile:
    df_ml_5 = pickle.load(myFile)

with open(f'../prem_clean_fixtures_and_dataframes/{df_10_saved_name}', 'rb') as myFile:
    df_ml_10 = pickle.load(myFile)
    
    
#scaling dataframe to make all features to have zero mean and unit vector.
df_ml_10 = scale_df(df_ml_10, list(range(14)), [14,15,16])
df_ml_5 = scale_df(df_ml_5, list(range(14)), [14,15,16])

x_10 = df_ml_10.drop(['Fixture ID', 'Team Result Indicator', 'Opponent Result Indicator'], axis=1)
y_10 = df_ml_10['Team Result Indicator']

x_5 = df_ml_5.drop(['Fixture ID', 'Team Result Indicator', 'Opponent Result Indicator'], axis=1)
y_5 = df_ml_5['Team Result Indicator']


#------------------------------- RANDOM FOREST --------------------------------


def rand_forest_train(df, print_result=True, print_result_label=''):

    #create features matrix
    x = df.drop(['Fixture ID', 'Team Result Indicator', 'Opponent Result Indicator'], axis=1)
    y = df['Team Result Indicator']
    
    #instantiate the random forest class
    clf = RandomForestClassifier(max_depth=4, max_features=4, n_estimators=120)
    
    #split into training data and test data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    
    #train the model
    clf.fit(x_train, y_train)
    
    if print_result:
        print(print_result_label)
        #training data
        train_data_score = round(clf.score(x_train, y_train) * 100, 1)
        print(f'Training data score = {train_data_score}%')
        
        #test data
        test_data_score = round(clf.score(x_test, y_test) * 100, 1)
        print(f'Test data score = {test_data_score}% \n')
    
    return clf, x_train, x_test, y_train, y_test


ml_10_rand_forest, x10_train, x10_test, y10_train, y10_test = rand_forest_train(df_ml_10, print_result_label='DF_ML_10')
ml_5_rand_forest, x5_train, x5_test, y5_train, y5_test = rand_forest_train(df_ml_5, print_result_label='DF_ML_5')


# ---------- ENSEMBLE MODELLING ----------

#In this section we will combine the results of using the same algorithm but with different input data used to train the model. The features are still broadly the same but have been averaged over a different number of games df_ml_10 is 10 games, df_ml_5 is 5 games. 

#reducing fixtures in df_ml_5 to contain only the fixtures within df_ml_10 and training that new dataset
df_ml_5_dropto10 = df_ml_5.drop(list(range(0,50)))
ml_5_to10_rand_forest, x5_to10_train, x5_to10_test, y5_to10_train, y5_to10_test = rand_forest_train(df_ml_5_dropto10, print_result=False)

#making predictions using the two df inputs independantly
y_pred_ml10 = ml_10_rand_forest.predict(x10_test)
y_pred_ml5to10 = ml_5_to10_rand_forest.predict(x10_test)

#making probability predictions on each of the datasets independantly
pred_proba_ml10 = ml_10_rand_forest.predict_proba(x10_test)
pred_proba_ml5_10 = ml_5_to10_rand_forest.predict_proba(x10_test)

#combining independant probabilities and creating combined class prediction
pred_proba_ml5and10 = (np.array(pred_proba_ml10) + np.array(pred_proba_ml5_10)) / 2.0
y_pred_ml5and10 = np.argmax(pred_proba_ml5and10, axis=1)

#accuracy score variables
y_pred_ml10_accuracy = round(accuracy_score(y10_test, y_pred_ml10), 3) * 100
y_pred_ml5to10_accuracy = round(accuracy_score(y10_test, y_pred_ml5to10), 3) * 100
y_pred_ml5and10_accuracy = round(accuracy_score(y10_test, y_pred_ml5and10), 3) * 100

print('ENSEMBLE MODEL TESTING')
print(f'Accuracy of df_10 alone = {y_pred_ml10_accuracy}%')
print(confusion_matrix(y10_test, y_pred_ml10), '\n')
print(f'Accuracy of df_5 alone = {y_pred_ml5to10_accuracy}%')
print(confusion_matrix(y10_test, y_pred_ml5to10), '\n')
print(f'Accuracy of df_5 and df_10 combined = {y_pred_ml5and10_accuracy}%')
print(confusion_matrix(y10_test, y_pred_ml5and10), '\n\n')


# ---------- GRID SEARCH ----------

if grid_search:
    param_grid_grad = [{'n_estimators':list(range(50,200,50)),
                        'max_depth':list(range(1,5,1)),
                        'max_features':list(range(2,5,1))}]
    param_grid_grad = [{'n_estimators':list(range(10,200,10))}]
    
    #random forest gridsearch 
    grid_search_grad = GridSearchCV(ml_10_rand_forest, 
                                    param_grid_grad, 
                                    cv=5, 
                                    scoring = 'accuracy', 
                                    return_train_score = True)
    grid_search_grad.fit(x_10, y_10)
    
    #Output best Cross Validation score and parameters from grid search
    print('\n', 'Gradient Best Params: ' , grid_search_grad.best_params_)
    print('Gradient Best Score: ' , grid_search_grad.best_score_ , '\n')


#------------------------------- MODEL EVALUATION -----------------------------

#cross validation
skf = StratifiedKFold(n_splits=5, shuffle=True)

cv_score_av = round(np.mean(cross_val_score(ml_10_rand_forest, x_10, y_10, cv=skf))*100,1)
print('Cross-Validation Accuracy Score ML10: ', cv_score_av, '%\n')

cv_score_av = round(np.mean(cross_val_score(ml_5_rand_forest, x_5, y_5, cv=skf))*100,1)
print('Cross-Validation Accuracy Score ML5: ', cv_score_av, '%\n')


# ---------- PREDICTION PROBABILITY PLOTS ----------

if pred_prob_plot_df10:
    fig = pred_proba_plot(ml_10_rand_forest, 
                          x_10, 
                          y_10, 
                          no_iter=50, 
                          no_bins=36, 
                          x_min=0.3, 
                          classifier='Random Forest (ml_10)')
    if save_pred_prob_plot_df10:
        fig.savefig('figures/ml_10_random_forest_pred_proba.png')

if pred_prob_plot_df5:
    fig = pred_proba_plot(ml_5_rand_forest, 
                          x_5, 
                          y_5, 
                          no_iter=50, 
                          no_bins=35, 
                          x_min=0.3, 
                          classifier='Random Forest (ml_5)')
    if save_pred_prob_plot_df5:
        fig.savefig('figures/ml_5_random_forest_pred_proba.png')


# ---------- CONFUSION MATRIX PLOTS ----------

#modified to take cross-val results.

plot_cross_val_confusion_matrix(ml_10_rand_forest, 
                                x_10, 
                                y_10, 
                                display_labels=('team loses', 'draw', 'team wins'), 
                                title='Random Forest Confusion Matrix ML10', 
                                cv=skf)
if save_conf_matrix_df10:
    plt.savefig('figures\ml_10_confusion_matrix_cross_val_random_forest.png')

plot_cross_val_confusion_matrix(ml_5_rand_forest, 
                                x_5, 
                                y_5, 
                                display_labels=('team loses', 'draw', 'team wins'), 
                                title='Random Forest Confusion Matrix ML5', 
                                cv=skf)
if save_conf_matrix_df5:
    plt.savefig('figures\ml_5_confusion_matrix_cross_val_random_forest.png')


# ---------- LEARNING CURVE PLOTS ----------

plot_learning_curve(ml_10_rand_forest, 
                    x_10, 
                    y_10, 
                    training_set_size=20, 
                    x_max=600, 
                    title='Learning Curve - Random Forest DF_10')
if save_learning_curve_df10:
    plt.savefig('figures\ml_10_random_forest_learning_curve.png')

plot_learning_curve(ml_5_rand_forest, 
                    x_5, 
                    y_5, 
                    training_set_size=20, 
                    x_max=600, 
                    title='Learning Curve - Random Forest DF_5')
if save_learning_curve_df5:
    plt.savefig('figures\ml_5_random_forest_learning_curve.png')


# ---------- FEATURE IMPORTANCE ----------

fi_ml_10 = pd.DataFrame({'feature': list(x10_train.columns),'importance': ml_10_rand_forest.feature_importances_}).sort_values('importance', ascending = False)

fi_ml_5 = pd.DataFrame({'feature': list(x5_train.columns),'importance': ml_5_rand_forest.feature_importances_}).sort_values('importance', ascending = False)


#--------------------------------- FINAL MODEL --------------------------------

#in this section we will take the learnings from the hyperparameter testing above and train a final model using 100% of the data. This model may then be used for predictions going forward.

if create_final_model:
    
    #intantiating and training the df_5 network
    ml_5_rf = RandomForestClassifier(max_depth=4, max_features=4, n_estimators=120)
    ml_5_rf.fit(x_5, y_5)
    
    #intantiating and training the df_10 network
    ml_10_rf = RandomForestClassifier(max_depth=4, max_features=4, n_estimators=120)
    ml_10_rf.fit(x_10, y_10)
    
    with open('ml_models/random_forest_model_5.pk1', 'wb') as myFile:
        pickle.dump(ml_5_rf, myFile)

    with open('ml_models/random_forest_model_10.pk1', 'wb') as myFile:
        pickle.dump(ml_10_rf, myFile)


# ----------------------------------- END -------------------------------------

print('\n', 'Script runtime:', round(((time.time()-start)/60), 2), 'minutes')
print(' ----------------- END ----------------- \n')
