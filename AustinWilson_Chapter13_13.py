import sqlite3 # imports sqlite for databases
import matplotlib.pyplot as plt # imports matplotlib for graph visualizations

#Function for creating tables and their values
def create_database():
    conn = sqlite3.connect('population_AW.db')  #connects the database
    cursor = conn.cursor() # allows for fetching of info
#creates table and city(name)/year/population values
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS population ( 
            city TEXT,
            year INTEGER,
            population INTEGER
        )
    ''')
# populations chosen from "Florida Demographics" in 2023
    cities_2023 = [
        ('Sarasota', 2023, 57602),
        ('Bradenton', 2023, 57076),
        ('St. Petersburg', 2023, 263553),
        ('Tampa', 2023, 403364),
        ('Riverview', 2023, 107776),
        ('Gainesville', 2023, 145812),
        ('Venice', 2023, 28150),
        ('Panama City Beach', 2023, 19393),
        ('Miami', 2023, 455924),
        ('Orlando', 2023, 320742)
    ]
    # inserts 2023 data into population table
    cursor.executemany('INSERT INTO population (city, year, population) VALUES (?, ?, ?)', cities_2023)
    conn.commit() #save and close
    conn.close()

# function to visualize 2% growth for 20 years
def simulate_growth():
    conn = sqlite3.connect('population_AW.db')
    cursor = conn.cursor()
#fetch 2023 city data
    cursor.execute('SELECT city, year, population FROM population WHERE year = 2023')
    base_data = cursor.fetchall()
# loops through base data
    for city, year, population in base_data:
        current_population = population #starts at 2023
        for i in range(1, 21): # simulates 20 years
            new_year = year + i # increases year
            current_population = int(current_population * 1.02) # applies 2% growth
            cursor.execute('INSERT INTO population (city, year, population) VALUES (?, ?, ?)', # inserts new data
                           (city, new_year, current_population))
    conn.commit()
    conn.close()
# function for plotting and displaying selected city
def show_growth():
    # list 10 cities for user
    cities = [
        'Sarasota', 'Bradenton', 'St. Petersburg', 'Tampa', 'Riverview',
        'Gainesville', 'Venice', 'Panama City Beach', 'Miami', 'Orlando'
    ]
    # display to user cities numbered
    print("Select a city to see growth:")
    for i, city in enumerate(cities, 1):
        print(f"{i}. {city}")
    # user input and error handling
    selection = int(input("Type number of your chosen city: "))
    if not (1 <= selection <= len(cities)):
        print("Invalid choice.")
        return
    # variable for selected city
    selected_city = cities[selection -1]

    conn = sqlite3.connect('population_AW.db')
    cursor = conn.cursor()
    # fetches population data for selected city
    cursor.execute('SELECT year, population FROM population WHERE city = ? ORDER BY year', (selected_city,))
    data = cursor.fetchall()
    #seperate year and population into rows
    years = [row[0] for row in data]
    populations = [row[1] for row in data]

    plt.figure(figsize=(10, 5)) #figure size
    plt.plot(years, populations, marker = '*', linestyle='--', color = 'g') # star marker, dashed lines, green color
    plt.title(f'Population growth for {selected_city} (2023 -2043)') # titles table
    plt.xlabel('Year') # x = year
    plt.ylabel('Population') # y = population
    plt.grid(True) # gridlines
    plt.tight_layout() # fit onto screen
    plt.show() # displays

    conn.close()

if __name__ == '__main__':
    create_database()
    simulate_growth()
    show_growth()