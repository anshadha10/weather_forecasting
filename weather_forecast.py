import requests
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# database connection
def create_database():
    conn=sqlite3.connect('weather_data.db') # Create a new database folder
    cursor=conn.cursor()
    cursor.execute('''
              CREATE TABLE IF NOT EXISTS weather(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      city TEXT,
                      temperature REAL,
                      description TEXT,
                      date TEXT
               )
           ''')
    conn.commit()
    conn.close()
    

# fetching weather data
def fetch_weather_data(city,api_key):
    url=f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response=requests.get(url)
    return response.json()

# store the retrieved weather data  
def store_weather_data(city,temperature,description):
    conn= sqlite3.connect('weather_data.db')
    cursor=conn.cursor()
    cursor.execute('''
         INSERT INTO weather(city,temperature,description,date)
         VALUES(?,?,?,CURRENT_TIMESTAMP)
        ''',(city,temperature,description))
    conn.commit()
    conn.close()
#data visualization
def visualize_weather_data():
    conn = sqlite3.connect('weather_data.db')
    df = pd.read_sql_query("SELECT * FROM weather", conn)
    conn.close()

    df['date'] = pd.to_datetime(df['date'])
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['temperature'], marker='o')
    plt.title('Weather Temperature Over Time')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
# main function
def main():
    create_database() #calling first fun and creating database and table
    api_key='6bba7dbef14f4f9ea066aab343632cf8' #aspi key is set
    city=input('Enter the name of the city:')
    data=fetch_weather_data(city,api_key) #calling ssecond function and fetching details and storing in data variable
    if data['cod']== 200: #check if the req was successful
        temperature= data['main']['temp']
        description= data['weather'][0]['description']
        store_weather_data(city,temperature,description)# store the data of the city weather in db
        print(f'Temperature in {city}:{temperature}°C,{description}')
        visualize_weather_data()

    else:
        print('City not found!')
   

if __name__=='__main__':
         main()        
         
     
