import os
import mysql.connector
import json

db = open('./app/modules/emotions.json', 'r')
wavedb = json.load(db)
db_password = open('/run/secrets/db_root_password', 'r').read().strip()

def get(queries):
    # Create a cursor object to execute queries
    # Connect to the database
    with mysql.connector.connect(
        host="172.23.0.2",
        user=os.getenv("USER"),
        password=db_password,
        database=os.getenv("DATABASE")
    ) as mydb:
        mycursor = mydb.cursor()
        # Perform database operations
        # The connection is automatically closed when leaving the "with" block
        # Execute a query
        mycursor.execute(queries)
        # Fetch the results
        results = mycursor.fetchall()
    return results

def about_emotions():
    titles = get("SELECT column_name\
                FROM information_schema.columns\
                WHERE table_name = 'AboutEmotions';\
                ")
    emotions = get("SELECT * FROM AboutEmotions;")
    about_emotion = {}
    for i in range(0, len(emotions[0])):
        about_emotion[titles[i][0]] = emotions[0][i]

    return about_emotion
    # return wavedb['about_emotions_data']

def emotion_cards():
    cards_dict = {}
    cards_titles = ["ID", "Category", "Name", "Description", "Example"]

    cards = get(
            "SELECT cardID, ecg.categoryName, cardName, description, example\
            FROM EmotionCards AS ec\
                JOIN EmotionCategories ecg\
	            ON ec.categoryID = ecg.categoryID;")

    for i in range(0, len(cards)):
        cards_dict[cards[i][0]] = {cards_titles[0]:cards[i][0],
                                   cards_titles[1]:cards[i][1],
                                   cards_titles[2]:cards[i][2],
                                   cards_titles[3]:cards[i][3],
                                   cards_titles[4]:cards[i][4],}

    return cards_dict
    # return wavedb['emotion_cards']
    
