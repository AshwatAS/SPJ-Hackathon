import streamlit as st
import pandas as pd
from datetime import datetime
from utils import generate, clinic_booking  # Your custom Gemini functions

# Load datasets
@st.cache_data
def load_data():
    menu = pd.read_csv("restaurant_menu_final_expanded.csv")[["Item_Name", "Description"]]
    clinic = pd.read_csv("updated_clinic_appointments.csv")[["Doctor Name", "Specialization"]]
    return menu, clinic
menu_df, clinic_df = load_data()

# Page Setup
st.set_page_config(page_title="Smart Assistant App", layout="wide", page_icon="🤖")
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-size: 16px;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Smart Assistant: Food Ordering & Clinic Booking")

# Initial Screen
if "screen" not in st.session_state:
    st.session_state.screen = "home"

# Navigation Handler
if st.session_state.screen == "home":
    st.subheader("What would you like to do today?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🍽️ Order Food", help="Explore our menu and get food recommendations"):
            st.session_state.screen = "food_chat"
    with col2:
        if st.button("🏥 Book Clinic Appointment", help="Check doctor availability and book an appointment"):
            st.session_state.screen = "clinic_chat"

# Food Chat Interface
elif st.session_state.screen == "food_chat":
    st.subheader("🍴 Chat with Food Assistant")
    st.write("### 📜 Menu Overview")
    st.dataframe(menu_df, use_container_width=True)
    if "food_chat_history" not in st.session_state:
        st.session_state.food_chat_history = []

    for chat in st.session_state.food_chat_history:
        st.chat_message("user").markdown(f"**🧑‍💬:** {chat['user']}")
        st.chat_message("assistant").markdown(f"**🤖:** {chat['bot']}")

    user_input = st.chat_input("Ask about menu, combos, vegan dishes, etc.")
    if user_input:
        response = generate(user_input)
        st.session_state.food_chat_history.append({"user": user_input, "bot": response})
        st.chat_message("user").markdown(f"**🧑‍💬:** {user_input}")
        st.chat_message("assistant").markdown(f"**🤖:** {response}")

    st.button("🔙 Back to Home", on_click=lambda: st.session_state.update({"screen": "home"}))

# Clinic Chat Interface
elif st.session_state.screen == "clinic_chat":
    st.subheader("💬 Chat with Clinic Assistant")
    st.write("### 📅 Available Appointments")
    st.dataframe(clinic_df, use_container_width=True)
    if "clinic_chat_history" not in st.session_state:
        st.session_state.clinic_chat_history = []

    for chat in st.session_state.clinic_chat_history:
        st.chat_message("user").markdown(f"**🧑‍💬:** {chat['user']}")
        st.chat_message("assistant").markdown(f"**🤖:** {chat['bot']}")

    user_input = st.chat_input("Ask about doctor availability, fees, appointments...")
    if user_input:
        response = clinic_booking(user_input)
        st.session_state.clinic_chat_history.append({"user": user_input, "bot": response})
        st.chat_message("user").markdown(f"**🧑‍💬:** {user_input}")
        st.chat_message("assistant").markdown(f"**🤖:** {response}")

    st.button("🔙 Back to Home", on_click=lambda: st.session_state.update({"screen": "home"}))

