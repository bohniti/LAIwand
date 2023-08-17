for chunk in assistant_response.split():
    full_response += chunk + " "
    time.sleep(0.05)
    # Add a blinking cursor to simulate typing
    message_placeholder.markdown(full_response + "▌")