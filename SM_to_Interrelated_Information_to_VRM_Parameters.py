


import tweepy
import re
import os, logging, datetime, argparse
from logging.handlers import RotatingFileHandler
import json
from prepare_data_for_labeling_infer import prepare_data_for_subject_object_labeling_infer
from produce_submit_json_file import Sorted_relation_and_entity_list_Management
from DataInteroperability import SPO2KG_Function
import sys
import subprocess
from py2neo import Graph, Node, Relationship,NodeMatcher

CONSUMER_KEY = "1LBqUbcbBOAD6LKsq2f49yHVM"

CONSUMER_SECRET = "TFUQKKBXSKxOJcPCm0XlT2UbrcBaTv2M30oTQTD7dK1ZSW81qN"

OAUTH_TOKEN = "944909346760146946-S0zPwmjF4n5CZQouYUwFFxPsKixfjYT"

OAUTH_TOKEN_SECRET = "nS8k5I4xok4UmhbFynfSysfMK5Hn1dBYe4V4VmPhbdO4Z"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

api = tweepy.API(auth)

graph = Graph('http://localhost:7474', username='neo4j', password='ab014415')

def claddify_traffic_and_non_traffic_tweet(Id):
    data_dir=r"--data_dir=D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master-tweetclassification\bin/predicate_classifiction/classification_data/"+Id
    output_dir=r" --output_dir=D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master-tweetclassification/output/predicate_classification_model/epochs1700/"+Id+r"/"
    os.makedirs("D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master-tweetclassification/output/predicate_classification_model/epochs1700/"+Id+r"/")
    classification_command=r"C:\Users\CivilIM\Anaconda3\envs\TF115P37\python.exe D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master-tweetclassification\run_predicate_classification.py "+data_dir+output_dir
    print (data_dir)
    os.system(classification_command)
def check_classification_result(Id):
    f = open(r"D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master-tweetclassification/output/predicate_classification_model/epochs1700/"+Id+r"/predicate_predict.txt")
    classification_result=f.read()
    classification_result=classification_result.replace("\n", "")
    print(classification_result)
    if classification_result=="traffic":
        return True
    else:
        return False
def predict_relations(Id):
    data_dir = r"--data_dir=D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master-tweetclassification\bin/predicate_classifiction/classification_data/" + Id
    output_dir = r" --output_dir=D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master/output/predicate_classification_model/epochs700/" + Id + r"/"
    os.makedirs("D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master/output/predicate_classification_model/epochs700/"+Id+r"/")
    predict_relations_command = r"C:\Users\CivilIM\Anaconda3\envs\TF115P37\python.exe D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master\run_predicate_classification.py " + data_dir + output_dir
    os.system(predict_relations_command)
    print("finish predict_relations")
def check_predict_relations(Id):
    f = open(r"D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master/output/predicate_classification_model/epochs700/"+Id+r"/predicate_predict.txt")
    relations_result=f.read()
    relations_result=relations_result.replace("\n", "")
    str_list = relations_result.split(" ")
    print("check_predict_relations",str_list)
    if ("Road_status" in str_list) and ( "Road_position" in str_list) and ("Lane_of_Road" not in str_list) :
        return True
    elif ("Road_status" in str_list) and ( "Road_position" in str_list) and ("Lane_of_Road" in str_list) and ("Lane_status" in str_list) and (( "Lane_position" in str_list) or ("Lane_direction" in str_list)):
        return True
    else:
        return False
def prepare_data_for_extracting_SO(Id):
    data_dir = r"D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master-tweetclassification\bin/predicate_classifiction/classification_data/" + Id+"/test"
    predicate_classifiction_infer_file_dir=r"D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master\output\predicate_classification_model\epochs700/"+Id+"/"
    output_dir = r"D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master\bin\subject_object_labeling\sequence_labeling_data/" + Id + r"/test"
    os.makedirs(r"D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master\bin\subject_object_labeling\sequence_labeling_data/" + Id + r"/test/")
    #prepare_data_for_extracting_SO_command = r"C:\Users\CivilIM\Anaconda3\envs\TF115P37\python.exe D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master\bin/predicate_classifiction/prepare_data_for_labeling_infer.py"
    #os.system(prepare_data_for_extracting_SO_command)
    prepare_data_for_subject_object_labeling_infer(data_dir,predicate_classifiction_infer_file_dir,output_dir)

