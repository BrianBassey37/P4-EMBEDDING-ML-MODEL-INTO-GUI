import streamlit as st
import yaml


with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

def save_config():
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file)

def authenticate(username, password):
    if username in config['credentials']['usernames']:
        stored_password = config['credentials']['usernames'][username]['password']
        if password == stored_password:
            return True
    return False

st.set_page_config(
    page_title="Vodafone Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"  
)

st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to bottom, #800000, #FFFFFF); /* Wine red to milk white gradient */
        width: 100vw;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image('images\Vodafonelogo.jpg', use_column_width=True)
st.markdown("""
    Attrition Insight is a Machine Learning application that predicts the likelihood of an employee to leave the company based on various demographic and job-related factors.
 
    **Key Features**
    - View Data: Access proprietary data from IBM.
    - Dashboard: Explore interactive data visualizations for insights.
    - Real-time Prediction: Instantly see predictions for employee attrition.
    - History: See past predictions made.
 
    **User Benefits**
    - Data-driven Decisions: Make informed decisions backed by data analytics.
    - Easy Machine Learning: Utilize powerful machine learning algorithms effortlessly.
    - Live Demo: Watch a demo video to see the app in action.
 
    **How to run application**
    ```
    # activate virtual environment
    env/scripts/activate
    streamlit run 1_Home.py
    ```
 
    **Machine Learning Integration**
    - Model Selection: Choose between two advanced models for accurate predictions.
    - Seamless Integration: Integrate predictions into your workflow with a user-friendly interface.
    - Probability Estimates: Gain insights into the likelihood of predicted outcomes.
 
    """)

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state["name"] = username
        else:
            st.error("Invalid username or password. Please try again.")

def create_account():
    st.title("Create Account")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    if st.button("Create Account"):
        if new_username in config['credentials']['usernames']:
            st.error("Username already exists. Please choose a different username.")
        else:
            config['credentials']['usernames'][new_username] = {'email': '', 'logged_in': False, 'name': new_username, 'password': new_password}
            save_config()
            st.success("Account created successfully. You can now log in.")

if 'name' not in st.session_state:
    login()
    create_account()
else:
    st.success(f"Welcome, {st.session_state['name']}!")
    
