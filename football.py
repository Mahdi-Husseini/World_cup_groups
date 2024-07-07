import pandas as pd
import streamlit as st
import altair as alt
from string import ascii_uppercase as alphabet
from PIL import Image

image = Image.open('fifa.jpg')
st.image(image, use_column_width= True)
st.title('2022 FIFA World Cup QATAR Group Stage')
st.write("""
    this app fetches the data of the group stages of 2022 FIFA QATAR World Cup
    \nthe data used in this is app scraped from [Wikipedia](https://en.wikipedia.org/wiki/2022_FIFA_World_Cup)
    \n* **Python libraries:** streamlit, pandas, string, PIL, base64, altair
    \n***
""")

url = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup')
goals = pd.read_csv('goals.csv')
dict_group = {}
dict_goals = {}
for letter, i in zip(alphabet, range(9, 65, 7)):
    df = url[i]
    df.rename(columns={df.columns[1]: 'Team'}, inplace=True)
    df.pop('Qualification')
    dict_group[f"Group {letter}"] = df


show_goal = False

if st.sidebar.checkbox('Show top scorers'):
    show_goal = True
st.sidebar.title('Search a specific team')
selected_team = st.sidebar.text_input('eg: Brazil')
selected_team =  selected_team.lower()
selected_team = selected_team.capitalize()
found = False
if selected_team and show_goal == False:
    for letter in alphabet[:8]:
        if(selected_team in dict_group[f"Group {letter}"]["Team"].tolist()):
            st.header(selected_team)
            found = True
            df = dict_group[f"Group {letter}"]
            res = "no"
            if( df.set_index('Team').loc[selected_team, "Pos"] == 1 or df.set_index('Team').loc[selected_team, "Pos"] == 2):
                res="yes"
            st.subheader(f'_Group: {letter}')
            st.subheader(f'-Qualified: {res}')
            rank = df.set_index('Team').loc[selected_team, 'Pos']
            st.subheader(f'-rank: {rank}')
            points = df.set_index('Team').loc[selected_team, 'Pts']
            st.subheader(f"-Points: {points}")
            st.header('Matches')
            mp = df.set_index('Team').loc[selected_team, 'Pld']
            mw = df.set_index('Team').loc[selected_team, 'W']
            md = df.set_index('Team').loc[selected_team, 'D']
            ml = df.set_index('Team').loc[selected_team, 'L']
            st.subheader(f"-Played: {mp}")
            st.subheader(f"-Won: {mw}")
            st.subheader(f"-Draw: {md}")
            st.subheader(f"-Lost: {ml}")
    if not found:
        st.header("Team not found")
elif show_goal == False:
    for key in dict_group.keys():
        st.subheader(key)
        st.dataframe(dict_group[key])
        st.write("***")
else:
    all_goals = pd.read_csv('all_goals.csv')
    st.subheader('Top Goal Scorers')
    st.dataframe(goals)
    st.write("***")
    st.subheader('Bar Chart of goal-scorers per team(goals > 1): ')
    #parsing dict to dataframe to pass to altair
    player_count = all_goals['team'].value_counts().reset_index()
    player_count.columns = ['team', 'count']
    f = alt.Chart(player_count).mark_bar().encode(
        x = "team",
        y = 'count'
    )

    f = f.properties(
        width = alt.Step(75)
    )
    st.write(f)