def extract_SO(Id):
    data_dir = r"--data_dir=D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master\bin\subject_object_labeling\sequence_labeling_data/" + Id
    output_dir = r" --output_dir=D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master\output/sequnce_infer_out/epochs700/ckpt12415/" + Id
    os.makedirs(r"D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master\output/sequnce_infer_out/epochs700/ckpt12415/"+Id+r"/")
    extract_SO_command = r"C:\Users\CivilIM\Anaconda3\envs\TF115P37\python.exe D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master\run_sequnce_labeling.py " + data_dir + output_dir
    os.system(extract_SO_command)

def generate_json_result(Id):
    spo_list_manager = Sorted_relation_and_entity_list_Management(
        r"D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master\bin\subject_object_labeling\sequence_labeling_data/"+Id+"/test",
        r"D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master\output\sequnce_infer_out\epochs700\ckpt12415/"+Id+"/",
        Competition_Mode=True)
    spo_list_manager.produce_output_file(
        OUT_RESULTS_DIR=r"D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master/output/final_text_spo_list_result/"+Id,
        keep_empty_spo_list=True)


#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def on_data(self, data):
    #print data
        with open('fetched_tweets.json','a') as tf:
            tf.write(data)
        data = json.loads(data)
        print (data)
        tweet=data['text']
        tweet=re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", " ", tweet)
        tweet=tweet.replace("  "," ")
        tweet = tweet.replace("  ", " ")
        tweet = tweet.replace("  ", " ")
        tweet = tweet.replace("  ", " ")
        tweet = tweet.replace("  ", " ")
        print(tweet)
        print(data['id'])
        tweet_storage=r"D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master-tweetclassification\bin/predicate_classifiction/classification_data/"+str(data['id'])+r"/test/"
        os.makedirs(tweet_storage)
        with open(tweet_storage+"text.txt",'w') as tf:
            tf.write(tweet)
        with open(tweet_storage+"token_in.txt",'w') as tf:
            tf.write(tweet)
        with open(tweet_storage+"token_in_not_UNK.txt",'w') as tf:
            tf.write(tweet)

        if str(data['user']['id'])=="1348585566040772609":
            claddify_traffic_and_non_traffic_tweet(str(data['id']))
            print("check_classification_result(str(data['id']))",check_classification_result(str(data['id'])))
            if check_classification_result(str(data['id']))==True:
                predict_relations(str(data['id']))
                print("check_predict_relations(str(data['id']))", check_predict_relations(str(data['id'])))
                if check_predict_relations(str(data['id']))==True:
                    prepare_data_for_extracting_SO(str(data['id']))
                    print("prepare_data_for_extracting_SO finish")
                    extract_SO(str(data['id']))
                    print("extract_SO finish")
                    generate_json_result(str(data['id']))
                    print("generate_json_result finish")
                    SPO2KG_Function(r"D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master/output/final_text_spo_list_result/"+str(data['id'])+r"\keep_empty_spo_list_subject_predicate_object_predict_output.json",graph)
                    print("Tweet2KnowledgeGraph finish")

        subprocess.Popen([r"C:\Program Files\ArcGIS\Pro/bin\Python\envs/arcgispro-py3\python.exe", r"D:/ZHOUSHENGHUA/PythonNeo4j/geodatabase.py"])
        return True

    def on_error(self, status):
        print (status)
    def on_status(self, status):
        print(status.text)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
#api.verify_credentials()

# --- 支持异步，参数is_async，推荐使用异步形式
myStream.filter(track=["st OR lane"], filter_level="low", follow=["1348585566040772609"],locations=[-84.501918,38.039574,-84.499156,38.049216], is_async=True)
#locations=[-84.501918,38.039574,-84.499156,38.049216]

print (myStream)
#print (myStreamListener.on_status())
#myStream.disconnect()
print ("OK")  