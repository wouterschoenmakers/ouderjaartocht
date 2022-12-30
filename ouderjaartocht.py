import pandas as pd
import streamlit as st
import numpy as np
import json

st.header("Degelijkheidsrankinglist🚴🏼‍♀")
st.subheader("Gebaseerd op de ingevulde scores wordt een teamindeling gemaakt")
# uploader = st.file_uploader(label="Upload de resultaten van de ranking the degelijkheid")
#

order = ["Bart", "Bram", "Cody", "Daan", "Gijs", "Ido", "Joost", "Jorg", "Lennart", "Noud", "Olivier", "Pim","Sander", "Wouter"]

with st.form("Degelijkheidsform"):
        user = st.selectbox(options=order, label="Wie ben je?")
        tabs = st.tabs(order)
        for i, person in enumerate(order):
            tab = tabs[i]
            with tab:
                vraag1 = st.slider(label=f"Op een schaal van 1 tot 10 hoe groot is de kans dat {person} op zaterdag met zijn vriendin op de bank blijft ipv met vrienden wat te doen?",
                                    min_value=1,max_value=10,step=1,key=f"vraag1-{person}")
                vraag2=st.slider(label=f"Op een schaal van 1 tot 10 hoe groot is de kans dat {person} niet alleen maar samen met zijn vriendin naar een feestje komt?",
                                    min_value=1,max_value=10,step=1,key=f"vraag2-{person}")
                vraag3 = st.slider(
                    label=f"Op een schaal van 1 tot 10 hoe vaak praat {person} in de wij vorm?",
                    min_value=1, max_value=10, step=1, key=f"vraag3-{person}")
        submit = st.form_submit_button()
        sub_session_state = {key: value for key, value in st.session_state.items() if "vraag" in key}
        num_ones = sum(int(value == 1) for value in sub_session_state.values())
        if submit and num_ones > 18:
            st.warning("Vul de vragenlijst voor iedereen in")
        elif submit and num_ones < 18:
            with open(f"{user}.json", "w") as f:
                json.dump(sub_session_state, f)
            st.succes("lekker bezig homie")


            # df = pd.DataFrame(data=sub_session_state)

# if uploader is not None:
#
#     df = pd.read_excel(uploader)
#
#     Bonus = df.loc[:, df.columns[-1]]
#     df = df.loc[:, df.columns[1:-1]]
#     order = ["Bart", "Bram", "Cody", "Daan", "Gijs", "Ido", "Joost", "Jorg", "Lennart", "Noud", "Olivier", "Pim",
#              "Sander", "Wouter"]
#     df.loc["name", :] = np.repeat(order, 4)
#
#     title_op_bank = "Op een schaal van 1 tot 10 hoe groot is de kans dat deze persoon op zaterdag met zijn vriendin op de bank blijft ipv met vrienden wat te doen?	"
#     op_bank = df.T.iloc[np.arange(0, len(df.T), 4), :].set_index("name", drop=True)
#     title_op_feest = "Op een schaal van 1 tot 10 hoe groot is de kans dat deze persoon niet alleen maar samen met zijn vriendin naar een feestje komt?"
#     op_feest = df.T.iloc[np.arange(1, len(df.T), 4), :].set_index("name", drop=True)
#     title_we = "Op een schaal van 1 tot 10 hoe groot is de kans dat deze persoon niet alleen maar samen met zijn vriendin naar een feestje komt?"
#     we_df = df.T.iloc[np.arange(2, len(df.T), 4), :].set_index("name", drop=True)
#
#     print(op_bank.mean(axis=1))
#     bank, feest, we,overal= st.tabs(["vraag 1", "vraag 2", "vraag 3", "Overal"])
#     with bank:
#         st.bar_chart(op_bank.mean(axis=1).sort_values())
#     with feest:
#         st.bar_chart(op_feest.mean(axis=1).sort_values())
#     with we:
#         st.bar_chart(we_df.mean(axis=1).sort_values())
#     with