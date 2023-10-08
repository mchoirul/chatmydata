# chatmydata
interact with your data in natural language, powered by LLM. automatically generate visualization in pie chart, bar chart, and others. 
Components used:
- Google text-bison@001 model from Vertex AI Palm API
- Langchain
- Streamlit

## Use case
- upload sample csv our your own csv
- ask questions about data inside csv
- depending on the prompt, chatmydata will show the response in table, chart, or text

## Installation
Tested on Python 3.9x
Create Python virtual enviroment and install dependencies:
pip install -r requirements.txt

## Run chatmydata
streamlit run chatmydata.py
