import streamlit as st
from dbhelper import DB
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


st.set_page_config(layout="wide")
db = DB()

st.sidebar.title('Flights Analysis')

user_option = st.sidebar.selectbox('Menu',['Select one','Check Flights','Analytics'])

if user_option == 'Check Flights':
    st.title('Check Flights')

    col1,col2 = st.columns(2)
    city = db.fetch_city_names()

    with col1:
        source = st.selectbox('Source',sorted(city))

    with col2:
        destination = st.selectbox('Destination', sorted(city))

    if st.button('Search'):
        if source == destination:
            st.warning("Source and destination can't be the same.")
        else:
            results = db.fetch_all_flights(source, destination)
            if results:
                df = pd.DataFrame(results, columns=["Airline", "Route", "Departure Time", "Duration (min)", "Price"])
                st.dataframe(df, use_container_width=True)
            else:
                st.warning(f"No flights found from {source} to {destination}. Try a different route.")

elif user_option == 'Analytics':

    st.title('Analytics')

    # Row 1: Summary metrics (full width, not in columns)
    total, avg_price_val, min_price, max_price = db.summary_stats()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Flights", total)
    col2.metric("Avg Price", f"₹{avg_price_val:,.0f}")
    col3.metric("Min Price", f"₹{min_price:,.0f}")
    col4.metric("Max Price", f"₹{max_price:,.0f}")

    # Row 2: Pie chart + Busy airports
    col1, col2 = st.columns(2)
    with col1:
        airline, frequency = db.fetch_airline_frequency()
        fig = go.Figure(go.Pie(labels=airline, values=frequency, hoverinfo="label+percent", textinfo='value'))
        st.header('Airline Frequency')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        city, frequency = db.busy_airport()
        fig = px.bar(x=city, y=frequency, labels={'x': 'City', 'y': 'Number of Flights'})
        st.header('Busiest Airports')
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    # Row 3: Daily frequency + Avg price by airline
    col1, col2 = st.columns(2)
    with col1:
        date, frequency = db.daily_frequency()
        fig = px.line(x=date, y=frequency, labels={'x': 'Date', 'y': 'Number of Flights'})
        st.header('Daily Flight Frequency')
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    with col2:
        airline, avg_price = db.avg_price_by_airline()
        fig = px.bar(x=airline, y=avg_price, labels={'x': 'Airline', 'y': 'Average Price'})
        st.header('Average Price by Airline')
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    # Row 4: Stops distribution + Duration by stops
    col1, col2 = st.columns(2)
    with col1:
        stops, frequency = db.duration_by_stops()
        fig = px.pie(names=stops, values=frequency)
        st.header('Flights by Number of Stops')
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    with col2:
        stops, avg_duration = db.duration_by_stops()
        fig = px.bar(x=stops, y=avg_duration, labels={'x': 'Stops', 'y': 'Average Duration (min)'})
        st.header('Average Duration by Stops')
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    # Row 5: Top expensive routes (full width — horizontal bar with 10 labels needs space)
    route, price = db.top_expensive_routes()
    fig = px.bar(x=price, y=route, orientation='h', labels={'x': 'Price', 'y': 'Route'})
    st.header('Top 10 Most Expensive Routes')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

else:
    st.title('Flights Analysis')
    st.write("A look at Indian domestic flight data — 10,000+ flights, all routes, all airlines.")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Check Flights")
        st.write("Pick a source and destination, see what's available — airline, timing, duration, price.")
        st.caption("Heads up: not every city pair has a direct flight in the data.")

    with col2:
        st.subheader("Analytics")
        st.write("Busiest airports, which airlines dominate, how price and duration play out across the dataset.")

    st.divider()
    st.write("Pick something from the sidebar to get started.")