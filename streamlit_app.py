import streamlit as st
import pandas as pd
from datetime import datetime

# Load datasets
@st.cache_data
def load_data():
    menu = pd.read_csv("restaurant_menu_final_expanded.csv")
    try:
        clinic = pd.read_csv("clinic_appointments.csv")
    except:
        clinic = pd.DataFrame(columns=["Doctor Name", "Specialization", "Available Date", "Available Time", "Consultation Fee"])
    return menu, clinic

menu_df, clinic_df = load_data()

st.title("🍽️ Restaurant & 🏥 Clinic Booking System")

# Sidebar Navigation
choice = st.sidebar.radio("Select Service", ["Order Food", "Book Clinic Appointment", "Admin Panel"])

if choice == "Order Food":
    st.header("Order from Our Restaurant Menu")
    dietary_pref = st.multiselect("Choose your dietary preference:", ["Vegetarian", "Gluten-Free", "Vegan"])
    spice_level = st.selectbox("Preferred Spice Level", ["Any", "Mild", "Medium", "Hot", "Extra Spicy"])
    category = st.multiselect("Select Category", menu_df["Category"].unique())

    filtered_menu = menu_df.copy()
    if "Vegetarian" in dietary_pref:
        filtered_menu = filtered_menu[filtered_menu["Vegetarian"] == "Yes"]
    if "Gluten-Free" in dietary_pref:
        filtered_menu = filtered_menu[filtered_menu["Gluten-Free"] == "Yes"]
    if "Vegan" in dietary_pref:
        filtered_menu = filtered_menu[filtered_menu["Vegan"] == "Yes"]
    if spice_level != "Any":
        filtered_menu = filtered_menu[filtered_menu["Spice Level"].str.contains(spice_level, case=False)]
    if category:
        filtered_menu = filtered_menu[filtered_menu["Category"].isin(category)]

    st.dataframe(filtered_menu)

    selected_items = st.multiselect("Select items to order:", filtered_menu["Item Name"].tolist())
    if selected_items:
        total_price = filtered_menu[filtered_menu["Item Name"].isin(selected_items)]["Price"].sum()
        st.success(f"Total Price: ₹{total_price}")
        if st.button("Confirm Order"):
            st.balloons()
            st.success("Order placed! Your food will be ready in approx 20 minutes.")

elif choice == "Book Clinic Appointment":
    st.header("Book an Appointment at the Clinic")
    st.dataframe(clinic_df)

    doctor_name = st.selectbox("Choose Doctor:", clinic_df["Doctor Name"].unique())
    selected_doctor = clinic_df[clinic_df["Doctor Name"] == doctor_name]
    date_selected = st.date_input("Choose Appointment Date:")

    doctor_available = selected_doctor[selected_doctor["Available Date"] == str(date_selected)]

    if not doctor_available.empty:
        time_slot = st.selectbox("Available Time Slot:", doctor_available["Available Time"].unique())
        st.success(f"Appointment confirmed with {doctor_name} on {date_selected} at {time_slot}.")
    else:
        st.warning("No slots available for the selected doctor on this date.")

elif choice == "Admin Panel":
    st.header("Upload/Manage Datasets")
    uploaded_menu = st.file_uploader("Upload Updated Restaurant Menu CSV", type=["csv"])
    if uploaded_menu:
        new_menu = pd.read_csv(uploaded_menu)
        new_menu.to_csv("restaurant_menu_final_expanded.csv", index=False)
        st.success("New menu uploaded successfully!")

    uploaded_clinic = st.file_uploader("Upload Updated Clinic Appointment CSV", type=["csv"])
    if uploaded_clinic:
        new_clinic = pd.read_csv(uploaded_clinic)
        new_clinic.to_csv("clinic_appointments.csv", index=False)
        st.success("New clinic data uploaded successfully!")

