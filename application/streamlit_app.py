# Import Streamlit

import streamlit as st
from azure_services import create_response
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import azure_services as chatbot
from datetime import time

# Here, import your application functions
# For example, you might have a file `azure_services.py` in the application folder:
# from application.azure_services import some_azure_function

# Placeholder function to simulate application processing
# Replace this with actual calls to Azure Cognitive Services in your application code


# Streamlit App



def main():
    """
    The main Streamlit application. This function defines the layout and flow of the app.
    """
    st.title('LAIwand Generative AI Demo')

    st.write('Welcome to the LAIwand Generative AI Demo!')
    st.write('This app is a prototype developed for the Accenture Corporate Hackathon.')

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

    # Add histogram data
    x1 = np.random.randn(200) - 2
    x2 = np.random.randn(200)
    x3 = np.random.randn(200) + 2

    # Group data together
    hist_data = [x1, x2, x3]
    group_labels = ['Group 1', 'Group 2', 'Group 3']

    # Create distplot with custom bin_size
    fig = ff.create_distplot(hist_data, group_labels, bin_size=[.1, .25, .5])

    # Create a 3-column layout
    col1, col2, col3 = st.columns(3)

    # Use the middle column for the plot
    col2.plotly_chart(fig, use_container_width=True)

# Run the Streamlit app
if __name__ == "__main__":
    main()
