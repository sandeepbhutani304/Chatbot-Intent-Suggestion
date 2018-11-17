#################################################################################################################
# Author :	Sandeep Bhutani
# Date	 : 	2 Nov 2018
# Purpose: Suggests frequently asked intents, based on current intent asked by chatbot user
# Usage	 : apriori_chat.py "CurrentIntentName"
#          apriori_chat.py --retrain : It will generate apri.pkl training model.
# How	: It uses apriori assiciation rule mining based on historical user name and user intents. On every run the pickle file is loaded in memory and results are returned
#################################################################################################################

t=["system slow,outlook not working,unexpected reboot".split(","), "system not compliant,system slow,IE not working".split(","), "outlook not working,system slow,IE not working".split(","),
   ['system slow', 'unexpected reboot']]

pickle_file = "data\\apri.pkl"  #to be changed

from apyori import apriori as ap
import pandas as pd
import pickle

ruleslist=None

def read_train_data():
    global t
    d=pd.ExcelFile("data\\mytech_data.xlsx")#,sheet_name="")  #to be changed
    # d.sheet_names
    du=d.parse('User_Queries')
    # du=d.parse('tbl_UserLog')
    # du.columns
    # du.head()
    # du.tail()
    # du['Utterance_User']
    du=du[['User_name', 'Predicted_Intent']]
    du=du.dropna(0)
    gb=du.groupby('User_name')
    gb['User_name'].unique()
    t=[]
    for name, group in gb:
       #print(name)
       #print(group.head())
       #print(group['Predicted_Intent'].tolist())
       t.append(group['Predicted_Intent'].unique().tolist())
    with open(pickle_file, 'wb') as f:
        pickle.dump(t, f)

def train_apriori(t):
    global ruleslist
    ruleslist=list(ap(t, max_length=2, min_support=0.1, min_lift=1.00000, min_confidence=0.4))
    
def get_next_intent_suggestion(findwhat, debug=False):
#    findwhat = "system slow"
    global ruleslist
    if debug==True:
        print("---> ruleslist")
        print(ruleslist)

    #, min_confidence=0.1, min_lift=0.2
    ordered_statistics = [x.ordered_statistics for x in ruleslist if (x.items.__len__() > 1 and x.items.__contains__(findwhat))]
    if debug==True:
        print("---> ordered_statistics")
        print(ordered_statistics)
    ordered_list = []
    next_list=[]
    for o in ordered_statistics:
        for o1 in o:
            if o1.items_base.__contains__(findwhat):
                ordered_list.append(o1)
                for _ in o1.items_add.__iter__(): next_list.append(_)
    if debug==True:
        print("---> ordered_list")
        print(ordered_list)
    return next_list

import sys
current_intent=""
if(len(sys.argv) < 2):
    print("Usage:\n apriori_chat.py <Current intent name>     e.g. apriori_chat.py \"Project SPOC\" \n apriori_chat.py --retrain to retrain")
    exit(1)
else:
    if(sys.argv[1] == "--retrain"):
        train_apriori(t)
        exit(0)
    else:
        with open(pickle_file, 'rb') as f:
            t = pickle.load(f)
        current_intent=sys.argv[1]


#print(current_intent)

#read_train_data()
#train_apriori(t)  #uncomment this line when you have actual data. For now hardcoded data in variable t is being used
#l=get_next_intent_suggestion("Project SPOC")
l=get_next_intent_suggestion(current_intent)
print(l)
