from datetime import datetime

import streamlit as st
from langchain_core.messages import HumanMessage

from auth import login_user, register_user
from db_utils import delete_user_trip, get_user_trips, init_auth_db, rename_user_trip, save_user_trip
from main import app


st.set_page_config(
    page_title="TripwiseAI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_auth_db()


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background: #ffffff;
    color: #121a2b;
}

.block-container {
    max-width: 1180px;
    padding-top: 1.5rem;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.auth-shell {
    max-width: 538px;
    margin: 1.2rem auto 0;
    border: 1px solid #d4d9e2;
    border-radius: 8px;
    padding: 1.5rem 1.25rem 1.85rem;
    background: #ffffff;
}

.auth-brand-title {
    color: #ff4651;
    font-size: 2rem;
    font-weight: 800;
    line-height: 1.1;
    text-align: center;
}

.auth-brand-subtitle {
    color: #2563eb;
    font-size: 1rem;
    font-weight: 700;
    margin-top: 0.35rem;
    margin-bottom: 1.1rem;
    text-align: center;
}

.auth-title {
    color: #050b1f;
    font-size: 1.85rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0.25rem;
}

.auth-subtitle {
    color: #5b6678;
    font-size: 1rem;
    text-align: center;
    margin-bottom: 1.55rem;
}

.auth-switch {
    color: #5b6678;
    text-align: center;
    margin: 1.1rem 0 0.2rem;
}

div[data-testid="stFormSubmitButton"] > button {
    background: #ff4651 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 9px !important;
    min-height: 3.1rem !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    box-shadow: none !important;
}

div[data-testid="stFormSubmitButton"] > button:hover {
    background: #ef3d48 !important;
    box-shadow: none !important;
    transform: none !important;
}

.stTextInput input, .stTextArea textarea {
    background: #f0f2f6 !important;
    border: 1px solid #e4e8ef !important;
    border-radius: 9px !important;
    color: #121a2b !important;
}

.stTextInput input {
    min-height: 3.1rem !important;
}

.stTextArea textarea {
    min-height: 118px !important;
}

.stTextInput label, .stTextArea label {
    color: #121a2b !important;
    font-size: 0.98rem !important;
    font-weight: 500 !important;
}

section[data-testid="stSidebar"] {
    background: #f7f9fc !important;
    border-right: 1px solid #d9e3f0 !important;
}

.sidebar-title {
    color: #121a2b;
    font-size: 1rem;
    font-weight: 800;
    margin: 1rem 0 0.5rem;
}

.sidebar-chip {
    background: #ffffff;
    border: 1px solid #d9e3f0;
    border-radius: 8px;
    color: #4b5f78;
    font-size: 0.84rem;
    margin-bottom: 0.45rem;
    padding: 0.55rem 0.7rem;
}

.trip-history-card {
    background: #ffffff;
    border: 1px solid #d9e3f0;
    border-radius: 8px;
    color: #4b5f78;
    font-size: 0.84rem;
    min-height: 3.1rem;
    padding: 0.55rem 0.7rem;
}

.trip-history-card strong {
    color: #121a2b;
}

.hero-wrapper {
    position: relative;
    border-radius: 18px;
    overflow: hidden;
    margin-bottom: 1.5rem;
    height: 285px;
}

.hero-wrapper::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, rgba(8, 18, 32, 0.9), rgba(8, 18, 32, 0.58), rgba(8, 18, 32, 0.16));
    z-index: 1;
}

.hero-bg {
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(0.9);
    position: absolute;
    inset: 0;
}

.hero-content {
    position: relative;
    z-index: 2;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}

.hero-badge {
    background: rgba(255, 255, 255, 0.14);
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 999px;
    color: #dbeafe;
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    padding: 0.35rem 0.85rem;
    text-transform: uppercase;
}

.hero-title {
    color: #ffffff;
    font-size: 2.7rem;
    font-weight: 800;
    line-height: 1.1;
    margin: 0.8rem 0 0.5rem;
}

.hero-sub {
    color: #d8e7f8;
    font-size: 1rem;
    max-width: 650px;
}

