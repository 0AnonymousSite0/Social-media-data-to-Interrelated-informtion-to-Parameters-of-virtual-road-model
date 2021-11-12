
import xlwt

def get_index(lst=None, item=''):
    return [index for (index, value) in enumerate(lst) if value == item]

def get_SBI(lst, item1,item2):
    return get_index(lst, item1)+get_index(lst,item2)

def index2word(lst, items):
    a=[]
    for i in items:
        b=i
        a.append(lst[b])
    return a






#file = r'D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master\bin\subject_object_labeling\sequence_labeling_data\train\token_label_and_one_prdicate_out.txt'
#file2 = r'D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master\bin\subject_object_labeling\sequence_labeling_data\train\token_in.txt'
#file = r'D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master\bin\subject_object_labeling\sequence_labeling_data\valid\token_label_and_one_prdicate_out.txt'
#file2 = r'D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master\bin\subject_object_labeling\sequence_labeling_data\valid\token_in.txt'
file = r'D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master\bin\subject_object_labeling\sequence_labeling_data\test\token_label_and_one_prdicate_out.txt'
file2 = r'D:\ZHOUSHENGHUA\PycharmProjects\Entity-Relation-Extraction-master\bin\subject_object_labeling\sequence_labeling_data\test\token_in.txt'

all_tweets=[]
with open(file, 'r',encoding="utf-8") as f:  #可读可写二进制，文件若不存在就创建
    data = f.readlines() #读取文本所有内容，并且以数列的格式返回结果，一般配合for in使用

with open(file2, 'r', encoding="utf-8") as f2:  # 可读可写二进制，文件若不存在就创建
    textdata = f2.readlines()  # 读取文本所有内容，并且以数列的格式返回结果，一般配合for in使用
    #print (data)
    n=0
for i in data:
    tweet=textdata[n]
        # print (i)
    tweet = tweet.replace("\t", " ")
    tweet = tweet.replace("\n", "")
    tweet = tweet.split(" ")
    print(tweet)
    #print (i)
    i=i.replace("\t", " ")
    i = i.replace("\n", "")
    IO_words=i.split(" ")
    print (IO_words)
    BSUB=get_index(IO_words,"B-SUB")
    #ISUB=get_index(IO_words, "I-SUB")
    #print(BSUB)
    SUB_index=get_SBI(IO_words, "B-SUB","I-SUB")
    OBJ_index = get_SBI(IO_words, "B-OBJ", "I-OBJ")
    #print(SUB_index)
    subject=index2word(tweet,SUB_index)
    object=index2word(tweet,OBJ_index)
    get_index(IO_words, "B-OBJ")
    get_index(IO_words, "I-OBJ")
    if len(tweet)!=len(IO_words):
        print(n)
    n=n+1
        #words=IO_words.split(" ")
        #print(words)

    tweet_result=[]
    tweet_result.append(' '.join(tweet))
    tweet_result.append(tweet[len(tweet)-1])
    tweet_result.append(' '.join(subject))
    tweet_result.append(str(SUB_index[0]))
    tweet_result.append(' '.join(object))
    tweet_result.append(str(OBJ_index[0]))
    all_tweets.append(tweet_result)




    print(tweet_result)
#sentence,relation,head,head_offset,tail,tail_offset

def write_excel_xls(path, sheet_name, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿
    print("Results are successfully saved！")


write_excel_xls('./all_annotated_tweets_test.xls', "tweets", all_tweets)



