import streamlit as st
import pandas as pd
import google.generativeai as genai

# ==============================
# 🎨 Page Configuration
# ==============================
st.set_page_config(page_title="Gemini Chatbot with Data Analysis", layout="wide")
st.title("🤖 Gemini Chatbot with CSV Data Analysis")
st.markdown("Upload your CSV file and chat with Gemini AI about your data!")

# ==============================
# 🔑 Gemini API Key Input
# ==============================
gemini_api_key = st.text_input("Gemini API Key:", type="password", placeholder="Enter your Gemini API Key")

# ==============================
# 🚀 Initialize Gemini Model
# ==============================
model = None
if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.success("Gemini API Key successfully configured!")
    except Exception as e:
        st.error(f"Error configuring Gemini model: {e}")

# ==============================
# 🧩 Session State Initialization
# ==============================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None

# ==============================
# 📂 File Uploader
# ==============================
st.subheader("Upload CSV for Analysis")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        st.session_state.uploaded_data = pd.read_csv(uploaded_file)
        st.success("File successfully uploaded!")
        st.write("### Uploaded Data Preview")
        st.dataframe(st.session_state.uploaded_data.head())
    except Exception as e:
        st.error(f"Error reading the file: {e}")

# ==============================
# ✅ Data Analysis Checkbox
# ==============================
analyze_data_checkbox = st.checkbox("Enable AI Data Analysis")

# ==============================
# 💬 Display Chat History
# ==============================
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# ==============================
# 🧠 Chat Input
# ==============================
user_input = st.chat_input("Type your message here...")

if user_input:
    # Store and display user message
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    if model:
        try:
            # Case: Data Uploaded & Analysis Enabled
            if st.session_state.uploaded_data is not None and analyze_data_checkbox:
                if "analyze" in user_input.lower() or "insight" in user_input.lower():
                    # Prepare Data Summary
                    data_summary = st.session_state.uploaded_data.describe(include="all").to_string()
                    prompt = (
                        "You are an expert data analyst.\n"
                        "Analyze the following dataset and provide insights:\n\n"
                        f"{data_summary}\n\n"
                        f"User question: {user_input}"
                    )
                    response = model.generate_content(prompt)
                    bot_response = response.text
                else:
                    # General Question
                    response = model.generate_content(user_input)
                    bot_response = response.text

            # Case: Data Analysis Disabled
            elif not analyze_data_checkbox:
                bot_response = "⚠️ Data analysis is disabled. Please enable the checkbox to analyze the CSV data."

            # Case: No Data Uploaded
            else:
                bot_response = "⚠️ Please upload a CSV file first to enable data analysis."

            # Display and Store Assistant Response
            st.session_state.chat_history.append(("assistant", bot_response))
            with st.chat_message("assistant"):
                st.markdown(bot_response)

        except Exception as e:
            st.error(f"An error occurred: {e}")

    else:
        st.warning("⚠️ Please enter your Gemini API Key to enable chat.")