.section-title {
    color: #121a2b;
    font-size: 1rem;
    font-weight: 800;
    margin: 1.2rem 0 0.75rem;
}

.destination-card {
    border-radius: 10px;
    height: 92px;
    overflow: hidden;
    position: relative;
    background-size: cover;
    background-position: center;
}

.destination-card::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(0, 0, 0, 0.04), rgba(0, 0, 0, 0.68));
}

.destination-card span {
    position: absolute;
    z-index: 2;
    left: 0.75rem;
    right: 0.75rem;
    bottom: 0.55rem;
    color: #ffffff;
    font-size: 0.86rem;
    font-weight: 800;
    text-align: center;
}

div[data-testid="stButton"] > button {
    border-radius: 10px !important;
    font-weight: 800 !important;
}

.metric-row {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1rem;
    margin: 1.25rem 0;
}

.metric-box {
    background: #ffffff;
    border: 1px solid #d9e3f0;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}

.metric-val {
    color: #2563eb;
    font-size: 1.55rem;
    font-weight: 800;
}

.metric-lbl {
    color: #60748f;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.final-card {
    background: #ffffff;
    border: 1px solid #d9e3f0;
    border-left: 4px solid #2563eb;
    border-radius: 12px;
    color: #121a2b;
    line-height: 1.75;
    padding: 1.35rem;
}

.save-bar {
    background: #f3f7fc;
    border: 1px solid #d9e3f0;
    border-radius: 10px;
    color: #46617f;
    padding: 0.85rem 1rem;
}

[data-testid="stStatusWidget"] {
    background: #ffffff !important;
    border: 1px solid #d9e3f0 !important;
    border-radius: 10px !important;
}

[data-testid="stStatusWidget"] * {
    color: #121a2b !important;
}
</style>
""",
    unsafe_allow_html=True,
)


def set_logged_in_user(user):
    st.session_state.logged_in = True
    st.session_state.user_id = user["id"]
    st.session_state.username = user["username"]


def make_trip_title(user_query: str, max_length: int = 42) -> str:
    title = " ".join(user_query.strip().split())
    if not title:
        return f"Trip {datetime.now().strftime('%Y-%m-%d')}"
    if len(title) <= max_length:
        return title
    return title[: max_length - 3].rstrip(" ,.-") + "..."


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"


if not st.session_state.logged_in:
    _, auth_col, _ = st.columns([1, 1.35, 1])
    with auth_col:
        title = "Welcome back" if st.session_state.auth_mode == "login" else "Create account"
        subtitle = (
            "Login to continue your travel workspace."
            if st.session_state.auth_mode == "login"
            else "Register to save your personal trip history."
        )

        
        st.markdown("<div class='auth-shell'>", unsafe_allow_html=True)
        st.markdown("<div class='auth-brand-title'>✈️ Tripwise</div>", unsafe_allow_html=True)
        st.markdown("<div class='auth-brand-subtitle'>AI Trip Booking System</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='auth-title'>{title}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='auth-subtitle'>{subtitle}</div>", unsafe_allow_html=True)

        with st.form("auth_form", clear_on_submit=False):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_label = "Login" if st.session_state.auth_mode == "login" else "Register"
            submitted = st.form_submit_button(submit_label, use_container_width=True)

        if submitted:
            if st.session_state.auth_mode == "login":
                user = login_user(username, password)
                if user:
                    set_logged_in_user(user)
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
            else:
                user = register_user(username, password)
                if user:
                    set_logged_in_user(user)
                    st.rerun()
                else:
                    st.error("Username already exists or fields are empty.")

        if st.session_state.auth_mode == "login":
            st.markdown("<div class='auth-switch'>New user?</div>", unsafe_allow_html=True)
            if st.button("Register", use_container_width=True):
                st.session_state.auth_mode = "register"
                st.rerun()
        else:
            st.markdown("<div class='auth-switch'>Already have an account?</div>", unsafe_allow_html=True)
            if st.button("Login", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


with st.sidebar:
    st.markdown(f"<div class='sidebar-title'>Welcome, {st.session_state.username}</div>", unsafe_allow_html=True)
    if st.button("Logout", use_container_width=True):
        for key in ["logged_in", "user_id", "username"]:
            st.session_state.pop(key, None)
        st.session_state.auth_mode = "login"
        st.rerun()

    st.markdown("---")
    st.markdown("<div class='sidebar-title'>Your Trip History</div>", unsafe_allow_html=True)
    user_trips = get_user_trips(st.session_state.user_id)
    if user_trips:
        for trip in user_trips[:8]:
            trip_id = trip["id"]
            trip_col, menu_col = st.columns([0.78, 0.22], gap="small")
            with trip_col:
                st.markdown(
                    f"<div class='trip-history-card'><strong>{trip['trip_name']}</strong><br>{trip['created_at']}</div>",
                    unsafe_allow_html=True,
                )
            with menu_col:
                action = st.selectbox(
                    "...",
                    ["...", "Rename", "Delete"],
                    key=f"trip_action_{trip_id}",
                    label_visibility="collapsed",
                )
            if action == "Rename":
                new_name = st.text_input(
                    "New trip name",
                    value=trip["trip_name"],
                    key=f"rename_input_{trip_id}",
                    label_visibility="collapsed",
                )
                if st.button("Save rename", key=f"rename_btn_{trip_id}", use_container_width=True):
                    if rename_user_trip(st.session_state.user_id, trip_id, new_name):
                        st.success("Trip renamed.")
                        st.rerun()
                    else:
                        st.error("Enter a valid trip name.")
            elif action == "Delete":
                st.warning("Delete this trip from your history?")
                if st.button("Delete trip", key=f"delete_btn_{trip_id}", use_container_width=True):
                    if delete_user_trip(st.session_state.user_id, trip_id):
                        st.success("Trip deleted.")
                        st.rerun()
    else:
        st.caption("No saved trips yet.")

    st.markdown("<div class='sidebar-title'>Powered by</div>", unsafe_allow_html=True)
    for tech in ["LangGraph", "Groq LLaMA 3.3 70B", "PostgreSQL", "Tavily Search", "AviationStack"]:
        st.markdown(f"<div class='sidebar-chip'>{tech}</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-title'>Agent Pipeline</div>", unsafe_allow_html=True)
    for step in ["1. Flight Agent", "2. Hotel Agent", "3. Itinerary Agent", "4. Final Agent"]:
        st.markdown(f"<div class='sidebar-chip'>{step}</div>", unsafe_allow_html=True)


st.markdown(
    """
<div class="hero-wrapper">
    <img class="hero-bg"
         src="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1400&q=80"
         alt="scenic travel landscape"/>
    <div class="hero-content">
        <div class="hero-badge">Multi-Agent AI System</div>
        <div class="hero-title">Tripwise AI Travel Booking System</div>
        <div class="hero-sub">Four specialized agents search flights, hotels, build an itinerary, and deliver your travel plan.</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


st.markdown("<div class='section-title'>Choose a travel mood</div>", unsafe_allow_html=True)
destinations = [
    ("Beach Escape", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=300&q=70"),
    ("Mountain Trip", "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&q=70"),
    ("City Break", "https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=300&q=70"),
    ("Forest Stay", "https://images.unsplash.com/photo-1448375240586-882707db888b?w=300&q=70"),
    ("Island Holiday", "https://images.unsplash.com/photo-1500375592092-40eb2168fd21?w=300&q=70"),
]

cols = st.columns(5)
for col, (name, image_url) in zip(cols, destinations):
    with col:
        st.markdown(
            f"<div class='destination-card' style='background-image:url({image_url});'><span>{name}</span></div>",
            unsafe_allow_html=True,
        )


st.markdown("<div class='section-title'>Describe your trip</div>", unsafe_allow_html=True)
quick_options = [
    "7-day beach trip under Rs 2L",
    "5-day city break",
    "Weekend mountain getaway",
    "10-day island backpacking",
]
quick_cols = st.columns(len(quick_options))
quick_fill = ""
for col, label in zip(quick_cols, quick_options):
    with col:
        if st.button(label, key=f"quick_{label}", use_container_width=True):
            quick_fill = label

user_query = st.text_area(
    "Trip details",
    value=quick_fill,
    placeholder="Example: Plan a 7-day beach trip from Mumbai under Rs 2 lakhs with flights, hotels, food and sightseeing.",
    label_visibility="collapsed",
)

generate = st.button("Generate My Travel Plan", type="primary", use_container_width=True)

agent_meta = {
    "flight_agent": "Flight Agent",
    "hotel_agent": "Hotel Agent",
    "itinerary_agent": "Itinerary Agent",
    "final_agent": "Final Agent",
}

if generate:
    if not user_query.strip():
        st.warning("Please describe your trip first.")
        st.stop()

    trip_title = make_trip_title(user_query)
    thread_id = f"user_{st.session_state.user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    config = {"configurable": {"thread_id": thread_id}}
    collected = {
        "flight_results": "",
        "hotel_results": "",
        "itinerary": "",
        "final_response": "",
        "llm_calls": 0,
    }

    st.markdown("<div class='section-title'>Agent Pipeline - Live</div>", unsafe_allow_html=True)

    for chunk in app.stream(
        {
            "messages": [HumanMessage(content=user_query)],
            "user_query": user_query,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "llm_calls": 0,
        },
        config=config,
        stream_mode="updates",
    ):
        for node_name, state_update in chunk.items():
            label = agent_meta.get(node_name, node_name)
            with st.status(label, state="complete", expanded=True):
                if node_name == "flight_agent":
                    collected["flight_results"] = state_update.get("flight_results", "")
                    st.markdown(collected["flight_results"] or "_No flight data returned._")
                elif node_name == "hotel_agent":
                    collected["hotel_results"] = state_update.get("hotel_results", "")
                    st.markdown(collected["hotel_results"] or "_No hotel data returned._")
                elif node_name == "itinerary_agent":
                    collected["itinerary"] = state_update.get("itinerary", "")
                    st.markdown(collected["itinerary"] or "_No itinerary generated._")
                elif node_name == "final_agent":
                    messages = state_update.get("messages", [])
                    collected["final_response"] = messages[-1].content if messages else ""
                    st.markdown(collected["final_response"] or "_No final response._")

                collected["llm_calls"] = state_update.get("llm_calls", collected["llm_calls"])

    st.markdown(
        f"""
<div class="metric-row">
    <div class="metric-box"><div class="metric-val">4</div><div class="metric-lbl">Agents Run</div></div>
    <div class="metric-box"><div class="metric-val">{collected['llm_calls']}</div><div class="metric-lbl">LLM Calls</div></div>
    <div class="metric-box"><div class="metric-val">Done</div><div class="metric-lbl">Status</div></div>
</div>
""",
        unsafe_allow_html=True,
    )

    if collected["final_response"]:
        st.markdown("<div class='section-title'>Final Travel Plan</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='final-card'>{collected['final_response']}</div>", unsafe_allow_html=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"user_{st.session_state.user_id}_{timestamp}.md"
    file_content = f"""# Travel Plan
**Trip:** {trip_title}
**Query:** {user_query}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**User:** {st.session_state.username}

---

## Flight Information
{collected['flight_results'] or 'N/A'}

---

## Hotel Information
{collected['hotel_results'] or 'N/A'}

---

## Itinerary
{collected['itinerary'] or 'N/A'}

---

## Final Travel Plan
{collected['final_response'] or 'N/A'}

---
*LLM Calls: {collected['llm_calls']}*
"""

    save_user_trip(
        user_id=st.session_state.user_id,
        thread_id=thread_id,
        trip_name=trip_title,
        user_query=user_query,
        file_content=file_content,
    )

    download_col, info_col = st.columns([1, 3])
    with download_col:
        st.download_button(
            "Download Plan",
            data=file_content,
            file_name=filename,
            mime="text/markdown",
            use_container_width=True,
        )
    with info_col:
        st.markdown("<div class='save-bar'>Auto-saved to your PostgreSQL trip history.</div>", unsafe_allow_html=True)
