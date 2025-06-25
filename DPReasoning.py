class DPReasoning():
    def __init__(self):
        pass
    
    #des_list:[{
    #           id:TEXT
    #           destination:TEXT,
    #           city:TEXT,
    #           score:FLOAT,
    #           price:FLOAT,
    #           tags:[]},{},...]

    def valuing(self, des_dic, interest_list,weight_dic):
        total_score = 0
        weight = weight_dic[f"{des_dic['city']}"]
        for tag in des_dic["tags"]:
            if tag in interest_list:
                total_score += 1
        
        return (des_dic["score"]+total_score*0.4)*weight
        
    def dp_value_select(self, des_list, budget, interest_list,weight_dic):
        #dp list initialize
        current_best = [[0] * (budget + 1) for _ in range(len(des_list) + 1)]
        res = []
        values_list = [round(self.valuing(des,interest_list,weight_dic),2) for des in des_list]
        costs_list = [des["price"] for des in des_list]

        
        for i in range(1,len(des_list)+1):
            for b in range(budget+1):
                if costs_list[i-1] <= b: # if the cost is under b for a part of the budget
                    current_best[i][b] = round(max([current_best[i-1][b], values_list[i-1]+current_best[i-1][b-costs_list[i-1]]]),2)
                else:
                    current_best[i][b] = round(current_best[i-1][b],2)

        budget0 = budget
        for j in range(len(des_list),0,-1):
            if current_best[j][budget0]!=current_best[j-1][budget0]:
                res.append(des_list[j-1])

                budget0 -= costs_list[j-1]
        
        return reversed(res)

    def dp_route_select(self,res_list):
        #find departure point
        center_dis = 0
        start = 0
        for i in range(len(res_list)):
            dis = (res_list[i]["long_lat"][0]-res_list[i]["city"][0])**2 + (res_list[i]["long_lat"][1]-res_list[i]["city"][1])**2
            if i == 0:
                center_dis = dis
            else:
                if dis < center_dis:
                    center_dis = dis
                    start = i
        
        #find the shortest route

        route_list = []
        route_list.append(res_list[start])
        res_list.pop(start)

        for k in range(len(res_list)):
            dis_list = []
            for j in range(len(res_list)):
                dis0 = (res_list[j]["long_lat"][0]-route_list[-1]["long_lat"][0])**2 + (res_list[j]["long_lat"][1]-route_list[-1]["long_lat"][1])**2
                dis_list.append(dis0)
            idx = dis_list.index(min(dis0))
            route_list.append(res_list[idx])
            res_list.pop(idx)
    
        return dis_list
