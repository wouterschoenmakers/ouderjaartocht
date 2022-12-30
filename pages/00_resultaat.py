import os
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
order = ["Bart", "Bram", "Cody", "Daan", "Gijs", "Ido", "Joost", "Jorg", "Lennart", "Noud", "Olivier", "Pim","Sander", "Wouter"]
json_files = [file for file in os.listdir() if "json" in file]
to_go = [person for person in order if person+".json" not in json_files]

st.error(f"De volgende mensen moeten de vragenlijst nog invullen:\n {', '.join(to_go)}")


if not to_go:
    all_data = []
    for file in json_files:
        sub_df = pd.read_json(file, orient="records", typ="series").rename(file)
        all_data.append(sub_df)

    df = pd.concat(all_data,axis=1)
    df.index = df.index.str.split("-",expand=True)

    vraag1_tab, vraag2_tab, vraag3_tab,overal_tab = st.tabs(["Vraag 1","Vraag 2","Vraag 3","Overal"])
    vraag1 = df.loc["vraag1"].mean(axis=1).sort_values()
    vraag1.name="Score vraag 1"
    vraag2 = df.loc["vraag2"].mean(axis=1).sort_values()
    vraag2.name = "Score vraag 2"
    vraag3 = df.loc["vraag3"].mean(axis=1).sort_values()
    vraag3.name = "Score vraag 3"
    with vraag1_tab:
        fig = px.bar(vraag1)
        st.subheader("Op een schaal van 1 tot 10 hoe groot is de kans dat deze persoon op zaterdag met zijn vriendin op de bank blijft ipv met vrienden wat te doen?")
        st.plotly_chart(fig)
    with vraag2_tab:
        fig = px.bar(vraag2)
        st.subheader("Op een schaal van 1 tot 10 hoe groot is de kans dat deze persoon niet alleen maar samen met zijn vriendin naar een feestje komt?")
        st.plotly_chart(fig)
    with vraag3_tab:
        fig = px.bar(vraag3)
        st.subheader("Op een schaal van 1 tot 10 hoe vaak praat deze persoon in de wij vorm?")
        st.plotly_chart(fig)
    with overal_tab:
        gem = ((vraag1 + vraag2 + vraag3) /3).sort_values()
        gem.name = "Gemiddelde Score"
        fig = px.bar(gem)
        st.subheader("De gemiddelde degelijkheidsscore:")
        st.plotly_chart(fig)
        button = st.button('Create teams')
        if button:
            teams_df = gem.drop(index=["Gijs","Wouter"]).to_frame().assign(Team="Team")
            for e,team in enumerate(["Team 1", "Team 2","Team 3","Team 4"]):
                teams_df.iloc[e*3:(e+1)*3,:].loc[:,"Team"] = team
            gijs_wouter = gem[["Gijs","Wouter"]].to_frame()
            teams_df = teams_df.append(gijs_wouter).sort_values("Gemiddelde Score")
            teams_df.loc["Gijs","Team"] = teams_df.iloc[np.argmin(abs(teams_df.drop(index="Gijs").loc[:,"Gemiddelde Score"] - teams_df.loc["Gijs","Gemiddelde Score"]))].loc["Team"]
            teams_df.loc["Wouter", "Team"] = teams_df.iloc[np.argmin(
                abs(teams_df.drop(index="Wouter").loc[:, "Gemiddelde Score"] - teams_df.loc["Wouter", "Gemiddelde Score"]))].loc["Team"]
            fig = px.bar(teams_df,y="Gemiddelde Score",color="Team")
            st.plotly_chart(fig)




