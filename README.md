# Intelligent Bus Inquiry Assistance Chat Bot 🚌

### <i> Overview: </i>
The Intelligent Bus Inquiry Assistance Chat Bot is an AI-powered application developed using FastAPI and Streamlit. It provides users with information about bus schedules, routes, fares, and more. The chatbot integrates tools like Wikipedia and DuckDuckGo, along with a custom knowledge base, to answer queries. The chat history is stored in a PostgreSQL database, and a user-friendly interface is available via Streamlit.

### <i> Demo Video: </i>

You can watch the demo of the Intelligent Bus Inquiry Assistance Chat Bot [here](https://www.loom.com/share/4b9b591ae3ad4b9e8a41e12bcdd00160?sid=f25c72e3-bd26-429a-8c67-868be977a0c3).

### <i> Features: </i>

<b> 1. Natural Language Processing: </b> Uses AI to understand and respond to user queries.

<b> 2. Multi-Tool Integration: </b> Combines Wikipedia, DuckDuckGo, and a custom knowledge base to provide comprehensive answers.

<b> 3. Chat History Management: </b> Stores and retrieves chat history from a PostgreSQL database.

<b> 4. Streamlit Interface: </b> User-friendly interface for querying and reviewing chat history.

<b> 5. API Documentation: </b> Accessible via Swagger UI for easy interaction and testing.

### <i> Prerequisites: </i>

- Python 3.8+
- FastAPI
- PostgreSQL
- SQLAlchemy
- LangChain and Community Tools
- Uvicorn
- Streamlit


### <i> Project Structure: </i>

``` bash
├── main.py                    # FastAPI application file
├── app.py                     # Streamlit interface file
├── .env                       # Environment variables file
├── requirements.txt           # List of dependencies
└── README.md                  # Project documentation (this file)
```

### <i> Setup: </i>

<b> 1. Clone the Repository: </b>
   
```bash

git clone https://github.com/drashtiadn/Final_Project.git

```
<b> 2. Create a virtual environment and install dependencies: </b>

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt

```

<b> 3. Set Up Environment Variables by creating a .env file in the root directory of the project with the following content: </b>

```bash
GOOGLE_API_KEY="your_google_api_key"
USER=postgres
DATABASE=chatdb
PASSWORD=password
HOST=localhost
PORT=5432
```

*** Replace the placeholder values with your actual PostgreSQL credentials and Google API key. ***

<b> 4. Initialize the Database by ensuring PostgreSQL is running and create the database: </b>

```bash
psql -U postgres -c "CREATE DATABASE chatdb;"
```

<b> 5. Run the FastAPI Application: </b>

```bash

uvicorn main:app --reload
```
The application will be available at http://127.0.0.1:8000.


<b> 6. Run the Streamlit Interface in a new terminal: </b>

```bash
streamlit run app.py
```

The Streamlit app will be available at http://localhost:8501.

### <i> Usage: </i>

<b> <i> 1. API Endpoints: </i> </b>

<b>         a. POST /ask: </b> Send a query to the chatbot and receive a response.

<i> Example request: </i>
```json
{
  "input": "What is the route for the airport?"
}
```


<b>         b. GET /chat_history: </b> Retrieve the chat history from the database.

<i> Parameters:</i>

- skip (int): Number of records to skip.

- limit (int):  Maximum number of records to return.

<i> Example request: </i>

```bash
http://127.0.0.1:8000/chat_history?skip=0&limit=10
```

<b> <i>2. API Documentation: </i> </b>

Access the interactive API documentation at:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

<b> <i>3. Using the Streamlit Interface: </i> </b>

- Submit Query: Enter your query in the input field and press "Submit" to get a response from the chatbot.

- View Chat History: Use the sidebar to select and view previous chat histories.

### <i> Contributing: </i>
Feel free to fork the repository, make improvements, and submit a pull request. All contributions are welcome!

This README.md file provides a complete guide for setting up and using your Intelligent Bus Inquiry Assistance Chat Bot, including instructions for running both the FastAPI backend and the Streamlit interface.
