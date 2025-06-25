import sqlite3

class Rules():

    def __init__(self):
        self.path = "travel.db"

    def create_rule_table(self):
        conn = sqlite3.connect('travel.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rules (
                id TEXT PRIMARY KEY,
                name TEXT,
                condition TEXT,
                action TEXT,
                weight REAL,
                category TEXT,
                description TEXT
            )
        ''')

        conn.commit()
        conn.close()
    
    def insert_rules(self):
        conn = sqlite3.connect('travel.db')
        cursor = conn.cursor()
        #interesttag

        rules = [
            (1,"night_view","'interest=night' in self.facts or 'interest=night view' in self.facts","recommend>>best_dic['night_view']",1.8,"tag","These attractions are recommended for customers who are interested in night views"),        
            (2,"historic_buildings","'interest=history' in self.facts or 'interest=historic buildings' in self.facts or 'interest=buildings' in self.facts","recommend>>best_dic['historic_buildings']",1.8,"tag","These attractions are recommended for customers who are interested in historic buildings."),
            (3,"scenery","'interest=scenery' in self.facts or 'interest=nature' in self.facts or 'interest=view' in self.facts","recommend>>best_dic['scenery']",1.8,"tag","These attractions are recommended for customers who are interested in sceneries."),
            (4,"culture_museum","'interest=culture' in self.facts or 'interest=local' in self.facts or 'interest=museum' in self.facts","recommend>>best_dic['culture_museum']",1.8,"tag","These attractions are recommended for customers who are interested in local culture."),
            (5,"sea","'interest=sea' in self.facts or 'interest=ocean' in self.facts","recommend>>best_dic['sea']", 1.9, "name", "These destinations are for customers who like sea views and sea animals."),
            (6,"amusement_park","'interest=park' in self.facts or 'interest=amusement' in self.facts or 'interest=fun' in self.facts","recommend>>best_dic['amusement_park']",1.8,"tag","These attractions are recommended for customers who are interested in amusement parks."),
            (7,"cabel_montain","'interest=montain' in self.facts or 'interest=montains' in self.facts or 'interest=cabel' in self.facts","recommend>>best_dic['cabel_montain']",1.8,"tag","These attractions are recommended for customers who are interested in montains."),
            (8,"china_rec","'interest=china' in self.facts","recommend>>self.ranking(['Beijing','Shanghai','Shenzhen','Guangzhou','Suzhou','Nanjing'])",2.0,"contury","These are famous attractions from China."),
            (9,"japan_rec","'interest=japan' in self.facts","recommend>>self.ranking(['Tokyo','Osaka','Kyoto'])",2.0,"contury","These are famous destinations from Japan."),
            (10,"malaysia_rec","'interest=malaysia' in self.facts","recommend>>self.ranking(['Kuala Lumpur','Maleka','Penang'])",2.0,"contury","These are famous destinations from Malaysia"),
            (11,"us_rec","'interest=us' in self.facts or 'interest=usa' in self.facts or 'interest=united states' in self.facts","recommend>>self.ranking(['New York','San Frencisco','Los Angeles','Las Vegas'])",2.0,"contury","These are famous attractions from the US"),
            (12,"brit_rec","'interest=uk' in self.facts or 'interest=britain' in self.facts","recommend>>self.ranking(['London','Manchester'])", 2.0,"contury","These are famous attractions from the UK."),
        ]

        file = open("data.txt","r",encoding="utf-8")

        for line in file:
            line_list = line.split(":")
            city0 = line_list[1]
            rules.append((rules[-1][0]+1,f"{city0.strip()}",f"'interest={city0.lower().strip()}' in self.facts",f"city>>{city0.strip()}",10,"city",f"These are attractions from {city0.strip()}"))

        cursor.executemany("""
            INSERT OR REPLACE INTO rules (id, name, condition, action, weight, category, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,rules
        )

        conn.commit()
        conn.close()
        print("Rules set successfully")

    def start(self):

        self.create_rule_table()
        self.insert_rules()




if __name__ == "__main__":
    rule = Rules()
    rule.start()
