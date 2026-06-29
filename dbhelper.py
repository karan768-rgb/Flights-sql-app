import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

print("DEBUG:", os.getenv("DB_HOST"), os.getenv("DB_USER"), os.getenv("DB_NAME"))



class DB:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
                use_pure=True
            )
            self.mycursor = self.conn.cursor()
            print("connection established")
        except Exception as e:
            print("connection error:", e)

    def fetch_city_names(self):
        city = []
        self.mycursor.execute("""
        SELECT DISTINCT(Destination) FROM flights.flights
        UNION
        SELECT DISTINCT(Source) FROM flights.flights
        """)

        data = self.mycursor.fetchall()

        for i in data:
            city.append(i[0])

        return city

    def fetch_all_flights(self,source,destination):
        self.mycursor.execute("""
        SELECT Airline,Route,Dep_Time,Duration,Price FROM flights.flights
        WHERE Source = '{}' AND Destination = '{}'
        """.format(source,destination))

        data = self.mycursor.fetchall()
        return data

    def fetch_airline_frequency(self):

        airline = []
        frequency = []
        self.mycursor.execute("""
        SELECT Airline,COUNT(*) FROM flights.flights
        GROUP BY Airline
        """)

        data = self.mycursor.fetchall()

        for i in data:
            airline.append(i[0])
            frequency.append(i[1])

        return airline, frequency


    def busy_airport(self):

        city = []
        frequency = []

        self.mycursor.execute("""
        SELECT Source,COUNT(*) FROM ( SELECT Source FROM flights.flights
							UNION ALL
							SELECT Destination FROM flights.flights) t
        GROUP BY t.Source
        ORDER BY COUNT(*) DESC 
        """)

        data = self.mycursor.fetchall()
        for i in data:
            city.append(i[0])
            frequency.append(i[1])

        return city, frequency

    def daily_frequency(self):

        date = []
        frequency = []

        self.mycursor.execute("""
        SELECT Date_of_Journey,COUNT(*) FROM flights.flights
        GROUP BY Date_of_Journey
                              """)

        data = self.mycursor.fetchall()
        for i in data:
            date.append(i[0])
            frequency.append(i[1])

        return date, frequency

    def avg_price_by_airline(self):
        airline = []
        avg_price = []
        self.mycursor.execute("""
                              SELECT Airline, AVG(Price)
                              FROM flights.flights
                              GROUP BY Airline
                              ORDER BY AVG(Price) DESC
                              """)
        data = self.mycursor.fetchall()
        for i in data:
            airline.append(i[0])
            avg_price.append(round(i[1], 2))
        return airline, avg_price

    def top_expensive_routes(self):
        route = []
        price = []
        self.mycursor.execute("""
                              SELECT Route, MAX(Price)
                              FROM flights.flights
                              GROUP BY Route
                              ORDER BY MAX(Price) DESC LIMIT 10
                              """)
        data = self.mycursor.fetchall()
        for i in data:
            route.append(i[0])
            price.append(i[1])
        return route, price

    def summary_stats(self):
        self.mycursor.execute("""
                              SELECT COUNT(*), AVG(Price), MIN(Price), MAX(Price)
                              FROM flights.flights
                              """)
        data = self.mycursor.fetchone()
        return data

    def duration_by_stops(self):
        stops = []
        avg_duration = []
        self.mycursor.execute("""
                              SELECT Total_Stops, AVG(Duration)
                              FROM flights.flights
                              GROUP BY Total_Stops
                              """)
        data = self.mycursor.fetchall()
        for i in data:
            stops.append(i[0])
            avg_duration.append(round(i[1], 1))
        return stops, avg_duration