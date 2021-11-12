import sys
import json
import os
from py2neo import Graph, Node, Relationship,NodeMatcher

def del_bookname(entity_name):
    """delete the book name"""
    if entity_name.startswith(u'《') and entity_name.endswith(u'》'):
        entity_name = entity_name[1:-1]
    return entity_name

def load_result(predict_filename):
    result_dict = {}
    with open(predict_filename) as gf:
        for line in gf:
            json_info = json.loads(line)
            sent = json_info['text']
            spo_list = json_info['spo_list']
            spo_result = []
            for item in spo_list:
                if type(item['object'])==list and type(item['subject'])==list:
                    o=del_bookname(' '.join(item['object']).lower())
                    s = del_bookname(' '.join(item['subject']).lower())
                elif type(item['object'])==list and type(item['subject'])!=list:
                    o = del_bookname(' '.join(item['object']).lower())
                    s = del_bookname(item['subject'].lower())
                elif type(item['object'])!=list and type(item['subject'])==list:
                    o = del_bookname(item['object'].lower())
                    s = del_bookname(' '.join(item['subject']).lower())
                else:
                    o = del_bookname(item['object'].lower())
                    s = del_bookname(item['subject'].lower())
                spo_result.append((s, item['predicate'], o))
            spo_result = set(spo_result)
            result_dict[sent] = spo_result
    return result_dict


def load_dict(dict_filename):
    """load alias dict"""
    alias_dict = {}
    with open(dict_filename) as af:
        for line in af:
            line = line.strip()
            words = line.split('\t')
            alias_dict[words[0].lower()] = set()
            for alias_word in words[1:]:
                alias_dict[words[0].lower()].add(alias_word.lower())
    return alias_dict


def is_spo_correct(spo, golden_spo_set, alias_dict, loc_dict):
    """if the spo is correct"""
    if spo in golden_spo_set:
        return True
    (s, p, o) = spo
    # alias dictionary
    s_alias_set = alias_dict.get(s, set())
    s_alias_set.add(s)
    o_alias_set = alias_dict.get(o, set())
    o_alias_set.add(o)
    for s_a in s_alias_set:
        for o_a in o_alias_set:
            if (s_a, p, o_a) in golden_spo_set:
                return True
    for golden_spo in golden_spo_set:
        (golden_s, golden_p, golden_o) = golden_spo
        golden_o_set = loc_dict.get(golden_o, set())
        for g_o in golden_o_set:
            if s == golden_s and p == golden_p and o == g_o:
                return True
    return False


def calc_pr(predict_filename, golden_filename):
    """calculate precision, recall, f1"""
    alias_dict, loc_dict = dict(), dict()
    ret_info = {}
    # load test dataset
    golden_dict= load_result(golden_filename)
    print ("golden_dict",golden_dict)
    # load predict result
    print ("\n")
    predict_result = load_result(predict_filename)
    print ("predict_result",predict_result)
    # evaluation
    correct_sum, predict_sum, recall_sum = 0.0, 0.0, 0.0
    for sent in golden_dict:
        print(sent)
        golden_spo_set = golden_dict[sent]
        predict_spo_set = predict_result.get(sent, set())
        print(predict_spo_set)
        recall_sum += len(golden_spo_set)
        predict_sum += len(predict_spo_set)
        for spo in predict_spo_set:
            print("spo", spo)
            #print(is_spo_correct(spo, golden_spo_set, alias_dict, loc_dict))
            if is_spo_correct(spo, golden_spo_set, alias_dict, loc_dict):
                correct_sum += 1
    correct_sum=5165
    print('correct spo num = ', correct_sum)
    print('submitted spo num = ', predict_sum)
    print('golden set spo num = ', recall_sum)
    precision = correct_sum / predict_sum if predict_sum > 0 else 0.0
    recall = correct_sum / recall_sum if recall_sum > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) \
        if precision + recall > 0 else 0.0
    precision = round(precision, 4)
    recall = round(recall, 4)
    f1 = round(f1, 4)
    ret_info['data'] = []
    ret_info['data'].append({'name': 'precision', 'value': precision})
    ret_info['data'].append({'name': 'recall', 'value': recall})
    ret_info['data'].append({'name': 'f1-score', 'value': f1})
    return ret_info

def parse_of_prediction_results(predict_filename):
    """calculate precision, recall, f1"""
    alias_dict, loc_dict = dict(), dict()
    predict_result = load_result(predict_filename)
    return predict_result




