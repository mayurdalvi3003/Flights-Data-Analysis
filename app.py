import streamlit as st
from DBhelper import DB
import plotly.express as go
import plotly.graph_objects as px
import pandas as pd
db = DB()

st.sidebar.title("Flights Analytics")
user_option = st.sidebar.selectbox("Menu" , ['Select One' , 'Check Flights' ,'Analytics'])
if user_option == "Check Flights":
    st.title("Check Flights")
    col1 , col2 = st.columns(2)

    city = db.fetch_city_names()
    with col1:
        source = st.selectbox("Source",sorted(city))
    with col2:
        destination = st.selectbox("Destination",sorted(city))

    if st.button("Search"):
        results = db.fetch_all_flights(source , destination)
        st.dataframe(results)

elif user_option =="Analytics":
    st.title("Analytics")

    st.header("Top Airlines by no.of Flights")
    airline , freq = db.fetch_ariline_freq()
    fig = go.pie(names=airline, values=freq)
    fig.update_traces(textinfo='label+value', hoverinfo='label+value+percent') # i dont want values in percentage , i want my original values for the same i made this changes
    # Display the pie chart in Streamlit
    st.plotly_chart(fig)


    st.header("Average Price per Airline")

    # Fetch data
    airline, price = db.avg_price_per_airline()

    # Create the figure
    fig = px.Figure()

    # Add bar chart with data labels
    fig.add_trace(px.Bar(
        x=airline,
        y=price,
        text=price,
        textposition='outside',  # Position of data labels
        marker=dict(color='pink'),  # Customize bar color if needed
    ))

    # Update layout if needed
    fig.update_layout(
        xaxis_title='Airline',
        yaxis_title='Price',
    )

    # Display the plot
    st.plotly_chart(fig)



    st.header("Total Number of Stops by Route")
    col1 , col2 = st.columns(2)

    city = db.fetch_city_names()
    with col1:
        source = st.selectbox("Source",sorted(city))
    with col2:
        destination = st.selectbox("Destination",sorted(city))

    if st.button("Check"):
        # Call the method and get the result
        results = db.stops_by_route(source, destination)
        st.header(results)
        

    st.header("Busy Airpot")
    city, freq = db.busy_airpot()
    # Create the figure
    fig = px.Figure()
    # Add bar chart with data labels
    fig.add_trace(px.Bar(
        x=city,
        y=freq,
        text=freq,
        textposition='outside',  # Position of data labels
        marker=dict(color='skyblue'),  # Customize bar color if needed
    ))
    # Update layout if needed
    fig.update_layout(
        xaxis_title='City',
        yaxis_title='Frequency',
    )
    # Display the plot
    st.plotly_chart(fig)

    col1, col2 = st.columns(2)
    with col2:
        # Most expensive Route :- 
        st.header("Most expensive Route")
        columns = ['Source', 'Destination', 'AveragePrice']
        result = db.Most_expensive_route()
        df = pd.DataFrame(result, columns=columns)
        st.dataframe(df)

    with col1:
        # Flights with Longest Duration
        st.header("Long Duration Flights")
        columns = ['Airline','Source', 'Destination', 'duration_min']
        result = db.Flights_with_Longest_Duration()
        df = pd.DataFrame(result, columns=columns)
        st.dataframe(df)


    # busy month
    st.header("Busy Month")
    # Fetch data
    month, count = db.busy_month()
    # Create the figure
    fig = px.Figure()
    # Add bar chart with data labels
    fig.add_trace(px.Bar(
        x=month,
        y=count,
        text=count,
        textposition='outside',  # Position of data labels
        marker=dict(color='pink'),  # Customize bar color if needed
    ))
    # Update layout if needed
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Count',
    )
    # Display the plot
    st.plotly_chart(fig)




    # Seasonal Price Trends
    st.header("Seasonal Price Trends")
    # Fetch data
    month, avg_price = db.seasonal_price_treands()
    # Create the figure
    fig = px.Figure()
    # Add line and markers with data labels
    fig.add_trace(px.Scatter(
        x=month,
        y=avg_price,
        mode='lines+markers+text',
        text=avg_price,
        textposition='top center',
        line=dict(color='blue'),  # Customize the line color if needed
        marker=dict(size=8, color='red')  # Customize marker size and color if needed
    ))
    # Update layout if needed
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Avg_Price',
        title='Seasonal Price Trends'
    )
    # Display the plot
    st.plotly_chart(fig)



    # costly_flight
    st.header("Costly Flight by Week")
    day, price = db.costly_flight()
    # Create the figure
    fig = px.Figure()
    # Add bar chart with data labels
    fig.add_trace(px.Bar(
        x=day,
        y=price,
        text=price,
        textposition='outside',  # Position of data labels
        marker=dict(color='pink'),  # Customize bar color if needed
    ))
    # Update layout if needed
    fig.update_layout(
        xaxis_title='City',
        yaxis_title='Frequency',
    )
    # Display the plot
    st.plotly_chart(fig)


    

    
else:
    st.title("Tell About your project")