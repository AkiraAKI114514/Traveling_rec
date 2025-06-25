from Logic_engine import ForwardEngine
from DPReasoning import DPReasoning

def main():
    search = ForwardEngine()
    user_fact = {'budget':1200,'interest':'beach,china'}#all keys in low form

    if user_fact['interest'] == '':
        print("Please tell me what place you are interested.")
        return
    
    search.load_initial_facts(user_fact)
    des_list,weight_dic = search.infer(updating= False)

    print(weight_dic)
    dp = DPReasoning()
    dp_list = dp.dp_value_select(des_list,user_fact['budget'],user_fact['interest'].split(","),weight_dic)
    dp_list = list(dp_list)
    dp_list = dp_list[:5]
    print("The latest best traveling destinaitons session is:")
    for des in dp_list:
        print(f"\n{des['destination']}\nScore in Trip.com: {des['score']}\nPrice: {des['price']}")
        pass

if __name__ == "__main__":
    main()