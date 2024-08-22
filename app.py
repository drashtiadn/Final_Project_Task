import streamlit as st
import requests
from typing import List
from datetime import datetime

# Define a function to fetch chat history from the FastAPI endpoint
def get_chat_history(skip: int = 0, limit: int = 100):
    try:
        response = requests.get(f"http://127.0.0.1:8000/chat_history?skip={skip}&limit={limit}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching chat history: {e}")
        return []

# Streamlit interface
st.title("Intelligent Bus Inquiry Assistance Chat Bot 🚌")

# Sidebar for chat history
st.sidebar.title("Chat History")
chat_histories = get_chat_history()
if chat_histories:
    # Create a dictionary to map chat index to chat record
    chat_options = {f"Chat {i+1} - {chat['timestamp']}": chat for i, chat in enumerate(chat_histories)}
    selected_chat = st.sidebar.selectbox("Select a chat history", list(chat_options.keys()))

    # Display selected chat history
    if selected_chat:
        chat = chat_options[selected_chat]
        st.sidebar.write(f"**User Input:** {chat['user_input']}")
        st.sidebar.write(f"**Agent's Response:** {chat['agent_response']}")
        st.sidebar.write(f"**Timestamp:** {chat['timestamp']}")
else:
    st.sidebar.write("No chat history available.")

# User input
user_input = st.text_input("Enter your query:")

if st.button("Submit"):
    if user_input:
        # Send a POST request to FastAPI
        response = requests.post("http://127.0.0.1:8000/ask", json={"input": user_input})
        if response.status_code == 200:
            result = response.json()
            st.write(result["response"])
        else:
            st.error("Error: Unable to get the response from the server.")
    else:
        st.warning("Please enter a query.")