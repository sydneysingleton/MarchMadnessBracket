# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 14:40:09 2020

@author: sydne
"""

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
#just replace path strings with path to data files
path1 = "C:\\Users\\sydne\\Downloads\\BracketData (1).xlsx" #path to the seasons stats
path2 = "C:\\Users\\sydne\\Downloads\\Elo_Data.csv" #path to the game results dataset
seas_2018 = pd.read_excel(path1, sheetname='2018')

seas_columns = seas_2018.columns
print("Column headings:")
print(seas_2018.columns)

game_results = pd.read_csv(path2)
print(game_results.columns)
game_results = game_results[game_results['Year'] == '2017-18']
game_results = game_results[['Schl','Opp','Unnamed: 8']]

game_results['game_id']= range(0,5327)
home_data = pd.merge(game_results, seas_2018, left_on = "Schl", right_on = "School")
full_data = pd.merge(home_data, seas_2018, left_on = 'Opp', right_on= 'School')

print(full_data.columns)

full_data['ngd'] = full_data['NumGames_x'] - full_data['NumGames_y']
full_data['owd'] = full_data['OverallW_x'] - full_data['OverallW_y']
full_data['old'] = full_data['OverallL_x'] - full_data['OverallL_y']
full_data['srsd'] = full_data['SRS_x'] - full_data['SRS_y']
full_data['sosd'] = full_data['SOS_x'] - full_data['SOS_y']
full_data['tpd'] = full_data['Team Points_x'] - full_data['Team Points_y']
full_data['opd'] = full_data['OppPoints_x'] - full_data['OppPoints_y']
full_data['mpd'] = full_data['MP_x'] - full_data['MP_y']
full_data['fgpd'] = full_data['FG%_x'] - full_data['FG%_y']
full_data['orbd'] = full_data['ORB_x'] - full_data['ORB_y']
full_data['tppd'] = full_data['3P%_x'] - full_data['3P%_y']
full_data['trbd'] = full_data['TRB_x']-full_data['TRB_y']
full_data['ad'] = full_data['AST_x'] - full_data['AST_y']
full_data['sd'] = full_data['STL_x'] - full_data['STL_y']
full_data['bd'] = full_data['BLK_x'] - full_data['BLK_y']
full_data['td'] = full_data['TOV_x'] - full_data['TOV_y']




full_data['Home_win'] = full_data['Unnamed: 8']
full_data = full_data.drop(columns = ['Unnamed: 8'])


full_data['Home_win'] = full_data['Home_win'].map({'W':1, "L": 0})

up_samp = full_data[full_data['Home_win'] == 0]

full_data = pd.concat([full_data, up_samp], axis = 0)

full_data = full_data[['ngd','owd','old','srsd','sosd','tpd','opd','mpd','fgpd','orbd','tppd','trbd','ad','sd','bd','td','Home_win']]


#repeat above for past years to get more data for the model 


seas_2017 = pd.read_excel(path1, sheetname='2017')
seas_2017.columns = seas_columns

print("Column headings:")
print(seas_2017.columns)

game_results = pd.read_csv(path2)
print(game_results.columns)
game_results17 = game_results[game_results['Year'] == '2016-17']
game_results17 = game_results17[['Schl','Opp','Unnamed: 8']]

game_results17['game_id']= range(0,5298)
home_data17 = pd.merge(game_results17, seas_2017, left_on = "Schl", right_on = "School")
full_data17 = pd.merge(home_data17, seas_2017, left_on = 'Opp', right_on= 'School')

print(full_data17.columns)

full_data17['ngd'] = full_data17['NumGames_x'] - full_data17['NumGames_y']
full_data17['owd'] = full_data17['OverallW_x'] - full_data17['OverallW_y']
full_data17['old'] = full_data17['OverallL_x'] - full_data17['OverallL_y']
full_data17['srsd'] = full_data17['SRS_x'] - full_data17['SRS_y']
full_data17['sosd'] = full_data17['SOS_x'] - full_data17['SOS_y']
full_data17['tpd'] = full_data17['Team Points_x'] - full_data17['Team Points_y']
full_data17['opd'] = full_data17['OppPoints_x'] - full_data17['OppPoints_y']
full_data17['mpd'] = full_data17['MP_x'] - full_data17['MP_y']
full_data17['fgpd'] = full_data17['FG%_x'] - full_data17['FG%_y']
full_data17['orbd'] = full_data17['ORB_x'] - full_data17['ORB_y']
full_data17['tppd'] = full_data17['3P%_x'] - full_data17['3P%_y']
full_data17['trbd'] = full_data17['TRB_x']-full_data17['TRB_y']
full_data17['ad'] = full_data17['AST_x'] - full_data17['AST_y']
full_data17['sd'] = full_data17['STL_x'] - full_data17['STL_y']
full_data17['bd'] = full_data17['BLK_x'] - full_data17['BLK_y']
full_data17['td'] = full_data17['TOV_x'] - full_data17['TOV_y']




full_data17['Home_win'] = full_data17['Unnamed: 8']
full_data17 = full_data17.drop(columns = ['Unnamed: 8'])


full_data17['Home_win'] = full_data17['Home_win'].map({'W':1, "L": 0})

full_data17 = full_data17[['ngd','owd','old','srsd','sosd','tpd','opd','mpd','fgpd','orbd','tppd','trbd','ad','sd','bd','td','Home_win']]

full_data = pd.concat([full_data, full_data17], axis = 0)

###########################################

seas_2016 = pd.read_excel(path1, sheetname='2016')
seas_2016.columns = seas_columns

print("Column headings:")
print(seas_2016.columns)

game_results = pd.read_csv(path2)
print(game_results.columns)
game_results16 = game_results[game_results['Year'] == '2015-16']
game_results16 = game_results16[['Schl','Opp','Unnamed: 8']]

game_results16['game_id']= range(0,5288)
home_data16 = pd.merge(game_results16, seas_2016, left_on = "Schl", right_on = "School")
full_data16 = pd.merge(home_data16, seas_2016, left_on = 'Opp', right_on= 'School')

print(full_data16.columns)

full_data16['ngd'] = full_data16['NumGames_x'] - full_data16['NumGames_y']
full_data16['owd'] = full_data16['OverallW_x'] - full_data16['OverallW_y']
full_data16['old'] = full_data16['OverallL_x'] - full_data16['OverallL_y']
full_data16['srsd'] = full_data16['SRS_x'] - full_data16['SRS_y']
full_data16['sosd'] = full_data16['SOS_x'] - full_data16['SOS_y']
full_data16['tpd'] = full_data16['Team Points_x'] - full_data16['Team Points_y']
full_data16['opd'] = full_data16['OppPoints_x'] - full_data16['OppPoints_y']
full_data16['mpd'] = full_data16['MP_x'] - full_data16['MP_y']
full_data16['fgpd'] = full_data16['FG%_x'] - full_data16['FG%_y']
full_data16['orbd'] = full_data16['ORB_x'] - full_data16['ORB_y']
full_data16['tppd'] = full_data16['3P%_x'] - full_data16['3P%_y']
full_data16['trbd'] = full_data16['TRB_x']-full_data16['TRB_y']
full_data16['ad'] = full_data16['AST_x'] - full_data16['AST_y']
full_data16['sd'] = full_data16['STL_x'] - full_data16['STL_y']
full_data16['bd'] = full_data16['BLK_x'] - full_data16['BLK_y']
full_data16['td'] = full_data16['TOV_x'] - full_data16['TOV_y']




full_data16['Home_win'] = full_data16['Unnamed: 8']
full_data16 = full_data16.drop(columns = ['Unnamed: 8'])


full_data16['Home_win'] = full_data16['Home_win'].map({'W':1, "L": 0})

full_data16 = full_data16[['ngd','owd','old','srsd','sosd','tpd','opd','mpd','fgpd','orbd','tppd','trbd','ad','sd','bd','td','Home_win']]

full_data = pd.concat([full_data, full_data16], axis = 0)

################################################################


seas_2015 = pd.read_excel(path1, sheetname='2015')
seas_2015.columns = seas_columns

print("Column headings:")
print(seas_2015.columns)

game_results = pd.read_csv(path2)
print(game_results.columns)
game_results15 = game_results[game_results['Year'] == '2014-15']
game_results15 = game_results15[['Schl','Opp','Unnamed: 8']]

game_results15['game_id']= range(0,5295)
home_data15 = pd.merge(game_results15, seas_2015, left_on = "Schl", right_on = "School")
full_data15 = pd.merge(home_data15, seas_2015, left_on = 'Opp', right_on= 'School')

print(full_data15.columns)

full_data15['ngd'] = full_data15['NumGames_x'] - full_data15['NumGames_y']
full_data15['owd'] = full_data15['OverallW_x'] - full_data15['OverallW_y']
full_data15['old'] = full_data15['OverallL_x'] - full_data15['OverallL_y']
full_data15['srsd'] = full_data15['SRS_x'] - full_data15['SRS_y']
full_data15['sosd'] = full_data15['SOS_x'] - full_data15['SOS_y']
full_data15['tpd'] = full_data15['Team Points_x'] - full_data15['Team Points_y']
full_data15['opd'] = full_data15['OppPoints_x'] - full_data15['OppPoints_y']
full_data15['mpd'] = full_data15['MP_x'] - full_data15['MP_y']
full_data15['fgpd'] = full_data15['FG%_x'] - full_data15['FG%_y']
full_data15['orbd'] = full_data15['ORB_x'] - full_data15['ORB_y']
full_data15['tppd'] = full_data15['3P%_x'] - full_data15['3P%_y']
full_data15['trbd'] = full_data15['TRB_x']-full_data15['TRB_y']
full_data15['ad'] = full_data15['AST_x'] - full_data15['AST_y']
full_data15['sd'] = full_data15['STL_x'] - full_data15['STL_y']
full_data15['bd'] = full_data15['BLK_x'] - full_data15['BLK_y']
full_data15['td'] = full_data15['TOV_x'] - full_data15['TOV_y']




full_data15['Home_win'] = full_data15['Unnamed: 8']
full_data15 = full_data15.drop(columns = ['Unnamed: 8'])


full_data15['Home_win'] = full_data15['Home_win'].map({'W':1, "L": 0})

full_data15 = full_data15[['ngd','owd','old','srsd','sosd','tpd','opd','mpd','fgpd','orbd','tppd','trbd','ad','sd','bd','td','Home_win']]

full_data = pd.concat([full_data, full_data15], axis = 0)

#################################################################

seas_2015 = pd.read_excel(path1, sheetname='2015')
seas_2015.columns = seas_columns

print("Column headings:")
print(seas_2015.columns)

game_results = pd.read_csv(path2)
print(game_results.columns)
game_results15 = game_results[game_results['Year'] == '2014-15']
game_results15 = game_results15[['Schl','Opp','Unnamed: 8']]

game_results15['game_id']= range(0,5295)
home_data15 = pd.merge(game_results15, seas_2015, left_on = "Schl", right_on = "School")
full_data15 = pd.merge(home_data15, seas_2015, left_on = 'Opp', right_on= 'School')

print(full_data15.columns)

full_data15['ngd'] = full_data15['NumGames_x'] - full_data15['NumGames_y']
full_data15['owd'] = full_data15['OverallW_x'] - full_data15['OverallW_y']
full_data15['old'] = full_data15['OverallL_x'] - full_data15['OverallL_y']
full_data15['srsd'] = full_data15['SRS_x'] - full_data15['SRS_y']
full_data15['sosd'] = full_data15['SOS_x'] - full_data15['SOS_y']
full_data15['tpd'] = full_data15['Team Points_x'] - full_data15['Team Points_y']
full_data15['opd'] = full_data15['OppPoints_x'] - full_data15['OppPoints_y']
full_data15['mpd'] = full_data15['MP_x'] - full_data15['MP_y']
full_data15['fgpd'] = full_data15['FG%_x'] - full_data15['FG%_y']
full_data15['orbd'] = full_data15['ORB_x'] - full_data15['ORB_y']
full_data15['tppd'] = full_data15['3P%_x'] - full_data15['3P%_y']
full_data15['trbd'] = full_data15['TRB_x']-full_data15['TRB_y']
full_data15['ad'] = full_data15['AST_x'] - full_data15['AST_y']
full_data15['sd'] = full_data15['STL_x'] - full_data15['STL_y']
full_data15['bd'] = full_data15['BLK_x'] - full_data15['BLK_y']
full_data15['td'] = full_data15['TOV_x'] - full_data15['TOV_y']




full_data15['Home_win'] = full_data15['Unnamed: 8']
full_data15 = full_data15.drop(columns = ['Unnamed: 8'])


full_data15['Home_win'] = full_data15['Home_win'].map({'W':1, "L": 0})

full_data15 = full_data15[['ngd','owd','old','srsd','sosd','tpd','opd','mpd','fgpd','orbd','tppd','trbd','ad','sd','bd','td','Home_win']]

full_data = pd.concat([full_data, full_data15], axis = 0)

##################################################


seas_2014 = pd.read_excel(path1, sheetname='2014')
seas_2014.columns = seas_columns

print("Column headings:")
print(seas_2014.columns)

game_results = pd.read_csv(path2)
print(game_results.columns)
game_results14 = game_results[game_results['Year'] == '2013-14']
game_results14 = game_results14[['Schl','Opp','Unnamed: 8']]

game_results14['game_id']= range(0,5263)
home_data14 = pd.merge(game_results14, seas_2014, left_on = "Schl", right_on = "School")
full_data14 = pd.merge(home_data14, seas_2014, left_on = 'Opp', right_on= 'School')

print(full_data14.columns)

full_data14['ngd'] = full_data14['NumGames_x'] - full_data14['NumGames_y']
full_data14['owd'] = full_data14['OverallW_x'] - full_data14['OverallW_y']
full_data14['old'] = full_data14['OverallL_x'] - full_data14['OverallL_y']
full_data14['srsd'] = full_data14['SRS_x'] - full_data14['SRS_y']
full_data14['sosd'] = full_data14['SOS_x'] - full_data14['SOS_y']
full_data14['tpd'] = full_data14['Team Points_x'] - full_data14['Team Points_y']
full_data14['opd'] = full_data14['OppPoints_x'] - full_data14['OppPoints_y']
full_data14['mpd'] = full_data14['MP_x'] - full_data14['MP_y']
full_data14['fgpd'] = full_data14['FG%_x'] - full_data14['FG%_y']
full_data14['orbd'] = full_data14['ORB_x'] - full_data14['ORB_y']
full_data14['tppd'] = full_data14['3P%_x'] - full_data14['3P%_y']
full_data14['trbd'] = full_data14['TRB_x']-full_data14['TRB_y']
full_data14['ad'] = full_data14['AST_x'] - full_data14['AST_y']
full_data14['sd'] = full_data14['STL_x'] - full_data14['STL_y']
full_data14['bd'] = full_data14['BLK_x'] - full_data14['BLK_y']
full_data14['td'] = full_data14['TOV_x'] - full_data14['TOV_y']




full_data14['Home_win'] = full_data14['Unnamed: 8']
full_data14 = full_data14.drop(columns = ['Unnamed: 8'])


full_data14['Home_win'] = full_data14['Home_win'].map({'W':1, "L": 0})

full_data14 = full_data14[['ngd','owd','old','srsd','sosd','tpd','opd','mpd','fgpd','orbd','tppd','trbd','ad','sd','bd','td','Home_win']]

full_data = pd.concat([full_data, full_data14], axis = 0)

########################################################################3

seas_2013 = pd.read_excel(path1, sheetname='2013')
seas_2013.columns = seas_columns

print("Column headings:")
print(seas_2013.columns)

game_results = pd.read_csv(path2)
print(game_results.columns)
game_results13 = game_results[game_results['Year'] == '2012-13']
game_results13 = game_results13[['Schl','Opp','Unnamed: 8']]

game_results13['game_id']= range(0,5156)
home_data13 = pd.merge(game_results13, seas_2013, left_on = "Schl", right_on = "School")
full_data13 = pd.merge(home_data13, seas_2013, left_on = 'Opp', right_on= 'School')

print(full_data13.columns)

full_data13['ngd'] = full_data13['NumGames_x'] - full_data13['NumGames_y']
full_data13['owd'] = full_data13['OverallW_x'] - full_data13['OverallW_y']
full_data13['old'] = full_data13['OverallL_x'] - full_data13['OverallL_y']
full_data13['srsd'] = full_data13['SRS_x'] - full_data13['SRS_y']
full_data13['sosd'] = full_data13['SOS_x'] - full_data13['SOS_y']
full_data13['tpd'] = full_data13['Team Points_x'] - full_data13['Team Points_y']
full_data13['opd'] = full_data13['OppPoints_x'] - full_data13['OppPoints_y']
full_data13['mpd'] = full_data13['MP_x'] - full_data13['MP_y']
full_data13['fgpd'] = full_data13['FG%_x'] - full_data13['FG%_y']
full_data13['orbd'] = full_data13['ORB_x'] - full_data13['ORB_y']
full_data13['tppd'] = full_data13['3P%_x'] - full_data13['3P%_y']
full_data13['trbd'] = full_data13['TRB_x']-full_data13['TRB_y']
full_data13['ad'] = full_data13['AST_x'] - full_data13['AST_y']
full_data13['sd'] = full_data13['STL_x'] - full_data13['STL_y']
full_data13['bd'] = full_data13['BLK_x'] - full_data13['BLK_y']
full_data13['td'] = full_data13['TOV_x'] - full_data13['TOV_y']




full_data13['Home_win'] = full_data13['Unnamed: 8']
full_data13 = full_data13.drop(columns = ['Unnamed: 8'])


full_data13['Home_win'] = full_data13['Home_win'].map({'W':1, "L": 0})

full_data13 = full_data13[['ngd','owd','old','srsd','sosd','tpd','opd','mpd','fgpd','orbd','tppd','trbd','ad','sd','bd','td','Home_win']]

full_data = pd.concat([full_data, full_data13], axis = 0)



################################################

seas_2012 = pd.read_excel(path1, sheetname='2012')
seas_2012.columns = seas_columns

print("Column headings:")
print(seas_2012.columns)

game_results = pd.read_csv(path2)
print(game_results.columns)
game_results12 = game_results[game_results['Year'] == '2011-12']
game_results12 = game_results12[['Schl','Opp','Unnamed: 8']]

game_results12['game_id']= range(0,5122)
home_data12 = pd.merge(game_results12, seas_2012, left_on = "Schl", right_on = "School")
full_data12 = pd.merge(home_data12, seas_2012, left_on = 'Opp', right_on= 'School')

print(full_data12.columns)

full_data12['ngd'] = full_data12['NumGames_x'] - full_data12['NumGames_y']
full_data12['owd'] = full_data12['OverallW_x'] - full_data12['OverallW_y']
full_data12['old'] = full_data12['OverallL_x'] - full_data12['OverallL_y']
full_data12['srsd'] = full_data12['SRS_x'] - full_data12['SRS_y']
full_data12['sosd'] = full_data12['SOS_x'] - full_data12['SOS_y']
full_data12['tpd'] = full_data12['Team Points_x'] - full_data12['Team Points_y']
full_data12['opd'] = full_data12['OppPoints_x'] - full_data12['OppPoints_y']
full_data12['mpd'] = full_data12['MP_x'] - full_data12['MP_y']
full_data12['fgpd'] = full_data12['FG%_x'] - full_data12['FG%_y']
full_data12['orbd'] = full_data12['ORB_x'] - full_data12['ORB_y']
full_data12['tppd'] = full_data12['3P%_x'] - full_data12['3P%_y']
full_data12['trbd'] = full_data12['TRB_x']-full_data12['TRB_y']
full_data12['ad'] = full_data12['AST_x'] - full_data12['AST_y']
full_data12['sd'] = full_data12['STL_x'] - full_data12['STL_y']
full_data12['bd'] = full_data12['BLK_x'] - full_data12['BLK_y']
full_data12['td'] = full_data12['TOV_x'] - full_data12['TOV_y']




full_data12['Home_win'] = full_data12['Unnamed: 8']
full_data12 = full_data12.drop(columns = ['Unnamed: 8'])


full_data12['Home_win'] = full_data12['Home_win'].map({'W':1, "L": 0})

full_data12 = full_data12[['ngd','owd','old','srsd','sosd','tpd','opd','mpd','fgpd','orbd','tppd','trbd','ad','sd','bd','td','Home_win']]

full_data = pd.concat([full_data, full_data12], axis = 0)

#############################################################

seas_2011 = pd.read_excel(path1, sheetname='2011')
seas_2011.columns = seas_columns

print("Column headings:")
print(seas_2011.columns)

game_results = pd.read_csv(path2)
print(game_results.columns)
game_results11 = game_results[game_results['Year'] == '2010-11']
game_results11 = game_results11[['Schl','Opp','Unnamed: 8']]

game_results11['game_id']= range(0,5105)
home_data11 = pd.merge(game_results11, seas_2011, left_on = "Schl", right_on = "School")
full_data11 = pd.merge(home_data11, seas_2011, left_on = 'Opp', right_on= 'School')

print(full_data11.columns)

full_data11['ngd'] = full_data11['NumGames_x'] - full_data11['NumGames_y']
full_data11['owd'] = full_data11['OverallW_x'] - full_data11['OverallW_y']
full_data11['old'] = full_data11['OverallL_x'] - full_data11['OverallL_y']
full_data11['srsd'] = full_data11['SRS_x'] - full_data11['SRS_y']
full_data11['sosd'] = full_data11['SOS_x'] - full_data11['SOS_y']
full_data11['tpd'] = full_data11['Team Points_x'] - full_data11['Team Points_y']
full_data11['opd'] = full_data11['OppPoints_x'] - full_data11['OppPoints_y']
full_data11['mpd'] = full_data11['MP_x'] - full_data11['MP_y']
full_data11['fgpd'] = full_data11['FG%_x'] - full_data11['FG%_y']
full_data11['orbd'] = full_data11['ORB_x'] - full_data11['ORB_y']
full_data11['tppd'] = full_data11['3P%_x'] - full_data11['3P%_y']
full_data11['trbd'] = full_data11['TRB_x']-full_data11['TRB_y']
full_data11['ad'] = full_data11['AST_x'] - full_data11['AST_y']
full_data11['sd'] = full_data11['STL_x'] - full_data11['STL_y']
full_data11['bd'] = full_data11['BLK_x'] - full_data11['BLK_y']
full_data11['td'] = full_data11['TOV_x'] - full_data11['TOV_y']




full_data11['Home_win'] = full_data11['Unnamed: 8']
full_data11 = full_data11.drop(columns = ['Unnamed: 8'])


full_data11['Home_win'] = full_data11['Home_win'].map({'W':1, "L": 0})

full_data11 = full_data11[['ngd','owd','old','srsd','sosd','tpd','opd','mpd','fgpd','orbd','tppd','trbd','ad','sd','bd','td','Home_win']]

full_data = pd.concat([full_data, full_data11], axis = 0)

###############################################

seas_2010 = pd.read_excel(path1, sheetname='2010')
seas_2010.columns = seas_columns

print("Column headings:")
print(seas_2010.columns)

game_results = pd.read_csv(path2)
print(game_results.columns)
game_results10 = game_results[game_results['Year'] == '2009-10']
game_results10 = game_results10[['Schl','Opp','Unnamed: 8']]

game_results10['game_id']= range(0,4992)
home_data10 = pd.merge(game_results10, seas_2010, left_on = "Schl", right_on = "School")
full_data10 = pd.merge(home_data10, seas_2010, left_on = 'Opp', right_on= 'School')

print(full_data10.columns)

full_data10['ngd'] = full_data10['NumGames_x'] - full_data10['NumGames_y']
full_data10['owd'] = full_data10['OverallW_x'] - full_data10['OverallW_y']
full_data10['old'] = full_data10['OverallL_x'] - full_data10['OverallL_y']
full_data10['srsd'] = full_data10['SRS_x'] - full_data10['SRS_y']
full_data10['sosd'] = full_data10['SOS_x'] - full_data10['SOS_y']
full_data10['tpd'] = full_data10['Team Points_x'] - full_data10['Team Points_y']
full_data10['opd'] = full_data10['OppPoints_x'] - full_data10['OppPoints_y']
full_data10['mpd'] = full_data10['MP_x'] - full_data10['MP_y']
full_data10['fgpd'] = full_data10['FG%_x'] - full_data10['FG%_y']
full_data10['orbd'] = full_data10['ORB_x'] - full_data10['ORB_y']
full_data10['tppd'] = full_data10['3P%_x'] - full_data10['3P%_y']
full_data10['trbd'] = full_data10['TRB_x']-full_data10['TRB_y']
full_data10['ad'] = full_data10['AST_x'] - full_data10['AST_y']
full_data10['sd'] = full_data10['STL_x'] - full_data10['STL_y']
full_data10['bd'] = full_data10['BLK_x'] - full_data10['BLK_y']
full_data10['td'] = full_data10['TOV_x'] - full_data10['TOV_y']




full_data10['Home_win'] = full_data10['Unnamed: 8']
full_data10 = full_data10.drop(columns = ['Unnamed: 8'])


full_data10['Home_win'] = full_data10['Home_win'].map({'W':1, "L": 0})

full_data10 = full_data10[['ngd','owd','old','srsd','sosd','tpd','opd','mpd','fgpd','orbd','tppd','trbd','ad','sd','bd','td','Home_win']]

full_data = pd.concat([full_data, full_data10], axis = 0)

full_data.to_csv('Documents\\win_loss_bracket.csv')

