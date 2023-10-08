# chatmydata
interact with your data in natural language, powered by LLM. automatically generate visualization in pie chart, bar chart, and others. 
Components used:
- Google text-bison@001 model from Vertex AI Palm API
- Langchain
- Streamlit

<img src="https://github.com/mchoirul/chatmydata/blob/main/screenshots/chadata6.png" width="600" /> 

## Use case
- upload sample csv : [bankfinance.csv](https://github.com/mchoirul/chatmydata/blob/main/bankfinance.csv)
- ask questions about data inside csv
- depending on the prompt, chatmydata will show the response in table, chart, or text

## Installation
Tested on Python 3.9x
Create Python virtual enviroment and install dependencies:
```
pip install -r requirements.txt
```
## Run chatmydata
```
streamlit run chatmydata.py
```

## Usage examples
chatmydata was tested to receive questions in English and Bahasa Indonesia.

### Example 1:
- Ask in English
<img src="https://github.com/mchoirul/chatmydata/blob/main/screenshots/chadata1.png" width="600" />

### Example 2:
<img src="https://github.com/mchoirul/chatmydata/blob/main/screenshots/chadata2.png" width="600" />

### Example 3:
<img src="https://github.com/mchoirul/chatmydata/blob/main/screenshots/chadata3.png" width="600" />

### Example 4:
- Now switch question to Bahasa Indonesia
<img src="https://github.com/mchoirul/chatmydata/blob/main/screenshots/chadata4.png" width="600" />

### Example 5:
<img src="https://github.com/mchoirul/chatmydata/blob/main/screenshots/chadata5.png" width="600" />

## Run as Docker Image
Use Dockerfile 
