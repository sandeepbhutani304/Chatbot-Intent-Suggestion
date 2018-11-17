# Chatbot-Intent-Suggestion
In chatbots it is good to suggest user, what other users asked, when current user asks a question. This can help creating curiosity on user and can increase chatbot adoption.

It uses apriori assiciation rule mining based on historical user name and user intents. On every run the pickle file is loaded in memory and results are returned

The code is based on apriory module. You need to install the module by running command : pip install apyori 

The code reads excel file (in method read_train_data ) containing data in two columns User_name, Predicted_Intent. For demo, this function is not called and existing variable t is used.

The code generates association rules and prints top suggestions. 
Example, if user asks question my system is slow, then code finds out which user has asked this question and what other questions were asked by that user. Based on this association rule, the code suggests to current user that other similar users asked about vpn issues too.
