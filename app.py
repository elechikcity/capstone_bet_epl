# Import Libraries
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# Set Page configuration
# Read more at https://docs.streamlit.io/1.6.0/library/api-reference/utilities/st.set_page_config
st.set_page_config(page_title='Predict outcome of EPL match', page_icon='⚽', layout='wide', initial_sidebar_state='expanded')

# Set title of the app
st.title('⚽ Predict the outcome of an EPL match! ⚽')

# Load csv into df
df = pd.read_csv('new_df_final_to_streamlit.csv')


#Writing a text for introduction
st.write("Hello fellow football bettor, let's make our lives BET-ter! Key in the parameters as seen in the website, after which a predicted outcome and potential winnings will be generated! All the best!")

st.write("")

st.write("For Bet365 odds, you may refer to https://www.bet365.com.au/#/AC/B1/C1/D1002/E76169570/G40/H^1/ for more information.")
st.write("For odds converter, you may refer to https://matchedbettingblog.com/odds-converter/ for more information.")
st.write("For current rank of teams, you may refer to https://www.premierleague.com/tables for more information.")

#Text inputs 
st.write("")

col1, col2 = st.columns(2)
with col1:
    home_name = st.selectbox('Home Team Name',['','Arsenal','Aston Villa','Bournemouth','Brentford','Brighton & Hove Albion','Chelsea','Crystal Palace','Everton','Fulham','Leeds United','Leicester City','Liverpool','Manchester City','Manchester United','Newcastle United','Nottingham Forest','Southampton','Tottenham Hotspur','West Ham United','Wolverhampton Wanderers'])
 
with col2:
    away_name = st.selectbox('Away Team Name',['','Arsenal','Aston Villa','Bournemouth','Brentford','Brighton & Hove Albion','Chelsea','Crystal Palace','Everton','Fulham','Leeds United','Leicester City','Liverpool','Manchester City','Manchester United','Newcastle United','Nottingham Forest','Southampton','Tottenham Hotspur','West Ham United','Wolverhampton Wanderers']) 

#home_name = st.selectbox('Home Team Name',['Arsenal','Aston Villa','Bournemouth','Brentford','Brighton & Hove Albion','Chelsea','Crystal Palace','Everton','Fulham','Leeds United','Leicester City','Liverpool','Manchester City','Manchester United','Newcastle United','Nottingham Forest','Southampton','Tottenham Hotspur','West Ham United','Wolverhampton Wanderers'])

#away_name = st.selectbox('Away Team Name',['Arsenal','Aston Villa','Bournemouth','Brentford','Brighton & Hove Albion','Chelsea','Crystal Palace','Everton','Fulham','Leeds United','Leicester City','Liverpool','Manchester City','Manchester United','Newcastle United','Nottingham Forest','Southampton','Tottenham Hotspur','West Ham United','Wolverhampton Wanderers']) 

Bet_Amount = st.sidebar.number_input('Bet Amount', 1.0, 100000000.0, 10.0)


# Set input widgets that will be the 'x_test' input thereafter

st.sidebar.subheader('Select Match Attributes')
Home_Odds = st.sidebar.number_input('Bet365 Home Odds', 1.0, 30.0, 2.0)
Draw_Odds = st.sidebar.number_input('Bet365 Draw Odds', 1.0, 30.0, 2.0)
Away_Odds = st.sidebar.number_input('Bet365 Away Odds', 1.0, 30.0, 2.0)
Home_Team_Rank = st.sidebar.slider('Current Rank (Home Team)', 1, 20, 10)
Away_Team_Rank = st.sidebar.slider('Current Rank (Away Team)', 1, 20, 10)
matchday = st.sidebar.selectbox('Select Matchday',[' ','Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday'])
referee = st.sidebar.selectbox('Select Referee',[' ','A Marriner', 'A Taylor', 'C Foy','H Webb','J Moss','K Friend','L Mason','L Probert','M Atkinson','M Clattenburg','M Dean','M Oliver','M Riley','P Dowd','M Jones','OTHERS'])

#Defining matchdays Variables

matchday_Monday =0
matchday_Tuesday =0
matchday_Wednesday =0
matchday_Thursday =0
matchday_Friday =0
matchday_Saturday =0
matchday_Sunday =0


#Depending on what the user puts in the matchday, change the model columns accordingly.

if matchday == 'Monday':
    matchday_Monday = 1
elif matchday == 'Tuesday':
    matchday_Tuesday = 1
elif matchday == 'Wednesday':
    matchday_Wednesday = 1   
elif matchday == 'Thursday':
    matchday_Thursday = 1    
