import mysql.connector

class DB :
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "Momdad@1018",
                port = 3003, 
                database = "flights"
            )
            # this cursor object is used to write the queries and all
            self.mycursor = self.conn.cursor()
            
            print("connection succesfull")
        except:
            print("connection error")
    def fetch_city_names(self):
        city = []
        self.mycursor.execute("""
        select distinct(Destination) from flights
        union 
        select distinct(Source) from flights
        
        """)
        
        data = self.mycursor.fetchall()

        for i in data:
            city.append(i[0])
        return city
    
    def fetch_all_flights(self , source , destination):
        self.mycursor.execute("""
        select Airline, Route , Dep_Time , Duration , Price from flights_data
        where Source = "{}" and Destination = "{}"
        """.format(source , destination))
        data = self.mycursor.fetchall()

        return data

    def fetch_ariline_freq(self):
        airline = []
        freq = []
        self.mycursor.execute("""
        select Airline , Count(*) as "Count" from flights 
        group by Airline""")
        data = self.mycursor.fetchall()
        for item in data :
            airline.append(item[0])
            freq.append(item[1])
        return  airline , freq
    

    def busy_airpot(self):
        city = []
        freq = []
        self.mycursor.execute("""
        select Source , count(*) as "count" from (select Source from flights
        union all
        select Destination from flights) t

        group by Source
        order by count desc""")

        data = self.mycursor.fetchall()
        for item in data :
            city.append(item[0])
            freq.append(item[1])
        return  city , freq

    
    def busy_month(self):
        month = []
        count =[]
        self.mycursor.execute("""
        select monthname(date_of_journey) , count(*) from flights
        group by monthname(date_of_journey)
        order by count(*) desc 
                              """)
        
        data  = self.mycursor.fetchall()
        for i in data:
            month.append(i[0])
            count.append(i[1])
        return month ,count
    
    def costly_flight(self):
        day = []
        price = []

        self.mycursor.execute("""
        select dayname(date_of_journey) , avg(Price) from flights
        group by dayname(date_of_journey)
        order by avg(Price) Desc """)

        data = self.mycursor.fetchall()

        for i in data :
            day.append(i[0])
            price.append(i[1])
        return day , price
    
    def avg_price_per_airline(self):
        airline = []
        avg_price = []
        self.mycursor.execute("""
                                SELECT Airline, AVG(Price)
                                FROM flights
                                GROUP BY Airline
                                ORDER BY AVG(Price) DESC """)
        data = self.mycursor.fetchall()
        for i in data :
            airline.append(i[0])
            avg_price.append(i[1])
        return airline ,avg_price
    
    def stops_by_route(self , source , destination):
        stops_count = []
        self.mycursor.execute("""
                                SELECT SUM(Total_Stops) AS TotalStops
                                FROM flights
                              where Source = "{}" and Destination = "{}"
                                GROUP BY "Source", "Destination"
                                ORDER BY TotalStops DESC """.format(source , destination))
        data = self.mycursor.fetchone()
    
        if data:
            total_stops = data[0]
        else:
            total_stops = 0  # or handle it as you prefer
        
        return total_stops
    
    def Most_expensive_route(self):
        self.mycursor.execute("""
                            SELECT Source, Destination, AVG(Price) AS AveragePrice
                            FROM flights
                            GROUP BY Source, Destination
                            ORDER BY AveragePrice DESC
                            LIMIT 10 """)
        
        data = self.mycursor.fetchall()

        return data 
    
    def Flights_with_Longest_Duration(self):
        self.mycursor.execute("""
                                SELECT Airline, Source, Destination, duration_min
                                FROM flights
                                ORDER BY duration_min DESC
                                LIMIT 5 """)
        
        data = self.mycursor.fetchall()

        return data
    
    def seasonal_price_treands(self):
        month = []
        avg_price = []

        self.mycursor.execute("""
                                SELECT MONTH(Date_of_Journey) AS Month, AVG(Price) AS AveragePrice
                                FROM flights
                                GROUP BY Month
                                ORDER BY Month """)
        
        data = self.mycursor.fetchall()
        for i in data:
            month.append(i[0])
            avg_price.append(i[1])

        return month  , avg_price
    

    def trend_analysis_by_airline(self):
        legends = []
        year = []
        month =[]
        avg_price =[]
        self.mycursor.execute("""
SELECT Airline, YEAR(Date_of_Journey) AS Year, MONTH(Date_of_Journey) AS Month, AVG(Price) AS AveragePrice
FROM flights
GROUP BY Airline, Year, Month
ORDER BY Airline, Year, Month """)
        
        data = self.mycursor.fetchall()
        for i in data:
            legends.append(i[0])
            year.append(i[1])
            month.append(i[2])
            avg_price.append(i[3])
        return legends , year , month , avg_price
