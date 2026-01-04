import streamlit as st

st.set_page_config(page_title="Game Setup", layout="centered")
st.title("Game Setup")

BASE_RESOURCE = 12
BASE_HEALTH = 30

def init_setup():
    st.session_state.setup_complete = False

if "setup_complete" not in st.session_state:
    init_setup()

st.subheader("Player 1")

p1_name = st.text_input("Player 1 Name")
p1_gridlord = st.text_input("Player 1 Gridlord Name")
p1_cost = st.number_input(
    "Player 1 Gridlord Resource Cost",
    min_value=0,
    max_value=BASE_RESOURCE,
    value=0
)

st.subheader("Player 2")

p2_name = st.text_input("Player 2 Name")
p2_gridlord = st.text_input("Player 2 Gridlord Name")
p2_cost = st.number_input(
    "Player 2 Gridlord Resource Cost",
    min_value=0,
    max_value=BASE_RESOURCE,
    value=0
)

st.divider()

if st.button("Start Game"):
    st.session_state.p1_name = p1_name
    st.session_state.p2_name = p2_name

    st.session_state.p1_gridlord = p1_gridlord
    st.session_state.p2_gridlord = p2_gridlord

    st.session_state.p1_health = BASE_HEALTH
    st.session_state.p2_health = BASE_HEALTH

    st.session_state.p1_resource = BASE_RESOURCE - p1_cost
    st.session_state.p2_resource = BASE_RESOURCE - p2_cost

    st.session_state.turn = 1
    st.session_state.pending_actions = []
    st.session_state.setup_complete = True

    st.success("Game setup complete! Go to the Game page ⬅️")
