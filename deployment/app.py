import streamlit as st
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage
from langgraph.store.memory import InMemoryStore
from langgraph.graph import END
import graph

from inspect import signature

# Print the signature of the method
print(signature(graph_instance.invoke))
print(signature(Pregel.stream))


# Initialize Streamlit app
st.set_page_config(page_title="LangGraph Chatbot", layout="centered")
st.title("LangGraph Chatbot")
st.write("This chatbot uses LangGraph to manage long-term memory and provides personalized responses.")

# Initialize the InMemoryStore for state persistence
store = InMemoryStore()

# Application State
if "state" not in st.session_state:
    st.session_state.state = MessagesState(messages=[])
    st.session_state.graph_instance = graph.graph  # The compiled graph from graph.py

# Define user input field
user_input = st.text_input("You:", key="user_input", placeholder="Enter your message here...")

# Display messages
if st.session_state.state["messages"]:
    st.write("---")
    for msg in st.session_state.state["messages"]:
        role = "System" if msg.role == "system" else "You"
        st.markdown(f"**{role}:** {msg['content']}")

print(signature(graph_instance.invoke))
print(signature(Pregel.stream))
print(store)

# Handle user input
if user_input:
    # Add user message to state
    st.session_state.state["messages"].append(HumanMessage(content=user_input))

    # Execute the graph with the current state
    graph_instance = st.session_state.graph_instance
    result = graph_instance.invoke(
    input={"state": st.session_state.state},  # Define the initial state
    config={},  # Configuration if needed
    store=store  # Pass the memory store
)



    # Check if we've reached the end
    if result == END:
        st.warning("The conversation has reached its end state.")
    else:
        # Add graph's response to messages
        st.session_state.state["messages"].extend(result.get("messages", []))

    # Clear input field
    st.experimental_rerun()

# Footer
st.write("---")
st.markdown(
    "Built with [Streamlit](https://streamlit.io/) and [LangGraph](https://github.com/langchain-ai/langgraph)"
)
