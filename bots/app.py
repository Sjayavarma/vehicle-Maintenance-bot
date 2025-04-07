import streamlit as st
import pandas as pd
import openai
import os

# 🔐 OpenAI API Key
openai.api_key = # your open api sceret key --> to create 

# 📦 Load Excel Data
def load_data():
    file_path = "vehicle_faults.xlsx"
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    else:
        st.error("❌ vehicle_faults.xlsx not found!")
        return pd.DataFrame()

# 🔍 Diagnose Faults
def diagnose_issue(symptom, df):
    if df.empty:
        return pd.DataFrame()
    return df[df['Symptom_Description'].str.contains(symptom, case=False, na=False)]

# 🛠 Maintenance Scheduler
def generate_maintenance_schedule(mileage, terrain, weather):
    schedule = []
    if mileage > 5000:
        schedule.append("🛢️ Engine Oil Change")
    if mileage > 10000:
        schedule.append("🧰 Brake Inspection")
    if terrain == "Mountainous":
        schedule.append("⚙️ Suspension Check")
    if weather in ["Rainy", "Snowy"]:
        schedule.append("🧽 Wiper & Tyre Inspection")
    if not schedule:
        schedule.append("✅ No immediate maintenance needed.")
    return schedule

# 🤖 Chatbot Assistant
def get_chatbot_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert vehicle maintenance assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

# 🗺️ Route Optimization Logic
def optimize_route(traffic_condition, weather_condition):
    if traffic_condition == "Heavy" or weather_condition == "Rainy":
        return "Suggested Route: Take Highway B → Use Flyover → Reach Destination"
    else:
        return "Suggested Route: Highway A → Main Street → Destination"

# 🗺️ Generate Google Maps Embed URL
def generate_google_maps_embed(start, end):
    api_key = "AIzaSyD9GDmZ7ZuKY0MrocFSeqXLkYOHlNmJQ60"
    embed_url = (
        f"https://www.google.com/maps/embed/v1/directions"
        f"?key={api_key}&origin={start}&destination={end}&mode=driving"
    )
    return embed_url

# 🚘 Main Streamlit App
def main():
    st.set_page_config(page_title="🚘 Vehicle Maintenance Expert System", layout="wide")
    st.title("🚘 Vehicle Maintenance & Assistance Expert System")

    df = load_data()

    # Sidebar Navigation
    menu = st.sidebar.radio("Choose Module", [
        "Vehicle Fault Diagnosis",
        "Maintenance Scheduler",
        "Chatbot Assistant",
        "Route Optimization"
    ])

    # 1️⃣ Vehicle Fault Diagnosis
    if menu == "Vehicle Fault Diagnosis":
        st.header("🔧 Vehicle Fault Diagnosis")
        symptom_input = st.text_input("Enter symptom (e.g., engine misfire, overheating)")
        if st.button("Diagnose Issue"):
            if symptom_input:
                results = diagnose_issue(symptom_input, df)
                if not results.empty:
                    st.success("✅ Possible Causes and Recommendations:")
                    st.dataframe(results[['Possible_Cause', 'Severity_Level', 'Recommended_Action']])
                else:
                    st.warning("⚠️ No matching issues found.")
            else:
                st.info("ℹ️ Please enter a symptom.")

    # 2️⃣ Maintenance Scheduler
    elif menu == "Maintenance Scheduler":
        st.header("🛠️ Predictive Maintenance Schedule")
        mileage = st.number_input("Enter vehicle mileage (km):", min_value=0)
        terrain = st.selectbox("Select Terrain Type", ["City", "Highway", "Mountainous"], key="terrain_select")
        weather = st.selectbox("Current Weather Condition", ["Clear", "Rainy", "Snowy"], key="weather_select")
        if st.button("Generate Schedule"):
            schedule = generate_maintenance_schedule(mileage, terrain, weather)
            st.success("🧾 Recommended Maintenance Tasks:")
            for task in schedule:
                st.markdown(f"- {task}")

    # 3️⃣ Chatbot Assistant
    elif menu == "Chatbot Assistant":
        st.header("💬 Chat with Vehicle Assistant")
        user_question = st.text_area("Ask me anything about your vehicle issue:")
        if st.button("Get Response"):
            if user_question.strip():
                response = get_chatbot_response(user_question)
                st.success("🤖 Assistant Response:")
                st.write(response)
            else:
                st.info("ℹ️ Please type a question first.")

    # 4️⃣ Route Optimization
    elif menu == "Route Optimization":
        st.header("🧭 Route Optimization")
        col1, col2 = st.columns(2)
        with col1:
            start_location = st.text_input("Start Location", "Chennai")
        with col2:
            end_location = st.text_input("Destination", "Bangalore")

        col3, col4 = st.columns(2)
        with col3:
            traffic = st.selectbox("Traffic Condition", ["Light", "Moderate", "Heavy"], key="traffic")
        with col4:
            weather = st.selectbox("Weather Condition", ["Clear", "Rainy", "Snowy"], key="weather")

        if st.button("Optimize Route"):
            suggestion = optimize_route(traffic, weather)
            st.success(f"📌 Route Suggestion:\n{suggestion}")

            st.markdown("#### 🗺 Google Maps Route")
            embed_url = generate_google_maps_embed(start_location, end_location)
            st.components.v1.iframe(embed_url, height=450)

if __name__ == "__main__":
    main()
