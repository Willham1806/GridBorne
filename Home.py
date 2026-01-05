import streamlit as st

st.set_page_config(page_title="Game Setup", layout="centered")
st.title("⚔️ GridBorne Setup")

BASE_HEALTH = 30
BASE_RESOURCE = 12

# ---------- Initialize session state ----------
if "p1_element" not in st.session_state:
    st.session_state.p1_element = "Water"
if "p2_element" not in st.session_state:
    st.session_state.p2_element = "Water"

# ---------- Player 1 ----------
st.subheader("Player 1 Setup")
p1_name = st.text_input("Player 1 Name")
p1_gridlord = st.text_input("Player 1 Gridlord Name")
p1_cost = st.number_input("Player 1 Gridlord Resource Cost", 0, BASE_RESOURCE, 0)
p1_element = st.radio("Player 1 Element", ["Water", "Earth", "Fire"], horizontal=True)

st.divider()

# ---------- Player 2 ----------
st.subheader("Player 2 Setup")
p2_name = st.text_input("Player 2 Name")
p2_gridlord = st.text_input("Player 2 Gridlord Name")
p2_cost = st.number_input("Player 2 Gridlord Resource Cost", 0, BASE_RESOURCE, 0)
p2_element = st.radio("Player 2 Element", ["Water", "Earth", "Fire"], horizontal=True)

st.divider()

# ---------- Start Game ----------
if st.button("Start Game"):
    if not p1_name or not p2_name:
        st.error("Please enter both players' names.")
    else:
        # Save setup to session_state
        st.session_state.p1_name = p1_name
        st.session_state.p2_name = p2_name
        st.session_state.p1_gridlord = p1_gridlord
        st.session_state.p2_gridlord = p2_gridlord
        st.session_state.p1_element = p1_element
        st.session_state.p2_element = p2_element

        # Health and resources
        st.session_state.p1_health = BASE_HEALTH
        st.session_state.p2_health = BASE_HEALTH
        st.session_state.p1_resource = BASE_RESOURCE - p1_cost
        st.session_state.p2_resource = BASE_RESOURCE - p2_cost

        # Save starting stats for Turn 0
        st.session_state.p1_health_start = st.session_state.p1_health
        st.session_state.p2_health_start = st.session_state.p2_health
        st.session_state.p1_resource_start = st.session_state.p1_resource
        st.session_state.p2_resource_start = st.session_state.p2_resource

        # Turn system
        st.session_state.turn = 1
        st.session_state.active_player = "p1"
        st.session_state.pending_actions = []
        st.session_state.history = {"turn": [], "p1_health": [], "p2_health": [], "p1_resource": [], "p2_resource": []}

        # Mark setup complete
        st.session_state.setup_complete = True

        # Switch to game page
        st.switch_page("pages/1_Game.py")
