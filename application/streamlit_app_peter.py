import openai
import plotly.express as px
import streamlit as st
import json
import pandas as pd
import helpers
import sl_test_graph


def setup():
    st.title("ChatGPT-like clone")

    credentials = helpers.load_json("./application/credentials.json")
    config = helpers.load_json("./application/config.json")

    openai.api_key = credentials['api_key']
    openai.api_type = credentials['api_type']
    openai.api_base = credentials['api_base']
    openai.api_version = credentials['api_version']

    model_engine = config['model_engine']
    temperature = config['temperature']

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    return model_engine, temperature


def ask_for_intent_confirmation(prompt, model_engine, temperature):
    intent_response = openai.ChatCompletion.create(
        engine=model_engine,
        temperature=temperature,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    intent_text = intent_response.choices[0].message.get("content", "Do you mean: ...?")
    return intent_text


def process_intent(model_engine, temperature):
    # The logic that should run after the user confirms their intent goes here.
    # This can include querying the model again, processing the response, etc.

    with st.chat_message("user"):
        st.markdown(st.session_state.prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
                engine=model_engine,
                temperature=temperature,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

        sql_query = helpers.parse_sql_query(full_response)
        st.write(sql_query)

        result = helpers.execute_sql_query_on_dataframe("./application/train.csv", sql_query)

        explanation_prompt = f"Please explain the result of this SQL query: {result}"
        st.session_state.messages.append({"role": "user", "content": explanation_prompt})
        explanation_response = openai.ChatCompletion.create(
            engine=model_engine,
            temperature=temperature,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        )

        if hasattr(explanation_response.choices[0], 'delta'):
            explanation_text = explanation_response.choices[0].delta.get("content",
                                                                         "Sorry, I couldn't understand the result.")
        elif hasattr(explanation_response.choices[0], 'message'):
            explanation_text = explanation_response.choices[0].message.get("content",
                                                                           "Sorry, I couldn't understand the result.")
        else:
            explanation_text = "Sorry, I couldn't understand the result."

        st.write(explanation_text)
        st.write(result)

        visualize_data()


def visualize_data():
    # Should be passed to function
    graph_type = "bar"
    # graph_type = "clustered_bar"

    if graph_type == "bar":
        # plot_config_path = "./application/sl_graph_config/sl_graph_bar_config.json"
        # data_path = "./application/sl_graph_data/sl_graph_bar_data.json"
        plot_config_path = "C:/Users/peter.j.lingner/OneDrive - Accenture/Accenture Docs/Opportunity/Vienna Hackathon/GIT Code/LAIwand/application/sl_graph_config/sl_graph_bar_config.json"
        data_path = "C:/Users/peter.j.lingner/OneDrive - Accenture/Accenture Docs/Opportunity/Vienna Hackathon/GIT Code/LAIwand/application/sl_graph_data/sl_graph_bar_data.json"


    elif graph_type == "clustered_bar":
        # plot_config_path = "./application/sl_graph_config/sl_graph_clustered_bar_config.json"
        # data_path = "./application/sl_graph_data/sl_graph_clustered_bar_data.json"
        plot_config_path = "C:/Users/peter.j.lingner/OneDrive - Accenture/Accenture Docs/Opportunity/Vienna Hackathon/GIT Code/LAIwand/application/sl_graph_config/sl_graph_clustered_bar_config.json"
        data_path = "C:/Users/peter.j.lingner/OneDrive - Accenture/Accenture Docs/Opportunity/Vienna Hackathon/GIT Code/LAIwand/application/sl_graph_data/sl_graph_clustered_bar_data.json"

    plot_config = helpers.load_json(plot_config_path)
    data_config = helpers.load_json(data_path)

    # Convert data to DataFrame
    df = pd.DataFrame(data_config["data"])

    # Generate the appropriate plot based on the graph_type
    if graph_type == "bar":
        fig = px.bar(
            df,
            x=plot_config["x_axis"]["column"],
            y=plot_config["y_axis"]["column"],
            color=plot_config["group_by"],
            title=plot_config["chart_title"],
            labels={
                plot_config["x_axis"]["column"]: data_config["headers"][plot_config["x_axis"]["column"]],
                plot_config["y_axis"]["column"]: data_config["headers"][plot_config["y_axis"]["column"]],
                plot_config["group_by"]: data_config["headers"][plot_config["group_by"]]
            },
            barmode='group'
        )

    elif graph_type == "clustered_bar":

        # Pivot the data to have 'metric' values as columns
        df_pivot = df.pivot_table(index=['year', 'district'], columns='metric', values='value').reset_index()

        # Flatten the column MultiIndex
        df_pivot.columns = [col if not isinstance(col, tuple) else col[1] for col in df_pivot.columns]

        fig = px.bar(
            df_pivot,
            x=plot_config["x_axis"]["column"],
            y=[col for col in plot_config["y_columns"]],
            color=plot_config["group_by"],
            title=plot_config["chart_title"],
            labels={col: data_config["headers"].get(col, col) for col in
                    [plot_config["x_axis"]["column"], *plot_config["y_columns"], plot_config["group_by"]]},
            barmode='group'
        )

    st.title(plot_config["chart_title"])
    st.plotly_chart(fig, use_container_width=True)


def run_app():
    model_engine, temperature = setup()

    # Check and initialize session states
    if 'intent_confirmed' not in st.session_state:
        st.session_state.intent_confirmed = False
    if 'prompt' not in st.session_state:
        st.session_state.prompt = None

    # Show previous chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if not st.session_state.prompt:
        st.session_state.prompt = st.chat_input("Hallo wie kann ich Ihnen helfen?")

    if st.session_state.prompt and not st.session_state.intent_confirmed:
        intent_text = ask_for_intent_confirmation(st.session_state.prompt, model_engine, temperature)
        st.session_state.messages.append({"role": "user", "content": st.session_state.prompt})
        with st.chat_message("assistant"):
            st.markdown(intent_text)

        if st.button("Confirm the above intent"):
            st.session_state.intent_confirmed = True

    if st.session_state.intent_confirmed:
        # Logic after confirmation goes here
        process_intent(model_engine, temperature)
        with st.chat_message("assistant"):
            st.markdown("Thank you for confirming! Your intent has been recognized and is being processed.")
        # Reset states for the next interaction
        st.session_state.intent_confirmed = False
        st.session_state.prompt = None
        st.session_state.messages = []


# Call the function to run the app
run_app()