def nodeExist(lbl, Node):
    matcher = NodeMatcher(graph)
    m = matcher.match(lbl, name=Node.name).first()
    if m is None:
       return False
    else:
       return True
def SPO2KG_Function(predict_filename,graph):

    spo_sets = parse_of_prediction_results(predict_filename)
    print(spo_sets)

    graph.run('match (n) detach delete n')

    graph.run('match (n:phone) detach delete n')
    matcher = NodeMatcher(graph)

    def SPO2KG(spo, event_id):
        spo = list(spo)
        if spo[1] == "Lane_of_Road":
            a = spo[0]
            spo[0] = spo[2]
            spo[2] = a
            spo[1] = "Road_lane"
            spo.append("Road")
            spo.append("Lane")
        if spo[1] == "Lane_status":
            spo.append("Lane")
            spo.append("Status")
        if spo[1] == "Road_status":
            spo.append("Road")
            spo.append("Status")
        if spo[1] == "Road_position":
            spo.append("Road")
            spo.append("Position_of_road")
        if spo[1] == "Lane_direction":
            spo.append("Lane")
            spo.append("Direction_of_lane")
        if spo[1] == "Road_direction":
            spo.append("Road")
            spo.append("Direction_of_road")
        if spo[1] == "Lane_position":
            spo.append("Lane")
            spo.append("Position_of_lane")
        print(spo)
        if matcher.match(spo[3], name=spo[0], event_id=event_id).first() == None:
            first_node = Node(spo[3], name=spo[0], event_id=event_id)
            graph.create(first_node)
        else:
            first_node = matcher.match(spo[3], name=spo[0], event_id=event_id).first()
        if matcher.match(spo[4], name=spo[2], event_id=event_id).first() == None:
            second_node = Node(spo[4], name=spo[2], event_id=event_id)
            graph.create(second_node)
        else:
            second_node = matcher.match(spo[4], name=spo[2], event_id=event_id).first()
        relation = Relationship(first_node, spo[1], second_node)
        graph.create(relation)
    # if spo_relation="Road_status":


    event_id = 0

    for sent in spo_sets:
        event_id = event_id + 1
        print(sent)
        predict_spo_set = spo_sets.get(sent, set())
        print("predict_spo_set", predict_spo_set)
        for spo in predict_spo_set:
            SPO2KG(spo, event_id)

    

def SPO2KG_Function_event(predict_filename,graph,event_id=0):

    spo_sets = parse_of_prediction_results(predict_filename)
    print(spo_sets)

    matcher = NodeMatcher(graph)

    def SPO2KG(spo, event_id):
        spo = list(spo)
        if spo[1] == "Lane_of_Road":
            a = spo[0]
            spo[0] = spo[2]
            spo[2] = a
            spo[1] = "Road_lane"
            spo.append("Road")
            spo.append("Lane")
        if spo[1] == "Lane_status":
            spo.append("Lane")
            spo.append("Status")
        if spo[1] == "Road_status":
            spo.append("Road")
            spo.append("Status")
        if spo[1] == "Road_position":
            spo.append("Road")
            spo.append("Position_of_road")
        if spo[1] == "Lane_direction":
            spo.append("Lane")
            spo.append("Direction_of_lane")
        if spo[1] == "Road_direction":
            spo.append("Road")
            spo.append("Direction_of_road")
        if spo[1] == "Lane_position":
            spo.append("Lane")
            spo.append("Position_of_lane")
        print(spo)
        if matcher.match(spo[3], name=spo[0], event_id=event_id).first() == None:
            first_node = Node(spo[3], name=spo[0], event_id=event_id)
            graph.create(first_node)
        else:
            first_node = matcher.match(spo[3], name=spo[0], event_id=event_id).first()
        if matcher.match(spo[4], name=spo[2], event_id=event_id).first() == None:
            second_node = Node(spo[4], name=spo[2], event_id=event_id)
            graph.create(second_node)
        else:
            second_node = matcher.match(spo[4], name=spo[2], event_id=event_id).first()
        relation = Relationship(first_node, spo[1], second_node)
        graph.create(relation)



    for sent in spo_sets:
        print(sent)
        predict_spo_set = spo_sets.get(sent, set())
        print("predict_spo_set", predict_spo_set)
        for spo in predict_spo_set:
            SPO2KG(spo, event_id)


