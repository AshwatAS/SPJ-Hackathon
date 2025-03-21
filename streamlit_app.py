import streamlit as st
import pandas as pd
from datetime import datetime
from utils import generate, clinic_booking  # Your custom Gemini functions

# Load datasets
@st.cache_data
def load_data():
    menu = pd.read_csv("restaurant_menu_final_expanded.csv")
    clinic = pd.read_csv("clinic_appointments.csv")
    return menu, clinic

menu_df, clinic_df = load_data()

# Page Setup
st.set_page_config(page_title="Smart Assistant App", layout="centered")
st.title("🤖 Smart Assistant: Food Ordering & Clinic Booking")

# Initial Screen
if "screen" not in st.session_state:
    st.session_state.screen = "home"

# Navigation Handler
if st.session_state.screen == "home":
    st.subheader("What would you like to do today?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🍽️ Order Food"):
            st.session_state.screen = "food_chat"
    with col2:
        if st.button("🏥 Book Clinic Appointment"):
            st.session_state.screen = "clinic_chat"

# Food Chat Interface
elif st.session_state.screen == "food_chat":
    st.subheader("🍴 Chat with Food Assistant")
    st.dataframe(menu_df)
    if "food_chat_history" not in st.session_state:
        st.session_state.food_chat_history = []

    for chat in st.session_state.food_chat_history:
        st.chat_message("user").markdown(chat["user"])
        st.chat_message("assistant").markdown(chat["bot"])

    user_input = st.chat_input("Ask about menu, combos, vegan dishes, etc.")
    if user_input:
        response = generate(user_input)
        st.session_state.food_chat_history.append({"user": user_input, "bot": response})
        st.chat_message("user").markdown(user_input)
        st.chat_message("assistant").markdown(response)

    st.button("🔙 Back to Home", on_click=lambda: st.session_state.update({"screen": "home"}))

# Clinic Chat Interface
elif st.session_state.screen == "clinic_chat":
    st.subheader("💬 Chat with Clinic Assistant")
    st.dataframe(clinic_df)
    if "clinic_chat_history" not in st.session_state:
        st.session_state.clinic_chat_history = []

    for chat in st.session_state.clinic_chat_history:
        st.chat_message("user").markdown(chat["user"])
        st.chat_message("assistant").markdown(chat["bot"])

    user_input = st.chat_input("Ask about doctor availability, fees, appointments...")
    if user_input:
        response = clinic_booking(user_input)
        st.session_state.clinic_chat_history.append({"user": user_input, "bot": response})
        st.chat_message("user").markdown(user_input)
        st.chat_message("assistant").markdown(response)

    st.button("🔙 Back to Home", on_click=lambda: st.session_state.update({"screen": "home"}))
