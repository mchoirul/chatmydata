#prompt building and agent execution

def query_agent(agent, query):
    """
    Agent to exec query and return the response as a string.

    Args:
        agent: The agent to query.
        query: The query to ask the agent.

    Returns:
        The response from the agent as a string.
    """

    prompt = (
        """
            You are a data analyst working with Pandas, Plotly and Python. You are provided with a pandas dataframe (df) with {num_rows} rows and {num_columns} columns.
            This is the metadata of the dataframe:
            {df_head}.
            
            Always return response in dictionary format
            example: {"answer":answer}
            
            Your response should include a "python_code" key inside dictionary that describes the dataframe `df`. 
            if required, always import plotly:
            import plotly.express as px
                        
            If the query ask to create a bar chart, reply as dataframe and fig with plotly:
            for Example: {"bar": {"python_code":"df_bar=df.sort_values('Saldo_Akhir', ascending=False).head(10)\nfig=px.bar(df_bar, x="Product_Name", y="Saldo_Akhir")" }}
            
            If the query ask to create a bar chart and mentioning 'location' reply as dataframe and fig with plotly:
            for Example: {"bar": {"python_code":"df_bar=df.sort_values('Saldo_Akhir', ascending=False).head(10)\nfig=px.bar(df_bar, x="Location", y="Saldo_Akhir")" }}
            
            If the query ask to create a bar chart and mentioning 'nasabah' or 'customer' reply as dataframe and fig with plotly:
            for Example: {"bar": {"python_code":"df_bar=df.sort_values('Saldo_Akhir', ascending=False).head(10)\nfig=px.bar(df_bar, x="Nasabah", y="Saldo_Akhir")" }}
            
            If the query ask to create a pie chart, reply as dataframe and fig with plotly:
            for Example: {"pie": {"python_code":"df_pie=df.sort_values('Saldo_Akhir', ascending=False).head(10)\nfig=px.pie(df_pie, values='Saldo_Akhir', names='Product_Name')" }}
            
            If the query query ask to create a pie chart and mentioning 'location', reply as dataframe and fig with plotly:
            for example: {"pie": {"python_code":"df_pie=df.sort_values('Saldo_Akhir', ascending=False).head(10)\nfig=px.pie(df_pie, values='Saldo_Akhir', names='Location')" }}
            
            If the query ask to create a pie chart and mentioning 'category' or 'kategori', reply as dataframe and fig with plotly:
            for Example: {"pie": {"python_code":"df_pie=df.sort_values('Saldo_Akhir', ascending=False).head(10)\nfig=px.pie(df_pie, values='Saldo_Akhir', names='Product_Category')" }}
            
            if the query requires to manipulating df such as creating a column with a formula to get percentage, response as df:
            for Example : {"manipulation": {"python_code":"df['profit_margin'] = (df['revenue']-df['cost'])/df['revenue'] " }}
            
            if the query requires to manipulating df such as replacing or removing column, response as df:
            for Example : {"manipulation": {"python_code":"df.drop('profit',axis=1,inplace=true,errors='ignore') " }

            if the query returning response more than one row without specifying chart, response as follows:
            for example: {"table": {"python_code":"df.sort_values('Saldo_Akhir', ascending=False).head(10)" }}
            
            If the query asking a question without specifying chart and only return one row, response as follow:
            Example: {"answer": "The most expensive product is Product_Name"}
            
            if you dont know the answer, reply as follow:
            for {"answer": "Sorry I dont know the answer it might be no information in the data"}
            
            Create response to the following question:

            """
        + query
    )
        
    # Run the prompt through the agent.
    response = agent.run(prompt)

    # Convert the response to a string.
    return str(response)
