# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 12:29:58 2020

@author: sydne
"""
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import seaborn as sn
import numpy as np

seas_2018 = pd.read_excel('C:\\Users\\sydne\\Downloads\\BracketData.xlsx', sheetname='Sheet1')
bdf = pd.read_excel("C:\\Users\\sydne\\Documents\\BracketDf.xlsx")
seas_columns = seas_2018.columns
print("Column headings:")
print(seas_2018.columns)
full_data = pd.read_csv("Documents\\win_loss_bracket.csv")


full_data = full_data[~full_data['srsd'].isnull()] #take out random NAs
X = full_data.drop(columns = ['Home_win', 'Unnamed: 0']) #predictor variables
y  = full_data['Home_win'] #response variable
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=0) #split into train and test

logistic_regression= LogisticRegression()
logistic_regression.fit(X_train,y_train)#fit on training data
y_pred=logistic_regression.predict(X_test) #predict test data
y_probs = logistic_regression.predict_proba(X_test) #get predicted probs from test data

confusion_matrix = pd.crosstab(y_test, y_pred, rownames=['Actual'], colnames=['Predicted'])
sn.heatmap(confusion_matrix, annot=True)
confusion_matrix #see how accurate the model is

def bracket(home, away, df): #this function takes in two teams and uses the logistic from above to predict if the home team will win or not
    home_df = df[df['School'] == home].reset_index()
    
    away_df = df[df['School'] == away].reset_index()
    
    full_df = pd.merge(home_df, away_df, right_index = True, left_index = True) #merge the home and away statistics 
    full_df['ngd'] = full_df['NumGames_x'] - full_df['NumGames_y'] #the next lines of code basically take the difference of the stats between the home and away team, which is what the modle was built on 
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
    win = logistic_regression.predict(X) #predict if the home team will win or not
    if win == 1: #if the logistic predicts 1 the home team wins
        winner = home
    if win == 0: #if it predicts 0 the away team wins
        winner = away

    prob_win = np.array(logistic_regression.predict_proba(X)) #get the predicted probability for that game
    return([prob_win[0][1], winner]) #print the probability and who is predicted to win
    
bracket('Duke', 'North Carolina', seas_2018)

bdf = pd.read_excel("C:\\Users\\sydne\\Documents\\BracketDf.xlsx", sheetname = '2018') #import the bracket dataframe that i constructed based on the bracket for the given year



def roundzero(brack_df, game1, game2, game3, game4, seas_df): #this fills in the dataframe above with the predicted winners of the wild card games
    zero = brack_df
    win1 = bracket(game1[0], game1[1], seas_df)[1]
    
    win2 = bracket(game2[0], game2[1], seas_df)[1]
     
    win3 = bracket(game3[0], game3[1], seas_df)[1]
    
    win4 = bracket(game4[0], game4[1], seas_df)[1]
    
    for index, row in zero.iterrows():
        if row['Team 2'] == 'Game 1':
            zero.loc[index, 'Team 2'] = win1
                
        elif row['Team 2'] == 'Game 2':
            zero.loc[index, 'Team 2'] = win2
            
        elif row['Team 2'] == 'Game 3':
            zero.loc[index, 'Team 2'] = win3
            
        elif row['Team 2'] == 'Game 4':
            zero.loc[index, 'Team 2'] = win4
    return(zero)
        
zero = roundzero(bdf, ['Long Island University', 'Radford'], ['St. Bonaventure', 'UCLA'], ['North Carolina Central', 'Texas Southern'], ['Arizona', 'Syracuse'], seas_2018)

def roundone(zeroth, seas_df): #creates a list of the round one winners 
    wins_1 = []
    for index, row in zeroth.iterrows():
        w = bracket(row['Team 1'], row['Team 2'], seas_df)[1]
        wins_1.append(w)
        print(wins_1)
    return(wins_1)
    

first = roundone(zero, seas_2018)

def roundtwo(firstround, seas_df): #creates a list of the round two winners from the list of round 1 winners: sweet 16!
    wins_2 = []
    for i in range(0,31,2):
        wins_2.append(bracket(firstround[i], firstround[i+1], seas_df)[1])
    return(wins_2)

second = roundtwo(first, seas_2018)


def roundthree(secondround, seas_df): #creates a list of round three winners from round 2 winners: elite 8! 
    wins_3 = []
    for i in range(0,15, 2):
        wins_3.append(bracket(secondround[i], secondround[i+1], seas_df)[1])
    return(wins_3)


third = roundthree(second, seas_2018)

def roundfour(thirdround, seas_df): #creates a list of fourth round winner from round 3 winners: final 4!
    wins_4 = []
    for i in range(0,7,2):
        wins_4.append(bracket(thirdround[i], thirdround[i+1], seas_df)[1])
    return(wins_4)

fourth = roundfour(third, seas_2018)

def roundfive(fourthround, seas_df): #creates a list of fifth round winners from round 4 winners: championship matchup!
    wins_5 = []
    for i in range(0,3,2):
        wins_5.append(bracket(fourthround[i], fourthround[i+1], seas_df)[1])
    return(wins_5)

fifth = roundfive(fourth, seas_2018)

#Championship!

bracket(fifth[0], fifth[1], seas_2018) #final game from the output of round 5

def simulate_rounds(brack_df, g1, g2, g3, g4, sdf): #combine all of the above functions in to one that will simulate and out put the winners from each rounf
    zero = roundzero(brack_df = brack_df, game1 = g1, game2 = g2, game3 = g3, game4 = g4, seas_df = sdf)
    first = roundone(zero, seas_df =sdf)
    sweet16 = roundtwo(first, seas_df =sdf)
    elite8 = roundthree(sweet16, seas_df =sdf)
    final4 = roundfour(elite8, seas_df =sdf)
    champgame = roundfive(final4, seas_df =sdf)
    champion = bracket(champgame[0], champgame[1], sdf)
    return zero, first, sweet16, elite8, final4, champgame, champion



simulate_rounds(bdf, ['Long Island University', 'Radford'], ['St. Bonaventure', 'UCLA'], ['North Carolina Central', 'Texas Southern'], ['Arizona', 'Syracuse'], seas_2018)

bdf2019 = pd.read_excel("C:\\Users\\sydne\\Documents\\BracketDf.xlsx", sheetname = '2019') #2019 bracket data that i constructed

seas_2019 = pd.read_excel('C:\\Users\\sydne\\Downloads\\BracketData (1).xlsx', sheetname='2019') #2019 season data 
seas_2019.columns = seas_columns #rename columns

simulate_rounds(bdf2019, ['Prairie View','Fairleigh Dickinson'], ['Belmont','Temple'],['North Dakota State','North Carolina Central'], ['Arizona State',"St. John's (NY)"], seas_2019) #test it out







