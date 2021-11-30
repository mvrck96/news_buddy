import streamlit as st
import utils as ut

conn = ut.db_connect()
st.set_page_config(page_title="newsbuddy", page_icon=":newspaper:")

st.sidebar.markdown("# Settings")
source = st.sidebar.radio("Select source:", ('tass', 'rbc', 'gazeta'))
counter = st.sidebar.slider("News counter:", 0, 30, 5)

st.title("Newsbuddy")
table = 'news_' + source

if source=="tass":
    st.write(f"## Fresh news from {source}")
    ut.print_news(conn, table, counter)

elif source=="rbc":
    st.write(f"## Fresh news from {source}")
    ut.print_news(conn, table, counter)

elif source=="gazeta":
    st.write(f"## Fresh news from {source}")
    ut.print_news(conn, table, counter)