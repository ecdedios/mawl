import streamlit as st
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langgraph.store.memory import InMemoryStore
import configuration

# Initialize the model, store, and graph for LangGraph
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
store = InMemoryStore()

# Set up a simple LangGraph as in the provided code
builder = StateGraph(MessagesState, config_schema=configuration.Configuration)
builder.add_node(task_master)
builder.add_node(update_todos)
builder.add_node(update_profile)
builder.add_node(update_instructions)
builder.add_edge(START, "task_master")
builder.add_conditional_edges("task_master", route_message)
builder.add_edge("update_todos", "task_master")
builder.add_edge("update_profile", "task_master")
builder.add_edge("update_instructions", "task_master")
graph = builder.compile()

# Define streamlit interface for profile and To-Do creation
st.title("Personal Assistant Chatbot")
st.write("Interact with your personal profile, tasks, and preferences.")

# Input fields for Profile
with st.form("profile_form"):
    st.header("User Profile")
    name = st.text_input("Your Name", "")
    location = st.text_input("Location", "")
    job = st.text_input("Job", "")
    connections = st.text_area("Connections", "")
    interests = st.text_area("Interests", "")
    submit_profile = st.form_submit_button("Update Profile")
    
    if submit_profile:
        st.write(f"Updating profile with: Name: {name}, Location: {location}, Job: {job}")
        # Trigger LangGraph process to update profile
        state = {
            'messages': [{"role": "user", "content": f"Name: {name}, Location: {location}, Job: {job}, Connections: {connections}, Interests: {interests}"}]
        }
        config = configuration.Configuration(user_id="user-123", todo_category="default", task_master_role="assistant")
        result = graph.invoke(state=state, config=config, store=store)
        st.write("Profile updated successfully!")

# Input fields for ToDo
with st.form("todo_form"):
    st.header("Add a Task")
    task = st.text_input("Task", "")
    mode = st.selectbox("Mode", ["anywhere", "errand", "home", "online", "phone"])
    time_to_complete = st.number_input("Time to Complete (minutes)", min_value=1, max_value=600, value=30)
    deadline = st.date_input("Deadline", None)
    location_todo = st.text_input("Location to complete the task", "")
    bizhours_flag = st.checkbox("Is the task within business hours?", False)
    status = st.selectbox("Task Status", ["not started", "in progress", "done", "archived"])
    solutions = st.text_area("Solutions (if any)", "")

    submit_todo = st.form_submit_button("Add Task")
    
    if submit_todo:
        st.write(f"Adding Task: {task}, Mode: {mode}, Status: {status}")
        # Trigger LangGraph process to add task
        state = {
            'messages': [{"role": "user", "content": f"Add Task: {task}, Mode: {mode}, Status: {status}, Solutions: {solutions}, Time: {time_to_complete} minutes"}]
        }
        config = configuration.Configuration(user_id="user-123", todo_category="default", task_master_role="assistant")
        result = graph.invoke(state=state, config=config, store=store)
        st.write("Task added successfully!")

# Add additional section to view or update instructions if required
with st.expander("Instructions for To-Do List Updates"):
    current_instructions = st.text_area("Update Instructions", "")
    update_instructions_btn = st.button("Update Instructions")
    
    if update_instructions_btn:
        # Process instructions update
        state = {
            'messages': [{"role": "user", "content": current_instructions}]
        }
        config = configuration.Configuration(user_id="user-123", todo_category="default", task_master_role="assistant")
        result = graph.invoke(state=state, config=config, store=store)
        st.write("Instructions updated successfully!")
