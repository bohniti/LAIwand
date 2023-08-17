# Import Streamlit
import streamlit as st
from azure_services import create_response
import time
import azure_services as chatbot

# Here, import your application functions
# For example, you might have a file `azure_services.py` in the application folder:
# from application.azure_services import some_azure_function

# Placeholder function to simulate application processing
# Replace this with actual calls to Azure Cognitive Services in your application code

st.title("Test chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # for the response what to do ?? ==> send the prompt and return the repsonse from our chatgpt
        # ---------------------------------
        # ACTUAL USE OF FUNCTION HERE
        assistant_response = chatbot.create_response(prompt)
        # ---------------------------------
        # assistant_response = chatbot.generate_response(prompt)
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

def process_text(input_text):
    """
    Placeholder function to simulate application processing.
    In the real application, this function should call the Azure Cognitive Services API.
    For this demo, it reverses the input text.

    Args:
        input_text (str): The text input from the user.

    Returns:
        str: The processed (reversed, in this demo) text.
    """
    return input_text[::-1]
#
# # Streamlit App
# def main():
#     """
#     The main Streamlit application. This function defines the layout and flow of the app.
#     """
#     st.title('LAIwand Generative AI Demo')
#
#     st.write('Welcome to the LAIwand Generative AI Demo!')
#     st.write('This app is a prototype developed for the Accenture Corporate Hackathon.')
#
#     # Text input from the user
#     user_input = st.text_area("Please enter some text to process:")
#
#     # Button to trigger processing
#     if st.button('Process'):
#         if user_input:
#             # Here, we call our placeholder application function (or your real Azure function)
#             #result = process_text(user_input)
#             result = create_response(user_input)
#
#             # Display the result
#             st.write('Processed Text:')
#             st.write(result)
#         else:
#             st.warning('Please enter some text before pressing the "Process" button.')
#
# # Run the Streamlit app
# if __name__ == "__main__":
#     main()
