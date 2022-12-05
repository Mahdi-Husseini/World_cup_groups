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
    \nthe data used in this is app scraped from [Wikipedia](https://en.wikipedia.org/wiki/2022_FIFA_World_Cup) and from [Si.com](https://www.si.com/soccer/liverpool/news/fifa-world-cup-2022-top-scorers-golden-boot-race#gid=ci02b0d1a1f00025f0&pid=cristiano-ronaldo)
    \n* **Python libraries:** streamlit, pandas, string, PIL, base64, altair
    \n***
""")

url = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup')
url2 = pd.read_html('https://www.si.com/soccer/liverpool/news/fifa-world-cup-2022-top-scorers-golden-boot-race#gid=ci02b0d1a1f00025f0&pid=harry-kane')
dict_group = {}
dict_goals = {}
for letter, i in zip(alphabet, range(9, 65, 7)):
    df = url[i]
    df.rename(columns={df.columns[1]: 'Team'}, inplace=True)
    df.pop('Qualification')
    dict_group[f"Group {letter}"] = df

goals = url2[0]
show_goal = False
for i in goals['Team'].unique():
    k = 0
    for j in goals['Team']:
        if i == j:
            k += 1
            dict_goals[i] = k
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
            if( df.set_index('Team').loc[selected_team, "Pos"] == 1 or  df.set_index('Team').loc[selected_team, "Pos"] == 2):
                res="yes"
            st.subheader(f'_Group: {letter}')
            st.subheader(f'\t-Qualified: {res}')
            rank = df.set_index('Team').loc[selected_team, 'Pos']
            st.subheader(f'\t-rank: {rank}')
            points = df.set_index('Team').loc[selected_team, 'Pts']
            st.subheader(f"\t-Points: {points}")
            st.header('Matches')
            mp = df.set_index('Team').loc[selected_team, 'Pld']
            mw = df.set_index('Team').loc[selected_team, 'W']
            md = df.set_index('Team').loc[selected_team, 'D']
            ml = df.set_index('Team').loc[selected_team, 'L']
            st.subheader(f"\t-Played: {mp}")
            st.subheader(f"\t-Won: {mw}")
            st.subheader(f"\t-Draw: {md}")
            st.subheader(f"\t-Lost: {ml}")
    if not found:
        st.header("Team not found")
elif show_goal == False:
    for key in dict_group.keys():
        st.subheader(key)
        st.dataframe(dict_group[key])
        st.write("***")
else:
    st.subheader('Top Goal Scorers')
    st.dataframe(goals)
    st.write("***")
    st.subheader('Bar Chart of top goal-scorers per team: ')
    #parsing dict to dataframe to pass to altair
    data_goals = pd.DataFrame.from_dict(dict_goals, orient="index")
    data_goals = data_goals.rename({0: 'Players'}, axis = 'columns')
    data_goals.reset_index(inplace=True)
    data_goals = data_goals.rename(columns = {'index': 'Team'})
    f = alt.Chart(data_goals).mark_bar().encode(
        x = "Players",
        y = "Team"
    )

    f = f.properties(
        width = alt.Step(75)
    )
    st.write(f)
    