elif matchday == 'Saturday':
    matchday_Saturday = 1
elif matchday == 'Sunday':
    matchday_Sunday = 1    
else: 
    matchday_Friday = 1

#Defining Referee Variables 

ref_AMarriner =0
ref_ATaylor =0
ref_AMarriner=0
ref_ATaylor=0
ref_CFoy=0
ref_HWebb=0
ref_JMoss=0
ref_KFriend=0
ref_LMason=0
ref_LProbert=0
ref_MAtkinson=0
ref_MClattenburg=0
ref_MDean=0
ref_MOliver=0
ref_MRiley=0
ref_PDowd=0
ref_MJones=0

#Depending on what the user puts in the select box under referee, change the model column accordingly
if referee == 'A Marriner':
     ref_AMarriner = 1
elif referee == 'A Taylor':
    ref_ATaylor= 1
elif referee == 'C Foy':
    ref_CFoy= 1   
elif referee == 'H Webb':
    ref_HWebb= 1
elif referee == 'J Moss':
    ref_JMoss= 1
elif referee == 'K Friend':
    ref_KFriend= 1
elif referee == 'L Mason':
    ref_LMason= 1
elif referee == 'L Probert':
    ref_LProbert= 1    
elif referee == 'M Atkinson':
    ref_MAtkinson= 1
elif referee == 'M Clattenburg':
    ref_MClattenburg= 1    
elif referee == 'M Dean':
    ref_MDean= 1    
elif referee == 'M Oliver':
    ref_MOliver= 1
elif referee == 'M Riley':
    ref_MRiley= 1 
elif referee == 'P Dowd':
    ref_PDowd= 1 
else:
    ref_MJones= 1 

    
feature_cols = ['B365H','B365D','B365A','matchday_Monday','matchday_Saturday',
               'matchday_Sunday','matchday_Thursday','matchday_Tuesday','matchday_Wednesday','ht_rank','at_rank',
               'ref_A Marriner','ref_A Taylor','ref_C Foy', 'ref_H Webb',
               'ref_J Moss','ref_K Friend','ref_L Mason','ref_L Probert','ref_M Atkinson'
              ,'ref_M Clattenburg','ref_M Dean','ref_M Oliver','ref_M Riley','ref_P Dowd','ref_M Jones']


# Separate to X and y
X = df[feature_cols]
y = df.FTR

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)


# Build model and train
knn = KNeighborsClassifier(n_neighbors=77)
knn.fit(X_train, y_train)


# # Generate prediction based on user selected attributes (predictingunseen data)

y_pred = knn.predict([[Home_Odds, Draw_Odds, Away_Odds, matchday_Monday, matchday_Saturday, matchday_Sunday, matchday_Thursday, matchday_Tuesday, matchday_Wednesday, Home_Team_Rank, Away_Team_Rank, ref_AMarriner, ref_ATaylor, ref_CFoy, ref_HWebb, ref_JMoss, ref_KFriend, ref_LMason, ref_LProbert, ref_MAtkinson, ref_MClattenburg, ref_MDean, ref_MOliver, ref_MRiley, ref_PDowd, ref_MJones]])

#Generating the predicted outcome 

if y_pred[0] == 0:
    winner = 'Draw'
elif y_pred[0] == 1:
    winner = away_name + " Win"
else:
    winner= home_name + " Win"

#Generating the winnings variable based on predicted outcome 

if y_pred[0] == 0:
    winnings = Bet_Amount * Draw_Odds
elif y_pred[0] == 1:
    winnings = Bet_Amount * Away_Odds
else:
    winnings = Bet_Amount * Home_Odds
    

st.write("")
st.write("")

#Print predicted outcome of the game with the use of a button!
if st.button('PREDICT'):
    st.write("")
    st.subheader('Final Prediction:')
    st.metric('', winner, '')
    st.subheader('Potential Winnings:')
    st.metric('', f'${winnings}', '')
else:
    st.write('')


st.write("Disclaimer: Please note that this information should not be construed as a recommendation or endorsement of gambling. The National Council on Problem Gambling in Singapore provides a helpline for individuals who are struggling with gambling addiction. The helpline number is 1800-6-668-668.")


#Unused code below:
# Print predicted outcome of the game

# st.write("")
# st.subheader('Final Prediction:')
# st.metric('', winner, '')

# st.subheader('')
# Print predicted winnings of the game if you were to bet
# st.subheader('Potential Winnings:')
# st.metric('', f'${winnings}', '')



# st.write("")
# home_name = st.text_input('Home Team Name')
# away_name = st.text_input('Away Team Name')
