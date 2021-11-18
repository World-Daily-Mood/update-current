import json
import mysql.connector
from numpy.core.defchararray import array

configfile = "./config.json"

connection = None
cursor = None

def main(event = None, context = None):
    def connect():
        with open(configfile, "r") as f:
            config = json.load(f)

            host = config["host"]
            user = config["user"]
            password = config["password"]
            database = config["database"]
        
        global connection
        global cursor
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = connection.cursor()

    def get_all_moods():
        query = "SELECT mood FROM today"
        cursor.execute(query)
        moods = cursor.fetchall()

        moods_arr = []
        for mood in moods:
            moods_arr.append(mood[0])
        
        return moods_arr

    def get_best_mood(all_moods: array):
        return max(all_moods)

    def set_current(mood: str):
        query = "DELETE FROM current"
        cursor.execute(query)

        query = "INSERT INTO current (mood) VALUES (%s)"
        cursor.execute(query, (mood,))

        connection.commit()
        connection.close()

    connect()
    all_moods = get_all_moods()
    best_mood = get_best_mood(all_moods)
    set_current(best_mood)