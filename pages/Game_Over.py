import streamlit as st
import pandas as pd
import altair as alt
import smtplib
from email.message import EmailMessage

st.set_page_config(page_title="Game Over", layout="centered")

# ---------- Guard ----------
if not st.session_state.get("game_over", False):
    st.warning("No finished game to show.")
    st.stop()

# ---------- Winner ----------
winner = st.session_state.get("winner", "Unknown")
st.title("🏆 Game Over!")
st.subheader(f"{winner} Wins!")
st.divider()

# ---------- Element emojis ----------
ELEMENT_EMOJI = {"Water": "💧", "Earth": "🌱", "Fire": "🔥"}
p1_emoji = ELEMENT_EMOJI.get(st.session_state.get("p1_element", "Water"), "")
p2_emoji = ELEMENT_EMOJI.get(st.session_state.get("p2_element", "Water"), "")

# ---------- Final Stats ----------
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"### {st.session_state.p1_name} {p1_emoji}")
    st.metric("Health", st.session_state.p1_health)
    st.metric("Resource", st.session_state.p1_resource)

with col2:
    st.markdown(f"### {st.session_state.p2_name} {p2_emoji}")
    st.metric("Health", st.session_state.p2_health)
    st.metric("Resource", st.session_state.p2_resource)

st.divider()

# ---------- Graph of Health & Resource ----------
if "history" in st.session_state:
    # Element colors: (Dark = Health, Light = Resource)
    ELEMENT_COLOR = {
        "Water": ("#1E90FF", "#87CEFA"),  # Dark Blue / Light Blue
        "Earth": ("#006400", "#32CD32"),  # Dark Green / Light Green
        "Fire": ("#8B0000", "#FF4500"),   # Dark Red / Bright Red
    }

    # Collect history
    turns = st.session_state.history["turn"]
    p1_health_history = st.session_state.history["p1_health"]
    p2_health_history = st.session_state.history["p2_health"]
    p1_resource_history = st.session_state.history["p1_resource"]
    p2_resource_history = st.session_state.history["p2_resource"]

    # ---------- Insert Turn 0 ----------
    turns = [0] + turns
    p1_health_history = [st.session_state.p1_health_start] + p1_health_history
    p2_health_history = [st.session_state.p2_health_start] + p2_health_history
    p1_resource_history = [st.session_state.p1_resource_start] + p1_resource_history
    p2_resource_history = [st.session_state.p2_resource_start] + p2_resource_history

    # Prepare tidy dataframe
    data = []

    # Player 1
    dark1, light1 = ELEMENT_COLOR.get(st.session_state.get("p1_element", "Water"))
    for t, h, r in zip(turns, p1_health_history, p1_resource_history):
        data.append({"Turn": t, "Player": st.session_state.p1_name, "Stat": "Health", "Value": h, "Color": dark1})
        data.append({"Turn": t, "Player": st.session_state.p1_name, "Stat": "Resource", "Value": r, "Color": light1})

    # Player 2
    dark2, light2 = ELEMENT_COLOR.get(st.session_state.get("p2_element", "Water"))
    for t, h, r in zip(turns, p2_health_history, p2_resource_history):
        data.append({"Turn": t, "Player": st.session_state.p2_name, "Stat": "Health", "Value": h, "Color": dark2})
        data.append({"Turn": t, "Player": st.session_state.p2_name, "Stat": "Resource", "Value": r, "Color": light2})

    df = pd.DataFrame(data)
    df["Label"] = df["Player"] + " - " + df["Stat"]

    # Map each Label to its color
    labels = df["Label"].unique()
    colors = [df.loc[df["Label"] == label, "Color"].iloc[0] for label in labels]

    # Altair chart
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X("Turn:O", title="Turn"),
        y=alt.Y("Value:Q", title="Value"),
        color=alt.Color("Label:N", scale=alt.Scale(domain=labels, range=colors),
                        legend=alt.Legend(title="Player & Stat")),
        tooltip=["Label", "Value", "Turn"]
    ).properties(
        title="Health & Resource Over Turns",
        width=700,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

st.divider()

# ---------- Prepare CSV ----------
history = st.session_state.get("history", {})
turns = history.get("turn", [])
p1_health = history.get("p1_health", [])
p1_resource = history.get("p1_resource", [])
p2_health = history.get("p2_health", [])
p2_resource = history.get("p2_resource", [])

# Include player info
data = []
for i, t in enumerate(turns):
    data.append({
        "Turn": t,
        "Player": st.session_state.p1_name,
        "Element": st.session_state.p1_element,
        "Gridlord": st.session_state.p1_gridlord,
        "Health": p1_health[i],
        "Resource": p1_resource[i]
    })
    data.append({
        "Turn": t,
        "Player": st.session_state.p2_name,
        "Element": st.session_state.p2_element,
        "Gridlord": st.session_state.p2_gridlord,
        "Health": p2_health[i],
        "Resource": p2_resource[i]
    })

df = pd.DataFrame(data)

# ---------- Download CSV ----------
csv = df.to_csv(index=False)
st.download_button(
    label="📥 Download Game CSV",
    data=csv,
    file_name="gridborne_game_history.csv",
    mime="text/csv"
)

# ---------- Email CSV ----------
st.divider()
st.subheader("📧 Send CSV by Email")

email_to = st.text_input("Recipient Email", "")
send_button = st.button("Send CSV")

if send_button:
    if not email_to:
        st.error("Please enter an email address!")
    else:
        # Create email
        msg = EmailMessage()
        msg['Subject'] = "GridBorne Game Report"
        msg['From'] = "your_email@example.com"  # your email
        msg['To'] = email_to
        msg.set_content("Attached is the GridBorne game report.")

        # Attach CSV
        msg.add_attachment(csv.encode('utf-8'),
                           maintype='text',
                           subtype='csv',
                           filename="gridborne_game_history.csv")
        try:
            # Connect to SMTP server (example: Gmail)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login("wparryslop1@gmail.com", "rtzl fycb hnhj phsb")  # app password if Gmail
                smtp.send_message(msg)
            st.success(f"✅ CSV sent to {email_to}!")
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")

# ---------- Play Again ----------
if st.button("Play Again"):
    keys_to_clear = [
        "setup_complete","p1_name","p2_name","p1_health","p2_health",
        "p1_resource","p2_resource","p1_gridlord","p2_gridlord",
        "p1_element","p2_element","active_player","turn",
        "pending_actions","game_over","winner","p1_emoji","p2_emoji","history",
        "p1_health_start","p2_health_start","p1_resource_start","p2_resource_start"
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
