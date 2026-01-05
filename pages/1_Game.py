import streamlit as st

st.set_page_config(page_title="1v1 Game", layout="wide")

if not st.session_state.get("setup_complete", False):
    st.warning("You must complete setup first.")
    st.stop()

# ---------- Turn owner ----------
active_player = st.session_state.active_player
active_name = st.session_state.p1_name if active_player == "p1" else st.session_state.p2_name
st.title("1v1 Game")
st.subheader(f"🎯 {active_name}'s Turn (Turn {st.session_state.turn})")
st.divider()

# ---------- Element emoji ----------
ELEMENT_EMOJI = {"Water": "💧", "Earth": "🌱", "Fire": "🔥"}
p1_emoji = ELEMENT_EMOJI.get(st.session_state.p1_element, "")
p2_emoji = ELEMENT_EMOJI.get(st.session_state.p2_element, "")

# ---------- Player status ----------
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"### {st.session_state.p1_name} {p1_emoji}")
    st.caption(f"Gridlord: {st.session_state.p1_gridlord}")
    st.metric("Health", st.session_state.p1_health)
    st.metric("Resource", st.session_state.p1_resource)

with col2:
    st.markdown(f"### {st.session_state.p2_name} {p2_emoji}")
    st.caption(f"Gridlord: {st.session_state.p2_gridlord}")
    st.metric("Health", st.session_state.p2_health)
    st.metric("Resource", st.session_state.p2_resource)

st.divider()

# ---------- Pending totals for resource check ----------
total_p1_res = sum(a["p1_res"] for a in st.session_state.pending_actions)
total_p2_res = sum(a["p2_res"] for a in st.session_state.pending_actions)

# ---------- Add action ----------
st.subheader("Add Action (Staged)")
action_name = st.text_input("Action name", "Custom Action")

col1, col2 = st.columns(2)
with col1:
    p1_hp = st.number_input("P1 Health change", value=0)
    p1_res = st.number_input("P1 Resource change", value=0)
with col2:
    p2_hp = st.number_input("P2 Health change", value=0)
    p2_res = st.number_input("P2 Resource change", value=0)

# Calculate future totals
total_future_p1_res = st.session_state.p1_resource + total_p1_res + p1_res
total_future_p2_res = st.session_state.p2_resource + total_p2_res + p2_res

# Add Action button
if st.button("Add Action"):
    if total_future_p1_res < 0 or total_future_p2_res < 0:
        st.error("❌ Cannot add action: it would reduce a player's resources below 0!")
    else:
        st.session_state.pending_actions.append({
            "label": action_name,
            "owner": active_player,
            "p1_hp": p1_hp,
            "p2_hp": p2_hp,
            "p1_res": p1_res,
            "p2_res": p2_res,
        })

st.divider()

# ---------- Pending actions ----------
st.subheader("Pending Actions")
total_p1_hp = total_p2_hp = total_p1_res = total_p2_res = 0

if not st.session_state.pending_actions:
    st.info("No actions added this turn.")
else:
    for i, action in enumerate(st.session_state.pending_actions):
        owner_name = st.session_state.p1_name if action["owner"] == "p1" else st.session_state.p2_name
        st.write(f"{i+1}. **{action['label']}** ({owner_name}) | "
                 f"P1 HP {action['p1_hp']} | P2 HP {action['p2_hp']} | "
                 f"P1 Res {action['p1_res']} | P2 Res {action['p2_res']}")
        total_p1_hp += action["p1_hp"]
        total_p2_hp += action["p2_hp"]
        total_p1_res += action["p1_res"]
        total_p2_res += action["p2_res"]

st.divider()

# ---------- Preview ----------
st.subheader("Resulting Stats If Applied")
preview_p1_hp = st.session_state.p1_health + total_p1_hp
preview_p2_hp = st.session_state.p2_health + total_p2_hp
preview_p1_res = max(0, st.session_state.p1_resource + total_p1_res)
preview_p2_res = max(0, st.session_state.p2_resource + total_p2_res)

col1, col2 = st.columns(2)
with col1:
    st.metric("Player 1 Health", preview_p1_hp, preview_p1_hp - st.session_state.p1_health)
    st.metric("Player 1 Resource", preview_p1_res, preview_p1_res - st.session_state.p1_resource)
with col2:
    st.metric("Player 2 Health", preview_p2_hp, preview_p2_hp - st.session_state.p2_health)
    st.metric("Player 2 Resource", preview_p2_res, preview_p2_res - st.session_state.p2_resource)

st.divider()

# ---------- End Turn ----------
turn_number = st.session_state.turn
if st.button(f"End Turn {turn_number}"):
    # Apply previewed values
    st.session_state.p1_health = preview_p1_hp
    st.session_state.p2_health = preview_p2_hp
    st.session_state.p1_resource = preview_p1_res
    st.session_state.p2_resource = preview_p2_res

    # Save to history
    st.session_state.history["turn"].append(turn_number)
    st.session_state.history["p1_health"].append(st.session_state.p1_health)
    st.session_state.history["p2_health"].append(st.session_state.p2_health)
    st.session_state.history["p1_resource"].append(st.session_state.p1_resource)
    st.session_state.history["p2_resource"].append(st.session_state.p2_resource)

    # Check for game over
    if st.session_state.p1_health <= 0 or st.session_state.p2_health <= 0:
        st.session_state.game_over = True
        st.session_state.winner = st.session_state.p1_name if st.session_state.p2_health <= 0 else st.session_state.p2_name
        st.session_state.p1_emoji = ELEMENT_EMOJI.get(st.session_state.p1_element, "")
        st.session_state.p2_emoji = ELEMENT_EMOJI.get(st.session_state.p2_element, "")
        st.switch_page("pages/Game_Over.py")

    # Switch player
    st.session_state.active_player = "p2" if st.session_state.active_player == "p1" else "p1"
    st.session_state.turn += 1
    st.session_state.pending_actions = []
    st.rerun()
