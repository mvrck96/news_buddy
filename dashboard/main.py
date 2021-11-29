import psycopg2 as ps
import streamlit as st


st.sidebar.markdown("## Select news source:")
source = st.sidebar.radio("", ('Tass', 'Rbc', 'Gazeta'))

if source == 'Tass':
    st.title("Tass news !")
elif source == 'Rbc':
    st.title("Rbc news !")
elif source == 'Gazeta':
    st.title("Gazeta news !")

    