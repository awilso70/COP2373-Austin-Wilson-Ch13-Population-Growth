import sqlite3
import matplotlib.pyplot as plt

def create_database():
    conn = sqlite3.connect('population_AW.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS population (
            city TEXT,
            year INTEGER,
            population INTEGER
        )
    ''')

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

    cursor.executemany('INSERT INTO population (city, year, population) VALUES (?, ?, ?)', cities_2023)
    conn.commit()
    conn.close()

def simulate_growth():
    conn = sqlite3.connect('population_AW.db')
    cursor = conn.cursor()

    cursor.execute('SELECT city, year, population FROM population WHERE year = 2023')
    base_data = cursor.fetchall()

    for city, year, population in base_data:
        current_population = population
        for i in range(1, 21):
            new_year = year + i
            current_population = int(current_population * 1.02)
            cursor.execute('INSERT INTO population (city, year, population) VALUES (?, ?, ?)',
                           (city, new_year, current_population))
    conn.commit()
    conn.close()
def show_growth():
    cities = [
        'Sarasota', 'Bradenton', 'St. Petersburg', 'Tampa', 'Riverview',
        'Gainesville', 'Venice', 'Panama City Beach', 'Miami', 'Orlando'
    ]

    print("Select a city to see growth:")
    for i, city in enumerate(cities, 1):
        print(f"{i}. {city}")

    selection = int(input("Type number of your chosen city: "))
    if not (1 <= selection <= len(cities)):
        print("Invalid choice.")
        return

    selected_city = cities[selection -1]

    conn = sqlite3.connect('population_AW.db')
    cursor = conn.cursor()

    cursor.execute('SELECT year, population FROM population WHERE city = ? ORDER BY year', (selected_city,))
    data = cursor.fetchall()

    years = [row[0] for row in data]
    populations = [row[1] for row in data]

    plt.figure(figsize=(10, 5))
    plt.plot(years, populations, marker = '*', linestyle='--', color = 'g')
    plt.title(f'Population growth for {selected_city} (2023 -2043)')
    plt.xlabel('Year')
    plt.ylabel('Population')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    conn.close()

if __name__ == '__main__':
    create_database()
    simulate_growth()
    show_growth()