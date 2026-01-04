import streamlit as st

st.set_page_config(page_title="Game", layout="wide")
st.title("1v1 Game")

if not st.session_state.get("setup_complete", False):
    st.warning("Please complete game setup first.")
    st.stop()

st.subheader(f"Turn {st.session_state.turn}")

# ---------- Player display ----------
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {st.session_state.p1_name}")
    st.caption(f"Gridlord: {st.session_state.p1_gridlord}")
    st.metric("Health", st.session_state.p1_health)
    st.metric("Resource", st.session_state.p1_resource)

with col2:
    st.markdown(f"### {st.session_state.p2_name}")
    st.caption(f"Gridlord: {st.session_state.p2_gridlord}")
    st.metric("Health", st.session_state.p2_health)
    st.metric("Resource", st.session_state.p2_resource)

st.divider()

# ---------- Add action ----------
st.subheader("Add Action")

action_name = st.text_input("Action name", "Custom Action")

col1, col2 = st.columns(2)

with col1:
    p1_hp = st.number_input("P1 Health change", value=0)
    p1_res = st.number_input("P1 Resource change", value=0)

with col2:
    p2_hp = st.number_input("P2 Health change", value=0)
    p2_res = st.number_input("P2 Resource change", value=0)

if st.button("Add Action"):
    st.session_state.pending_actions.append({
        "label": action_name,
        "p1_hp": p1_hp,
        "p2_hp": p2_hp,
        "p1_res": p1_res,
        "p2_res": p2_res,
    })

# ---------- Pending actions ----------
st.divider()
st.subheader("Pending Actions")

total_p1_hp = total_p2_hp = total_p1_res = total_p2_res = 0

if not st.session_state.pending_actions:
    st.info("No actions added.")
else:
    for i, action in enumerate(st.session_state.pending_actions):
        st.write(
            f"{i+1}. **{action['label']}** | "
            f"P1 HP {action['p1_hp']} | "
            f"P2 HP {action['p2_hp']} | "
            f"P1 Res {action['p1_res']} | "
            f"P2 Res {action['p2_res']}"
        )

        total_p1_hp += action["p1_hp"]
        total_p2_hp += action["p2_hp"]
        total_p1_res += action["p1_res"]
        total_p2_res += action["p2_res"]

# ---------- Preview ----------
st.divider()
st.subheader("Resulting Stats If Applied")

preview_p1_hp = max(0, st.session_state.p1_health + total_p1_hp)
preview_p2_hp = max(0, st.session_state.p2_health + total_p2_hp)
preview_p1_res = max(0, st.session_state.p1_resource + total_p1_res)
preview_p2_res = max(0, st.session_state.p2_resource + total_p2_res)

col1, col2 = st.columns(2)

with col1:
    st.metric("Player 1 Health", preview_p1_hp, preview_p1_hp - st.session_state.p1_health)
    st.metric("Player 1 Resource", preview_p1_res, preview_p1_res - st.session_state.p1_resource)

with col2:
    st.metric("Player 2 Health", preview_p2_hp, preview_p2_hp - st.session_state.p2_health)
    st.metric("Player 2 Resource", preview_p2_res, preview_p2_res - st.session_state.p2_resource)

# ---------- End turn ----------
st.divider()

if st.button("End Turn"):
    st.session_state.p1_health = preview_p1_hp
    st.session_state.p2_health = preview_p2_hp
    st.session_state.p1_resource = preview_p1_res
    st.session_state.p2_resource = preview_p2_res

    st.session_state.pending_actions = []
    st.session_state.turn += 1
