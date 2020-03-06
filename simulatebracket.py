# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:09:27 2020

@author: sydne
"""

#Bracket simulation

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from functools import reduce
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import seaborn as sn
import numpy as np

seas_2018 = pd.read_excel('C:\\Users\\sydne\\Downloads\\BracketData (1).xlsx', sheetname='2018')
bdf = pd.read_excel("C:\\Users\\sydne\\Documents\\BracketDf.xlsx")
seas_columns = seas_2018.columns
full_data = pd.read_csv("Documents\\win_loss_bracket.csv")

full_data = full_data[~full_data['srsd'].isnull()] #take out random NAs
X = full_data.drop(columns = ['Home_win', 'Unnamed: 0']) #same steps as in bracket_build.py just creating the model 
y  = full_data['Home_win']
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=0)

logistic_regression= LogisticRegression()
logistic_regression.fit(X_train,y_train)
y_pred=logistic_regression.predict(X_test)
y_probs = logistic_regression.predict_proba(X_test)

for i in enumerate(X.columns):
    print(i[1])
    print(logistic_regression.coef_[0][i[0]])
    



confusion_matrix = pd.crosstab(y_test, y_pred, rownames=['Actual'], colnames=['Predicted'])
sn.heatmap(confusion_matrix, annot=True)
confusion_matrix

def bracket(home, away, df): #same function as in bracket_build.py
    home_df = df[df['School'] == home].reset_index()
    
    away_df = df[df['School'] == away].reset_index()
    
    full_df = pd.merge(home_df, away_df, right_index = True, left_index = True)
    full_df['ngd'] = full_df['NumGames_x'] - full_df['NumGames_y']
    full_df['owd'] = full_df['OverallW_x'] - full_df['OverallW_y']
    full_df['old'] = full_df['OverallL_x'] - full_df['OverallL_y']
    full_df['srsd'] = full_df['SRS_x'] - full_df['SRS_y']
    full_df['sosd'] = full_df['SOS_x'] - full_df['SOS_y']
    full_df['tpd'] = full_df['Team Points_x'] - full_df['Team Points_y']
    full_df['opd'] = full_df['OppPoints_x'] - full_df['OppPoints_y']
    full_df['mpd'] = full_df['MP_x'] - full_df['MP_y']
    full_df['fgpd'] = full_df['FG%_x'] - full_df['FG%_y']
    full_df['orbd'] = full_df['ORB_x'] - full_df['ORB_y']
    full_df['tppd'] = full_df['3P%_x'] - full_df['3P%_y']
    full_df['trbd'] = full_df['TRB_x']-full_df['TRB_y']
    full_df['ad'] = full_df['AST_x'] - full_df['AST_y']
    full_df['sd'] = full_df['STL_x'] - full_df['STL_y']
    full_df['bd'] = full_df['BLK_x'] - full_df['BLK_y']
    full_df['td'] = full_df['TOV_x'] - full_df['TOV_y']
    X = full_df[['ngd','owd','old','srsd','sosd','tpd','opd','mpd','fgpd','orbd','tppd','trbd','ad','sd','bd','td']]
    win = logistic_regression.predict(X)
    if win == 1: 
        winner = home
    if win == 0: 
        winner = away

    prob_win = np.array(logistic_regression.predict_proba(X))
    return([prob_win[0][1], winner])

#the next functions output the list of predicted winners of that respective round but it uses a bernoulli distribution with p = to the logistic regression predicted probability and draws either a 0 or 1 from that

def roundzero_sim(brack_df, game1, game2, game3, game4, seas_df): #this function still outputs a new dataframe with the wild card winners in their respective spot
    zero = brack_df
    win1 = bracket(game1[0], game1[1], seas_df) 
    s1 = np.random.binomial(1, win1[0], 1)
    win2 = bracket(game2[0], game2[1], seas_df)
    s2 = np.random.binomial(1, win2[0], 1)
    win3 = bracket(game3[0], game3[1], seas_df)
    s3 = np.random.binomial(1, win3[0], 1)
    win4 = bracket(game4[0], game4[1], seas_df)
    s4 = np.random.binomial(1, win4[0], 1)
    for index, row in zero.iterrows():
        if row['Team 2'] == 'Game 1':
            if s1 == 1:
                zero.loc[index, 'Team 2'] = game1[0]
            if s1 == 0:
                zero.loc[index, 'Team 2'] = game1[1]
        elif row['Team 2'] == 'Game 2':
            if s2 == 1:
                zero.loc[index, 'Team 2'] = game2[0]
            if s2 == 0:
                zero.loc[index, 'Team 2'] = game2[1]
        elif row['Team 2'] == 'Game 3':
            if s3 == 1:
                zero.loc[index, 'Team 2'] = game3[0]
            if s3 == 0:
                zero.loc[index, 'Team 2'] = game3[1]
        elif row['Team 2'] == 'Game 4':
            if s4 == 1:
                zero.loc[index, 'Team 2'] = game4[0]
            if s4 == 0:
                zero.loc[index, 'Team 2'] = game4[1]
    return(zero)
        
#zero = roundzero(bdf, ['Long Island University', 'Radford'], ['St. Bonaventure', 'UCLA'], ['North Carolina Central', 'Texas Southern'], ['Arizona', 'Syracuse'])

def roundone_sim(zeroth, seas_df): #takes the dataframe outputted from the roundzero_sim function as well as seasons stats
    one = zeroth[zeroth['Round'] == 1] #only look at round 1
    wins_1 = [] #blank list
    for index, row in one.iterrows():
        w = bracket(row['Team 1'], row['Team 2'], seas_df) #remember bracket outputs the probability as well as predicted winner
        s = np.random.binomial(1, w[0], 1) #use the probability output to build bernoulli distribution
        if s == 1: 
            wins_1.append(row['Team 1']) #if you get a 1 from bernoulli team 1 wins
        if s == 0: 
            wins_1.append(row['Team 2']) #if you get a 0 from bernoulli team 2 wins
    return(wins_1)
    
   

#first = roundone(zero)
#first

def roundtwo_sim(firstround, seas_df): #does same thing as roundone_sim but takes the output from round 1
    wins_2 = []
    for i in range(0,31,2):
        w = bracket(firstround[i], firstround[i+1], seas_df)
        s = np.random.binomial(1, w[0], 1)
        if s == 1: 
                wins_2.append(firstround[i])
        if s == 0: 
                wins_2.append(firstround[i+1])
    return(wins_2)

#roundtwo(first)

def roundthree_sim(secondround, seas_df): #same but takes output from round 2
    wins_3 = []
    for i in range(0,15,2):
        w = bracket(secondround[i], secondround[i+1], seas_df)
        s = np.random.binomial(1, w[0], 1)
        if s == 1: 
                wins_3.append(secondround[i])
        if s == 0: 
                wins_3.append(secondround[i+1])
    return(wins_3)

#second = roundtwo(first)

#roundthree(second)


def roundfour_sim(thirdround, seas_df): #same but takes output from round3
    wins_4 = []
    for i in range(0,7,2):
        w = bracket(thirdround[i], thirdround[i+1], seas_df)
        s = np.random.binomial(1, w[0], 1)
        if s == 1: 
                wins_4.append(thirdround[i])
        if s == 0: 
                wins_4.append(thirdround[i+1])
    return(wins_4)

def roundfive_sim(fourthround, seas_df): #same but takes output from round 4
    wins_5 = []
    for i in range(0,3,2):
        w = bracket(fourthround[i], fourthround[i+1], seas_df)
        s = np.random.binomial(1, w[0], 1)
        if s == 1: 
                wins_5.append(fourthround[i])
        if s == 0: 
                wins_5.append(fourthround[i+1])
    return(wins_5)

def champion_sim(fifthround, seas_df): #takes output from round5
    w = bracket(fifthround[0], fifthround[1], seas_df)
    s = np.random.binomial(1,w[0],1)
    if s == 1:
        return(fifthround[0])
    if s == 0:
        return(fifthround[1])
        




#the following fucntion combines all of the functions above in to one and simulates n brackets, and keeps track of how many times 
#each team shows up in each round, then outputs a dataframe of the probability that each team will be in each round

def simulate_bracket_probs(brack_df, game1, game2, game3, game4, n, sdf): #takes the bracket dataframe that i constructed, the wild card games, the number of simulations you want to do, and the dataframe for the season 
    column_names = brack_df['Team 1'].append(brack_df['Team 2'], ignore_index = True)
    column_names = list(column_names)+game1+game2+game3+game4
    #create dataframes for each round that will store whether or not the team showed up in the respective round
    sim_round1 = pd.DataFrame(0, range(0,n), columns=column_names)
    sim_round2 = pd.DataFrame(0, range(0,n), columns = column_names)
    sim_round3 = pd.DataFrame(0, range(0,n), columns = column_names)
    sim_round4 = pd.DataFrame(0, range(0,n), columns = column_names)
    sim_round5 = pd.DataFrame(0, range(0,n), columns = column_names)
    champ = pd.DataFrame(0, range(0,n), columns = column_names)
    #run n loops (essentially build n brackets) and put a 1 when a team makes it to a certain round
    for i in range(0,n):
        zero = roundzero_sim(brack_df = brack_df, game1 = game1, game2 = game2, game3 = game3, game4 = game4, seas_df = sdf)
        first = roundone_sim(zero, seas_df = sdf)
        for elem in first: 
            sim_round1.loc[i,elem] = 1
        second = roundtwo_sim(first, seas_df = sdf)
        for elem2 in second: 
            sim_round2.loc[i,elem2] = 1
            third = roundthree_sim(second, seas_df = sdf)
        for elem3 in third: 
            sim_round3.loc[i, elem3] = 1
        fourth = roundfour_sim(third, seas_df = sdf)
        for elem4 in fourth: 
            sim_round4.loc[i, elem4] = 1
        fifth = roundfive_sim(fourth, seas_df = sdf)
        for elem5 in fifth: 
            sim_round5.loc[i, elem5] = 1
        final = champion_sim(fifth, seas_df = sdf)
        champ.loc[i, final] = 1
        print(i)
    #make dataframes that is the mean of each of the columns of each data frame (which gives proportion of times that team showed up in each round)    
    mean1 = pd.DataFrame(np.mean(sim_round1), columns = ['Round One'])
    mean2 = pd.DataFrame(np.mean(sim_round2), columns = ['Sweet 16'])
    mean3 = pd.DataFrame(np.mean(sim_round3), columns = ['Elite 8'])
    mean4 = pd.DataFrame(np.mean(sim_round4), columns = ['Final 4'])
    mean5 = pd.DataFrame(np.mean(sim_round5), columns = ['Championship'])
    mean6 = pd.DataFrame(np.mean(champ), columns = ['Champ'])
    #combine all these dataframes in to one
    means = [mean1, mean2, mean3, mean4, mean5, mean6]
    all_rounds = pd.concat(means, axis = 1).reset_index()    
    all_rounds['School'] = all_rounds['index']
    return all_rounds.drop(columns = ['index'])
    
#test it out
    
probs_2018 = simulate_bracket_probs(bdf, ['Long Island University', 'Radford'], ['St. Bonaventure', 'UCLA'], ['North Carolina Central', 'Texas Southern'], ['Arizona', 'Syracuse'],10, seas_2018)

#test it out on 2019 bracket dataframe that i constructed 
bdf2019 = pd.read_excel("C:\\Users\\sydne\\Documents\\BracketDf.xlsx", sheetname = '2019')
seas_2019 = pd.read_excel('C:\\Users\\sydne\\Downloads\\BracketData (1).xlsx', sheetname='2019')
seas_2019.columns = seas_columns

probs_2019 = simulate_bracket_probs(bdf2019, ['Prairie View','Fairleigh Dickinson'], ['Belmont','Temple'],['North Dakota State','North Carolina Central'], ['Arizona State',"St. John's (NY)"], 10, seas_2019)

import seaborn as sns
import matplotlib.pyplot as plt
#plot probabilities for each team each round
plt.figure(figsize=(20,10))
chart = sns.barplot(data = probs_2019, x = 'School', y= 'Championship')
chart.set_xticklabels(chart.get_xticklabels(), rotation=90)






