import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st

# ✅ Load .env file
load_dotenv()

# ✅ Get Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    # In a Streamlit app, it's better to show an error message
    # than to raise an exception.
    st.error("❌ GEMINI_API_KEY missing! Please set it in your .env file.")
    st.stop()

# ✅ Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# ✅ Load model
model = genai.GenerativeModel("gemini-2.5-flash")

# ✅ Prompt engineering
def enhance_prompt(user_query: str) -> str:
    return f"""
    You are Sandeep, a  AI Expert, 
    Your goal is to provide clear, practical, and friendly answers.
    - Be empathetic and understanding.
    - Break down complex topics into easy-to-understand points.
    - Use examples and analogies to clarify your explanations.
    - If you don't know the answer, say so honestly.
    - Keep your answers concise and to the point.
    - Use formatting, such as bullet points or numbered lists, to structure your response when appropriate.
    -you are mot right code , only give the definition.
    - you are a sandeep ai assistant, not a code assistant.

    Here's an example of a good response:

    User: "How does a black hole work?"
    AI: "A black hole is a region of spacetime where gravity is so strong that nothing, not even light, can escape. Here's a simple analogy:
    *   Imagine a trampoline representing spacetime.
    *   A bowling ball placed on the trampoline creates a dip.
    *   A marble rolled nearby will fall into the dip.
    A black hole is like an extremely heavy bowling ball that creates a very deep dip, trapping anything that comes too close."

    Now, here's the user's query:

    User: "{user_query}"
    AI:
    """.strip()

# ✅ Get AI response
def get_chat_response(user_message: str) -> str:
    prompt = enhance_prompt(user_message)
    response = model.generate_content(prompt)
    return response.text

# ✅ Streamlit UI
def main():
    st.set_page_config(page_title="Universal AI Assistant", page_icon="🤖")
    
    st.title("🤖 Universal AI Assistant (Gemini)")
    st.write("Ask me anything!")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get AI response
        with st.spinner("Thinking..."):
            response = get_chat_response(prompt)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
