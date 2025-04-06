import streamlit as st
import pandas as pd
import google.generativeai as genai

# ==============================
# Page Configuration
# ==============================
st.set_page_config(page_title="Gemini AI Python Code Generator for DataFrame", layout="wide")
st.title("🤖 Gemini AI Python Code Generator for DataFrame")
st.markdown("AI will generate Python code to answer your DataFrame questions!")

# ==============================
# Gemini API Key Input
# ==============================
gemini_api_key = st.text_input("Gemini API Key:", type="password", placeholder="Enter your Gemini API Key")

# Initialize Gemini Model
model = None
if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-2.0-flash-lite")
        st.success("Gemini API Key successfully configured!")
    except Exception as e:
        st.error(f"Error setting up the Gemini model: {e}")

# ==============================
# Session State Initialization
# ==============================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None

# ==============================
# Load Data From Local Files
# ==============================

try:
    # Read data from local files
    data_file = "transactions.csv"
    data_dict_file = "data_dict.csv"

    # Load data
    df_data = pd.read_csv(data_file)
    df_dict = pd.read_csv(data_dict_file)

    # Store in session state
    st.session_state.uploaded_data = df_data

    st.success(f"✅ Successfully loaded '{data_file}' and '{data_dict_file}'")
    st.write("### 📊 Data Preview")
    st.dataframe(df_data.head())

    st.write("### 📖 Data Dictionary")
    st.dataframe(df_dict.head())

except Exception as e:
    st.error(f"Error loading data files: {e}")
    df_data = None
    df_dict = None

# ==============================
# Enable Analysis Checkbox
# ==============================
analyze_data_checkbox = st.checkbox("Enable AI Code Generation for Data Analysis")

# ==============================
# Display Chat History
# ==============================
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# ==============================
# Chat Input
# ==============================
if user_input := st.chat_input("Type your data question here..."):

    # Store and display user message
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Process user input
    if model:
        try:
            if st.session_state.uploaded_data is not None and analyze_data_checkbox:

                df_name = "df_data"
                data_dict_text = df_dict.to_string()
                example_record = df_data.head(2).to_string()

                # === Use your advanced prompt ===
                prompt = f"""
You are a helpful Python code generator.
Your goal is to write Python code snippets based on the user's question
and the provided DataFrame information.

Here's the context:

**User Question:**
{user_input}

**DataFrame Name:**
{df_name}

**DataFrame Details:**
{data_dict_text}

**Sample Data (Top 2 Rows):**
{example_record}

**Instructions:**

1. Write Python code that addresses the user's question by querying or manipulating the DataFrame.
2. **Crucially, use the `exec()` function to execute the generated code.**
3. Do not import pandas
4. Change date column type to datetime
5. **Store the result of the executed code in a variable named `ANSWER`.**
    This variable should hold the answer to the user's question (e.g., a filtered DataFrame, a calculated value, etc.).
6. Assume the DataFrame is already loaded into a pandas DataFrame object
named `{df_name}`. Do not include code to load the DataFrame.
7. Keep the generated code concise and focused on answering the question.
8. If the question requires a specific output format (e.g., a list, a single value), ensure the `ANSWER` variable holds that format.

**Example:**
If the user asks: "Show me the rows where the 'age' column is greater than 30."
And the DataFrame has an 'age' column.

The generated code should look something like this (inside the `exec()` string):

```python
query_result = {df_name}[{df_name}['age'] > 30]
ANSWER = query_result
