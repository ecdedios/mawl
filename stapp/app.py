import streamlit as st
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage
from langgraph.store.memory import InMemoryStore
from langgraph.graph import END
import graph_logic
import re

# Initialize Streamlit app
st.set_page_config(page_title="LangGraph Chatbot by Dd", layout="centered")
st.title("LangGraph Chatbot by Dd")
st.write("This chatbot uses LangGraph to manage long-term memory and provides personalized responses.")

# Initialize the InMemoryStore for state persistence
store = InMemoryStore()

# Application State
if "state" not in st.session_state:
    st.session_state.state = MessagesState(messages=[])
    st.session_state.graph_instance = graph_logic.graph  # The compiled graph from graph.py

# Define configuration
thread_input = st.text_input("Thread ID:", key="thread_input", placeholder="Enter thread ID here.")
username_input = st.text_input("Username:", key="username_input", placeholder="Enter username here.")
config = {"configurable": {"thread_id": thread_input, "user_id": username_input}}

# Define user input field
user_input = st.text_input("You:", key="user_input", placeholder="How can I help you?")

input_counter = 0
while user_input:
    # Add user message to state
    st.session_state.state["messages"].append(HumanMessage(content=user_input))
    # Execute the graph with the current state
    graph_instance = st.session_state.graph_instance
    result = list(graph_instance.stream({"messages": user_input}, config, stream_mode="values"))
    st.write(result[-1]["messages"][-1].content)
    user_input = st.text_input("You:", key="user_input"+str(input_counter))
    input_counter = input_counter + 1

# Footer
st.write("---")
st.markdown(
    "Built by [Dd](https://ednalyn.com) with [Streamlit](https://streamlit.io/) and [LangGraph](https://github.com/langchain-ai/langgraph)"
)

