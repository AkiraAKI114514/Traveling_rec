from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sqlite3
import random
import findattri

class Sql_updating():
    #updating the scores of the attributions of the city
    def __init__(self,city):
        self.city = city
        self.db = "travel.db"
        file = open("data.txt","r",encoding="utf-8")

        for line in file:
            num_key = line.split(":")
            num = num_key[0]
            key = num_key[1]

            if key == self.city:
                self.idx = num
                break
            else:
                continue
        pass

        
    def update(self):
        return


    def set_list(self,tagname):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        score_dic = {}
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS best_dic (
                name TEXT,
                best_city TEXT
            )
        ''')

        

        cursor.execute(f"SELECT city,score FROM attractions WHERE tags LIKE '%{tagname}%'")

        city_list = cursor.fetchall()

        for city in city_list:
            if city[0] not in score_dic:

                score_dic[city[0]] = int(float(city[1])*10)/10
            else:
                score_dic[city[0]] += int(float(city[1])*10)/10
                score_dic[city[0]] = round(score_dic[city[0]]/2,2)
        
        maxvalue = 0
        best_city = ""
        for item in score_dic:
            if score_dic[item] > maxvalue:
                maxvalue = score_dic[item]
                best_city = item
        print(tagname,best_city)
        cursor.execute("""
            INSERT OR REPLACE INTO best_dic (name, best_city)
           VALUES (?, ?)
        """,(tagname,best_city)
        )

        conn.commit()
        conn.close()
    def addonid(self,json0):
        
        return


if __name__ == "__main__":
    update = Sql_updating("Beijing")
    update.set_list()