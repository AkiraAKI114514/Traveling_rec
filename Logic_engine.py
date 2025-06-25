import sqlite3
from typing import Dict, List, Set
from Sql_updating import Sql_updating
import os


class ForwardEngine:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path= os.path.join(current_dir, 'travel.db')
        self.facts = set()
        self.rule_fired = set() 
        self.rec_city = {}
        self.best_dic = {}
        self.user_prefs = {"budget":500,"interest":"trip"}

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM best_dic")
        rows = cursor.fetchall()
        for row in rows:
            name = row[0].split()
            name = "_".join(name) 
            self.best_dic[name] = row[1]
        
    #facts:category=value
    #rules:{id,name,condition,action,weight,description}

    def add_fact(self, fact: str):
        self.facts.add(fact)

    def load_initial_facts(self, user_prefs: Dict):
        #interest in facts
        for key, value in user_prefs.items():
            if type(value) == str:
                if "," in value:
                    value_list = value.split(",")
                    self.user_prefs[key] = value_list
                    for valu0 in value_list:
                        self.add_fact(f"{key}={valu0}")
                else:
                    self.user_prefs[key] = value
                    self.add_fact(f"{key}={value}")
            else:
                self.user_prefs[key] = value
                self.add_fact(f"{key}={value}")
        
        #tags in facts
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, tags FROM attractions")
            for aid, tags in cursor.fetchall():
                for tag in tags.split(','):
                    self.add_fact(f"attraction_tag={tag.strip().lower()},{aid}")

    def get_rules(self,conn) -> List[Dict]:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rules ORDER BY weight DESC")
        return [dict(row) for row in cursor.fetchall()]

    def infer(self, max_iterations=100,updating = False) -> Set[str]:
        newrules = False
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for _ in range(max_iterations):
            changed = False
            rules = self.get_rules(conn)
            
            for rule in rules:
                if rule['id'] not in self.rule_fired and self._eval_condition(rule['condition']):
                    self._execute_action(rule['action'],rule['weight'])
                    self.rule_fired.add(rule['id'])
                    changed = True
                    print(f"Condition '{rule['condition']}' approved")
            if not changed:
                break  #stop when no new facts appended
        if self.rec_city == []:
            newrules = True
        #find in facts table tags that match user interests
        for facts in self.facts:
            if facts.startswith("attraction_tag="):
                facts_split = facts.split(",")
                facts_id = facts_split[1]
                facts_str = facts_split[0][15:]

                if facts_str in self.user_prefs["interest"] and facts_str!="":
                    try:
                        cursor.execute(f"SELECT city FROM attractions WHERE id='{facts_id}'")
                    except:
                        pass

                    rows = cursor.fetchall()
                    for row in rows:
                        city0 = row[0]

                        if len(facts_str) == 1:
                            weight = 0.5
                        elif len(facts_str) == 2:
                            weight = 1
                        else:
                            weight = 5
                        if city0 not in self.rec_city:
                            self.rec_city[city0] = weight
                        else:
                            self.rec_city[city0] += weight*(1/(self.rec_city[city0]+1))
                            self.rec_city[city0] = round(self.rec_city[city0],2)
                    
                    
        
        #Sort the list and slice top5 cities                
        
        sorted_dict = dict(sorted(self.rec_city.items(), key=lambda item: item[1],reverse=True))
        items = list(sorted_dict.items())
        items_slice = items[:5]
        city_dic = dict(items_slice)
        weight_list = city_dic.values()
        #return destination list
        final_list = []
        if updating == True:
            self.get_latest_list(list(city_dic.keys()),conn)
        else:
            pass
        #print(self.rec_city)
        for city in city_dic.keys():
            rows = cursor.execute(f"SELECT * FROM attractions WHERE city='{city}'")
            for row in rows:
                des = {
                    "id":row[0],
                    "destination":row[1],
                    "city":row[2],
                    "score":float(row[3]),
                    "price":int(row[4]),
                    "tags":row[5].split(",")[:7]
                }
                final_list.append(des)

                

        return final_list,city_dic

    def _eval_condition(self, condition: str) -> bool:
        try:
            return eval(condition)
        except:
            return False

    def _execute_action(self, action: str, score: int):
        #do action in 'action'
        best_dic = self.best_dic
        if action.startswith("recommend>>"):
            attraction_id = action[11:]
            city0 = eval(attraction_id)
            if type(city0) == list:
                for city in city0:
                    self.add_fact(f"city>>{city}")
                return
            else:
                if city0 not in self.rec_city:
                    self.rec_city[city0] = score
                else:
                    self.rec_city[city0] += score
                self.add_fact(f"city>>{attraction_id}")
        elif action.startswith(f"city>>"):
            city1 = action[6:]

            if city1 not in self.rec_city:
                self.rec_city[city1] = score
            else:
                self.rec_city[city1] += score
            self.add_fact(f"city>>{city1}")

    def ranking(self,cities,score):
        #get best city in list
        for city0 in cities:
            if city0 == "":
                return
            if city0 not in self.rec_city:
                self.rec_city[city0] = score
            else:
                self.rec_city[city0] += score

        return cities
    
    def get_latest_list(self, city_list,conn):
        print("Cities updating")
        length = len(city_list)
        curr = 0
        outline = "="*curr*5+"-"*(length-curr)*5
        print(f"{outline}",end='', flush=True)
        for city in city_list:
            update = Sql_updating(city)
            update.update(conn)
            curr+=1
            outline = "="*curr*5+"-"*(length-curr)*5
            if curr == 1:
                print(f"\033[F\033[K\033[F\033[K{outline}", end='', flush=True)
            else:
                print(f"\033[F\033[K\033[F\033[K{outline}", end='', flush=True)
        print("\nUpdate finished")


# 使用示例
if __name__ == "__main__":
    engine = ForwardEngine()
    engine.load_initial_facts({'budget':1200,'interest':'japan'})
    result = engine.infer()
    