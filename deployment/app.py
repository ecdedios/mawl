import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph.store.memory import InMemoryStore
from graph import invoke_our_graph, task_master, update_todos, update_profile, update_instructions
import uuid
from configuration import Configuration

from langchain_core.callbacks import BaseCallback

class MyCallback(BaseCallback):
    def on_chain_start(self, serialized: dict):
        # You can log or inspect the chain start here
        print("Chain is starting", serialized)

    def on_chain_end(self, serialized: dict):
        # Handle end of chain
        print("Chain has ended", serialized)

# Initialize the store to keep track of memory
store = InMemoryStore()

# This defines the layout of the Streamlit app
st.title("Memory-based Task Manager")

# Load or create a Configuration instance
# You could fetch dynamic values for the user from user input, environment vars, etc.
config = Configuration(user_id=str(uuid.uuid4()), todo_category="work")

# Allow users to choose their Todo category dynamically
todo_category = st.selectbox("Select Todo Category", ["work", "personal", "study", "shopping"])

# Create a text input area for user chat
user_input = st.text_area("Talk to the Task Master:", height=200)

if user_input:
    # Handle user message and trigger memory updates
    user_message = HumanMessage(content=user_input)
    
    # Retrieve messages from the session state for chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Append user's input message to the conversation history
    st.session_state.messages.append(user_message)
    
    # Retrieve the user_id from config and the selected todo_category dynamically
    user_id = config.user_id  # Use config attribute
    namespace = (todo_category.lower(), config.todo_category, user_id)

    # Define the callback list
    callbacks = [MyCallback()]

    # Compile and invoke the graph with dynamic todo_category
    try:
        # Now, you can pass it when invoking the graph or chain
        response = invoke_our_graph(st.session_state.messages, callables=[task_master, update_todos, update_profile, update_instructions], callbacks=callbacks)
        # response = invoke_our_graph(st.session_state.messages, callables=[task_master, update_todos, update_profile, update_instructions], callbacks=callbacks)
        # response = invoke_our_graph(st.session_state.messages, [task_master, update_todos, update_profile, update_instructions])

        # Display the response from the chatbot
        response_message = response["messages"][0]["content"]
        st.write(f"Task Master: {response_message}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
