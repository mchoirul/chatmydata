import streamlit as st
import pandas as pd
import json
import os
from agent import query_agent
from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import VertexAI
from google.cloud import aiplatform
from google.oauth2 import service_account
import matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
from langchain.memory import ConversationBufferWindowMemory

# reference:
# https://github.com/Ngonie-x/langchain_csv/tree/main
# https://github.com/chatgpt/chart

    
#assign credential. replace project_id and credential
mycredential = service_account.Credentials.from_service_account_file(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
myproject=os.environ["PROJECT_ID"]

aiplatform.init(project=myproject, location='us-central1',credentials=mycredential)

@st.cache_data
def convert_df(df):
    # Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def decode_response(response: str) -> dict:
    """converts the string response from the model to a dictionary object.

    Args:
        response (str): response from the model

    Returns:
        dict: dictionary with response data
    """
    return json.loads(response,strict=False)


def write_response(response_dict: dict):
    """
    Write a response from an agent to a Streamlit app.

    Args:
        response_dict: The response from the agent.

    Returns:
        None.
    """
            
    # write output to streamlit
    # plot chart using plotly if required
    
    # if response is "answer"
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    # if response is bar chart
    elif "bar" in response_dict:
        code =response_dict['bar']['python_code']
        exec(code,globals())
        st.plotly_chart(fig,theme=None, use_container_width=True)
            
    # if response is pie chart
    elif "pie" in response_dict:
        code =response_dict['pie']['python_code']
        exec(code,globals())
        st.plotly_chart(fig,theme=None, use_container_width=True)
            
    # if response is scatter chart
    elif "scatter" in response_dict:
        code =response_dict['scatter']['python_code']
        exec(code,globals())
        st.plotly_chart(fig,theme=None, use_container_width=True)
        
    # if response is line chart
    elif "line" in response_dict:
        code =response_dict['line']['python_code']
        exec(code,globals())
        st.plotly_chart(fig,theme=None, use_container_width=True)

    # if response is Manipulation or using formula
    elif "manipulation" in response_dict:
                
        code =response_dict['manipulation']['python_code']
        exec(code,globals())
        csv = convert_df(df)
        st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='df.csv',
        mime='text/csv',key="manipulation"+str(uniq))
                
        st.write(df)
                
    # if response from agent is table
    elif "table" in response_dict:
        code="df_temp="+response_dict['table']['python_code']
        exec(code,globals())
        csv = convert_df(df_temp)
        st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='df.csv',
        mime='text/csv',key="table"+str(uniq))
        st.write(df_temp)
                
            
    else:
        st.write(response_dict)



st.title("👨‍💻 Chat with your data")

st.write("Please upload your CSV file below.")
with st.sidebar:
    option = st.selectbox("Model Temperature", [0,0.1, 0.2, 0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
                
# upload csv
data = st.file_uploader("Upload a CSV")
if data is not None:
    df  = pd.read_csv(data)
    reset_df=df
    st.write(df)
            
            
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

len_msg=len(st.session_state.messages)
uniq=len_msg

# Display chat messages from history on app rerun
for message in st.session_state.messages:
            
    try:
        uniq=uniq+1
                
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                if "{" in message["content"]:
                    decoded_history = decode_response(message["content"])
                else:
                    decoded_history = message["content"]
                    
                        
                if type(decoded_history) == dict: 
                    decoded_history = decoded_history
                else:
                    decoded_history = str(decoded_history)
                write_response(decoded_history)
            else:
                st.markdown(message["content"])
    except Exception as e:
        st.error(f"An error occurred: please try another query/question")

# capture query from user input
if prompt := st.chat_input("Enter your prompt:"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    uniq=uniq+1
    try:
        with st.spinner('Please wait...'):
            
            # chat memory up to 3 previous requests
            memory = ConversationBufferWindowMemory(memory_key="chat_history",k=3)
            
            #declare llm
            llm = VertexAI(model_name="text-bison@001",
                           temperature=option, 
                           max_retry=3)
                
            agent=create_pandas_dataframe_agent(llm, df, memory=memory, verbose=True)
            response = query_agent(agent=agent, query=prompt)
            if "{" in response:
                decoded_response = decode_response(response)
            else:
                decoded_response = response
                
                
            
            if type(decoded_response) == dict: 
                decoded_response = decoded_response
            else:
                decoded_response = str(decoded_response)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.write("Here the answer : ")
            write_response(decoded_response)
            
    except Exception as e:
        st.error(f"An error occurred: please try another query/question")

        
                    
    uniq=uniq+1
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


with st.sidebar:
    reset_button_key = "reset_button"
    reset_button = st.button("Reset Chat",key=reset_button_key)
    if reset_button:
        st.session_state.messages = []
        
