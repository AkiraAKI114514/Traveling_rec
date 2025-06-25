from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sqlite3
import random

#pip install selenium

class findattri:
    def __init__(self):
        pass
    def start(self,idx0,city):
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 屏蔽 DevTools 日志

        driver = webdriver.Chrome(options=options)
        url0 = f"https://www.trip.com/things-to-do/list?pagetype=city&citytype=dt&id={idx0}&name=&locale=en-XX&curr=MYR"
        driver.get(url0)
        #print(driver.page_source)
        wait = WebDriverWait(driver,10)
        try:
            data0 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".m_productcard_container")))
        except:
            return []
        
        cards = driver.find_elements(By.CLASS_NAME,"m_productcard_container")

        json_list = []
        idx = 0
        for card in cards:
            title = card.find_element(By.CLASS_NAME,"m_productcard_header_container").text#name

            title_check = title.split()
            #check if the data valid
            for word in title_check:
                if word == "5G" or word == "4G" or word == "eSIM" or word == "+" or "+"in word or "(" in word:
                    notvalid = True
                    break
            else:
                notvalid = False
                pass
            if notvalid == True:
                continue

            try:
                price_str = card.find_element(By.CLASS_NAME,"u_price").text.split()
            except:
                price_str = ["free"]
            price_float = 0#price
            for word in price_str:
                try:
                    price_float = float(word)
                except ValueError:
                    pass

            tags = card.find_elements(By.CLASS_NAME,"u_tag.u_tag_bordered.u_tag_solid_gray.u_tag_primary")
            tag_list = [tag.text for tag in tags]#tags
            if len(tag_list) == 0:
                tag_list = self.randomtag()
            else:
                pass

            tag_list.append(city)

            try:
                score = card.find_element(By.CLASS_NAME,"u_score_content").text
            except:
                score = self.randomfloat()
            json0 = {}
            json0["Id"] = city+str(idx)
            json0["Destination"] = title
            json0["City"] = city
            json0["Score"] = score
            json0["Tags"] = tag_list
            json0["Price"] = price_float
            json_list.append(json0)
            idx+=1
        print(idx0+city+" done")
        driver.quit()
        return json_list
    
    def create_db(self):
        conn = sqlite3.connect('travel.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attractions (
                id TEXT PRIMARY KEY,
                destination TEXT,
                city TEXT,
                score TEXT,
                price REAL,
                tags TEXT
            )
        ''')

        conn.commit()
        conn.close()
    
    def save_to_db(self,json_list):
        conn = sqlite3.connect('travel.db')
        cursor = conn.cursor()

        for item in json_list:
            cursor.execute('''
                INSERT OR REPLACE INTO attractions (id, destination, city, score, price, tags)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                item["Id"],
                item["Destination"],
                item["City"],
                item["Score"],
                item["Price"],
                ",".join(item["Tags"])#tag to str
            ))

        conn.commit()
        conn.close()


    def find_file(self):
        self.create_db()

        file = open("data.txt","r",encoding="utf-8")
        file_a = open("attri.txt","a",encoding="utf-8")
        for line in file:
            line = line.split(":")
            json0 = self.start(line[0],line[1].replace("\n",""))
            #print(json0)
            if json0!=[]:
                self.save_to_db(json0)
            else:
                continue
        
        file_a.close()
        file.close()

        return
    
    def randomfloat(self):
        random0 = random.random()
        random0 *= 10
        random0 = int(random0)
        random0 /= 10
        float0 = 4.0+random0
        return float0
    
    def randomtag(self):
        random1 = ["No Shopping","Historic buildings","Local culture","Scenery"]
        list0 = random.choices(random1,k=2)
        return list0

if __name__ == "__main__":
    find0 = findattri()
    find0.find_file()


