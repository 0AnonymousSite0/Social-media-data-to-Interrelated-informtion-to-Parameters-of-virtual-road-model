
import arcpy
import math
import  pandas  as pd
from py2neo import Graph, Node, Relationship,NodeMatcher
import time
#from __future__ import print_function
import os
# COM-Server
import win32com.client as com
import numpy as np
import time
from Operations_of_VRMs import adjust_traffic_flow
import operator
from functools import reduce
import difflib



def angle(v1, v2):
    dx1 = v1[2] - v1[0]
    dy1 = v1[3] - v1[1]
    dx2 = v2[2] - v2[0]
    dy2 = v2[3] - v2[1]
    angle1 = math.atan2(dy1, dx1)
    angle1 = int(angle1 * 180/math.pi)

    angle2 = math.atan2(dy2, dx2)
    angle2 = int(angle2 * 180/math.pi)

    if angle1*angle2 >= 0:
        included_angle = abs(angle1-angle2)
    else:
        included_angle = abs(angle1) + abs(angle2)
        if included_angle > 180:
            included_angle = 360 - included_angle
    return included_angle

def direction_angle(v1, v2):
    dx1 = v1[2] - v1[0]
    dy1 = v1[3] - v1[1]
    dx2 = v2[2] - v2[0]
    dy2 = v2[3] - v2[1]
    angle1 = math.atan2(dy1, dx1)
    angle1 = int(angle1 * 180/math.pi)
    # print(angle1)
    angle2 = math.atan2(dy2, dx2)
    angle2 = int(angle2 * 180/math.pi)
    # print(angle2)
    if angle1*angle2 >= 0:
        included_angle = abs(angle1-angle2)
    else:
        included_angle = abs(angle1) + abs(angle2)
    return included_angle

def between_mode(road_A,road_B,road_C):
    road_A.upper()
    road_B.upper()
    road_C.upper()
    road_A=fuzzy_query_of_road_name(road_A)
    road_B=fuzzy_query_of_road_name(road_B)
    symbol = '\''
    field = "\"ROADNAME\"="
    ROAD_A_segs=arcpy.SelectLayerByAttribute_management(fr, 'NEW_SELECTION', field+symbol+road_A+symbol)
    print("a")
    print(field+symbol+road_A+symbol)
    arcpy.CopyFeatures_management(ROAD_A_segs, arcpy.env.workspace+'/ROAD_A'+str(time.time())[0:9])
    ROAD_B_segs = arcpy.SelectLayerByAttribute_management(fr, 'NEW_SELECTION', field+symbol+road_B+symbol)
    arcpy.CopyFeatures_management(ROAD_B_segs, arcpy.env.workspace + '/ROAD_B' + str(time.time())[0:9])
    ROAD_C_segs = arcpy.SelectLayerByAttribute_management(fr, 'NEW_SELECTION', field+symbol+road_C+symbol)
    arcpy.CopyFeatures_management(ROAD_C_segs, arcpy.env.workspace + '/ROAD_C' + str(time.time())[0:9])
    ROAD_D_segs=arcpy.SelectLayerByLocation_management(ROAD_A_segs, "BOUNDARY_TOUCHES", ROAD_B_segs, "", "SUBSET_SELECTION")
    ROAD_E_segs=arcpy.SelectLayerByLocation_management(ROAD_D_segs, "BOUNDARY_TOUCHES", ROAD_C_segs, "", "SUBSET_SELECTION")
    filter_lines = 'ROAD_E' + str(time.time())[0:9]
    arcpy.CopyFeatures_management(ROAD_E_segs, arcpy.env.workspace + r'/'+filter_lines)
    cursor = arcpy.SearchCursor(arcpy.env.workspace + "\\" + filter_lines)  # search the records in the shp file

    for row in cursor:
        print("row.SCLINK", row.SCLINK)  # int
        road_segments = df[
            df.linkingeodb == str(row.SCLINK)].index.tolist()  # string,extract the index of road segment (two segment)
        # print("road_segments",road_segments)
        if row.ONEWAY=="B":
            segment_with_highest_possibility_DESB_index = determine_segment_direction(
            df_kg.at[df_kg[df_kg.P == "Road_direction"].index.tolist()[0], "O"], road_segments)  # later change it to item set
            print("segment_with_highest_possibility_DESB_index",
              segment_with_highest_possibility_DESB_index)  # pandas索引56，编号57
        else:
            segment_with_highest_possibility_DESB_index=road_segments

    return segment_with_highest_possibility_DESB_index

def past_mode(road_A,road_B):
    road_A.upper()
    road_B.upper()
    symbol = '\''
    field = "\"ROADNAME\"="
    sclinkfield="\"SCLINK\""
    road_A=fuzzy_query_of_road_name(road_A)
    road_B=fuzzy_query_of_road_name(road_B)
    ROAD_A_segs=arcpy.SelectLayerByAttribute_management(fr, 'NEW_SELECTION', field+symbol+road_A+symbol)
    print("a")
    print(field+symbol+road_A+symbol)
    arcpy.CopyFeatures_management(ROAD_A_segs, arcpy.env.workspace+'/ROAD_A'+str(time.time())[0:9])
    ROAD_B_segs = arcpy.SelectLayerByAttribute_management(fr, 'NEW_SELECTION', field+symbol+road_B+symbol)
    arcpy.CopyFeatures_management(ROAD_B_segs, arcpy.env.workspace + '/ROAD_B' + str(time.time())[0:9])

    ROAD_D_segs=arcpy.SelectLayerByLocation_management(ROAD_A_segs, "BOUNDARY_TOUCHES", ROAD_B_segs, "", "SUBSET_SELECTION")
    filter_lines_past = 'ROAD_D_segs' + str(time.time())[0:9]

    arcpy.CopyFeatures_management(ROAD_D_segs, arcpy.env.workspace + r'/'+filter_lines_past)
    cursor = arcpy.SearchCursor(arcpy.env.workspace + "\\" + filter_lines_past)  # search the records in the shp file
    road_segments=[]
    for row in cursor:
        print("row.SCLINK", row.SCLINK)  # int
        road_segments.append(df[df.linkingeodb == str(row.SCLINK)].index.tolist())  # string,extract the index of road segment (two segment)

    road_segments=reduce(operator.add, road_segments)
    print("road_segments", road_segments)
    filtered_line_with_sequence=[]

    for i in road_segments:
        connections = df[df['tolink'] == str(int(i)+1)].index.tolist()
        for j in connections:
            if int(df.at[j, "fromlink"])-1 in road_segments:
                filtered_line_with_sequence.append(i)


    print ("filtered_line_with_sequence",filtered_line_with_sequence)
    filter_lines='ROAD_E' + str(time.time())[0:9]
    # filtered_line_with_sequence=[87,98]
    if df_kg.at[df_kg[df_kg.P == "Road_direction"].index.tolist()[0], "O"]!= "Blank":
        filtered_line_with_sequence_and_direction = determine_segment_direction(
            df_kg.at[df_kg[df_kg.P == "Road_direction"].index.tolist()[0], "O"], filtered_line_with_sequence)
        print ("filtered_line_with_sequence_and_direction",filtered_line_with_sequence_and_direction)
    else:
        filtered_line_with_sequence_and_direction=filtered_line_with_sequence
    return filtered_line_with_sequence_and_direction

def prior_mode(road_A,road_B):
    road_A.upper()
    road_B.upper()
    symbol = '\''
    field = "\"ROADNAME\"="
    sclinkfield = "\"SCLINK\""
    road_A=fuzzy_query_of_road_name(road_A)
    road_B=fuzzy_query_of_road_name(road_B)
    print ("road_B",road_B)
    ROAD_A_segs = arcpy.SelectLayerByAttribute_management(fr, 'NEW_SELECTION', field + symbol + road_A + symbol)
    print("a")
    print(field + symbol + road_A + symbol)
    arcpy.CopyFeatures_management(ROAD_A_segs, arcpy.env.workspace + '/ROAD_A' + str(time.time())[0:9])
    ROAD_B_segs = arcpy.SelectLayerByAttribute_management(fr, 'NEW_SELECTION', field + symbol + road_B + symbol)
    arcpy.CopyFeatures_management(ROAD_B_segs, arcpy.env.workspace + '/ROAD_B' + str(time.time())[0:9])

    ROAD_D_segs = arcpy.SelectLayerByLocation_management(ROAD_A_segs, "BOUNDARY_TOUCHES", ROAD_B_segs, "",
                                                         "SUBSET_SELECTION")
    filter_lines_past = 'ROAD_D_segs' + str(time.time())[0:9]

    arcpy.CopyFeatures_management(ROAD_D_segs, arcpy.env.workspace + r'/' + filter_lines_past)
    cursor = arcpy.SearchCursor(arcpy.env.workspace + "\\" + filter_lines_past)  # search the records in the shp file
    road_segments = []
    for row in cursor:
        print("row.SCLINK", row.SCLINK)  # int
        road_segments.append(df[df.linkingeodb == str(
            row.SCLINK)].index.tolist())  # string,extract the index of road segment (two segment)

    road_segments = reduce(operator.add, road_segments)
    print("road_segments", road_segments)
    filtered_line_with_sequence = []
    for i in road_segments:
        connections = df[df['fromlink'] == str(int(i) + 1)].index.tolist()
        for j in connections:
            if int(df.at[j, "tolink"]) - 1 in road_segments:
                filtered_line_with_sequence.append(i)

    print("filtered_line_with_sequence", filtered_line_with_sequence)
    filter_lines = 'ROAD_E' + str(time.time())[0:9]
    # filtered_line_with_sequence=[87,98]
    if df_kg.at[df_kg[df_kg.P == "Road_direction"].index.tolist()[0], "O"] != "Blank":
        filtered_line_with_sequence_and_direction = determine_segment_direction(
            df_kg.at[df_kg[df_kg.P == "Road_direction"].index.tolist()[0], "O"], filtered_line_with_sequence)
        print("filtered_line_with_sequence_and_direction", filtered_line_with_sequence_and_direction)
    else:
        filtered_line_with_sequence_and_direction = filtered_line_with_sequence
    return filtered_line_with_sequence_and_direction

def extract_road_in_road_position(extracted_postion_of_road_text):
    road1=""
    road2=""
    if "between" in extracted_postion_of_road_text:
        splitted_text = extracted_postion_of_road_text.split(" and ")
        road2 = splitted_text[1]
        road1 = splitted_text[0].split("between ")[1]
        print(road1)
        print(road2)
    if ("past" in extracted_postion_of_road_text):
        splitted_text = extracted_postion_of_road_text.split("past ")
        road1 = splitted_text[1]
        print(road1)
    if ("toward" in extracted_postion_of_road_text):
        splitted_text = extracted_postion_of_road_text.split("toward ")
        road1 = splitted_text[1]
        print(road1)
    if ("towards" in extracted_postion_of_road_text):
        splitted_text = extracted_postion_of_road_text.split("towards ")
        road1 = splitted_text[1]
        print(road1)
    if ("to" in extracted_postion_of_road_text):
        splitted_text = extracted_postion_of_road_text.split("to ")
        road1 = splitted_text[1]
        print(road1)
    if ("approach" in extracted_postion_of_road_text):
        splitted_text = extracted_postion_of_road_text.split("approach ")
        road1 = splitted_text[1]
        print(road1)
    if ("approaching" in extracted_postion_of_road_text):
        splitted_text = extracted_postion_of_road_text.split("approaching ")
        road1 = splitted_text[1]
        print(road1)
    if ("leaving" in extracted_postion_of_road_text):
        splitted_text = extracted_postion_of_road_text.split("leaving ")
        road1 = splitted_text[1]
        print(road1)
    if ("leave" in extracted_postion_of_road_text):
        splitted_text = extracted_postion_of_road_text.split("leave ")
        road1 = splitted_text[1]
        print(road1)
    if ("off" in extracted_postion_of_road_text):
        splitted_text = extracted_postion_of_road_text.split("off ")
        road1 = splitted_text[1]
        print(road1)
    if "prior" in extracted_postion_of_road_text:
        splitted_text = extracted_postion_of_road_text.split("prior to ")
        road1 = splitted_text[1]
        print(road1)
    #new feature words could be flexibly added
    return road1,road2

def KG2PD (p):
    CQL_query=r"match (s)-[p:"+p+"]->(o) where s.event_id=1 return s,p,o"
    if len(graph.run(CQL_query).data())>0:
        #print(graph.run(CQL_query).data())
        extracted_spo = graph.run(CQL_query).data()
        print(extracted_spo)
        print(type(extracted_spo[0]))
        spo_dic = extracted_spo[0]
        extracted_s = spo_dic['s']
        extracted_o = spo_dic['o']
        extracted_s_text = dict(extracted_s)['name']
        extracted_o_text = dict(extracted_o)['name']
        return extracted_s_text,p,extracted_o_text
    else:
        return "Blank",p,"Blank"

def determine_road_segment(road_position_phase,affect_road,road1,road2):
    affect_road=affect_road.upper()
    road1=road1.upper()
    road2=road2.upper()
    if "between" in road_position_phase:
        filtered_road_segment=between_mode(affect_road,road1,road2)
    if "prior" in road_position_phase or "approach" in road_position_phase or "toward" in road_position_phase or "to" in road_position_phase:
        filtered_road_segment=prior_mode(affect_road,road1)
    if "past" in road_position_phase or "off" in road_position_phase or "leave" in road_position_phase or "from" in road_position_phase:
        filtered_road_segment=past_mode(affect_road,road1)
    return filtered_road_segment

def determine_segment_direction (road_direction,all_road_segments_satisfying_road_position):
    if "both" in road_direction:
        return all_road_segments_satisfying_road_position
    else:
        coordinate_of_inbound_direction = [110.715, -241.372, 860.536, 420.372] #depends on the city
        coordinate_of_outbound_direction = [860.536, 420.372, 110.715, -241.372]
        coordinate_of_eastnound_direction = [0, 0, 1, 0]
        coordinate_of_southbound_direction = [0, 0, 0, -1]
        coordinate_of_westbound_direction = [0, 0, -1, 0]
        coordinate_of_northbound_direction = [0, 0, 0, 1]
        if "inbound" in road_direction:
            coordinate_of_direction=coordinate_of_inbound_direction
        if "outbound" in road_direction:
            coordinate_of_direction=coordinate_of_outbound_direction
        if "eastbound" in road_direction:
            coordinate_of_direction=coordinate_of_eastnound_direction
        if "southbound" in road_direction:
            coordinate_of_direction=coordinate_of_southbound_direction
        if "westbound" in road_direction:
            coordinate_of_direction=coordinate_of_westbound_direction
        if "northbound" in road_direction:
            coordinate_of_direction=coordinate_of_northbound_direction
        coordinate_of_road_segment=[]
        segment_with_highest_possibility=0
        min_angle_between_seg_and_direction=181
        print("all_road_segments_satisfying_road_position",all_road_segments_satisfying_road_position)
        for index,i in enumerate(all_road_segments_satisfying_road_position):
            print("all_road_segments_satisfying_road_position",i)
            coordinate_of_road_segment.append(df.at[i, "firstlinkpolyptsx"])
            coordinate_of_road_segment.append(df.at[i, "firstlinkpolyptsy"])
            coordinate_of_road_segment.append(df.at[i, "lastlinkpolyptsx"])
            coordinate_of_road_segment.append(df.at[i, "lastlinkpolyptsy"])
            angle_between_seg_and_direction=angle(coordinate_of_direction, coordinate_of_road_segment)
            print("angle_between_seg_and_direction",angle_between_seg_and_direction)
            if angle_between_seg_and_direction<min_angle_between_seg_and_direction:
                min_angle_between_seg_and_direction=angle_between_seg_and_direction
                segment_with_highest_possibility=index
            segment_with_highest_possibility_DESB_index=all_road_segments_satisfying_road_position[segment_with_highest_possibility]
        return segment_with_highest_possibility_DESB_index


arcpy.env.overwriteOutput = True
arcpy.env.workspace =r"C:\Users\CivilIM\Documents\ArcGIS\Projects\RoadofLex\RoadofLex.gdb"
file_of_geodatabase=r"C:\Users\CivilIM\Documents\ArcGIS\Projects\RoadofLex"
graph = Graph('http://localhost:7474', username='neo4j', password='ab014415')
matcher = NodeMatcher(graph)
fr= arcpy.env.workspace + '/LexStreets'
df=pd.read_excel(file_of_geodatabase+r'\roadsegments.xls')
def fuzzy_query_of_road_name(road):
    road.upper()
    road_after_fuzzy_match=""
    if road in df["name"]:
        return road

    else:
        min_dis=0 #1 is the best
        for road_name in df["name"]:
            if difflib.SequenceMatcher(None, road, road_name).quick_ratio()>min_dis:
                min_dis=difflib.SequenceMatcher(None, road, road_name).quick_ratio()
                road_after_fuzzy_match=road_name
                print("road_name", road_name)
                print("dis", difflib.SequenceMatcher(None, road, road_name).quick_ratio())
        return road_after_fuzzy_match

print ("quality",fuzzy_query_of_road_name("QUALTY"))
print(df)
df_kg=pd.read_excel(file_of_geodatabase+r'\kg.xls')

for index,p in enumerate(["Road_status","Road_direction","Road_position","Lane_status","Road_lane","Lane_position","Lane_direction"]):
    s,p_r,o=KG2PD(p)
    df_kg.iat[index,0]=s
    df_kg.iat[index, 1] = p
    df_kg.iat[index, 2] = o
print("knowledge graph:", df_kg)
affect_road=df_kg.at[df_kg[df_kg.P == "Road_position"].index.tolist()[0],"S"]
road1,road2=extract_road_in_road_position(df_kg.at[df_kg[df_kg.P == "Road_position"].index.tolist()[0],"O"])
print ("road1,road2",road1,road2)
filter_lines=determine_road_segment(df_kg.at[df_kg[df_kg.P == "Road_position"].index.tolist()[0],"O"],affect_road,road1,road2)
print("source_of_filtered_lines",filter_lines)
segment_with_highest_possibility_DESB_index=filter_lines

def lane_position_conditions(segment_with_highest_possibility_DESB_index,lane_position_text):
    affected_lane_from_pos=[]
    print("segment_with_highest_possibility_DESB_index",segment_with_highest_possibility_DESB_index)
    segment_with_highest_possibility_DESB_index=segment_with_highest_possibility_DESB_index[0]
    if "right" in lane_position_text:
        affected_lane_from_pos.append(str(segment_with_highest_possibility_DESB_index+1)+"-"+"1")
    if "left" in lane_position_text:
        affected_lane_from_pos.append(str(segment_with_highest_possibility_DESB_index+1)+"-"+str(df.at[segment_with_highest_possibility_DESB_index,"numlanes"]))
    if "center" in lane_position_text or  "middle" in lane_position_text:
        affected_lane_from_pos.append(str(segment_with_highest_possibility_DESB_index+1)+"-"+str(math.floor(int(df.at[segment_with_highest_possibility_DESB_index,"numlanes"]+1)/2)))
    return affected_lane_from_pos

def  lane_direction_conditions(segment_with_highest_possibility_DESB_index,lane_direction_text):
    all_lane_connections = df[(df['fromlink'] == str(
        int(segment_with_highest_possibility_DESB_index) + 1))].index.tolist()  # 从这个link出发到其他link的lane，所有索引
    print("all_lane_connections",all_lane_connections)
    coordinates_linkfrom = [df.at[int(segment_with_highest_possibility_DESB_index), "firstlinkpolyptsx"],
                            df.at[int(segment_with_highest_possibility_DESB_index), "firstlinkpolyptsy"],
                            df.at[int(segment_with_highest_possibility_DESB_index), "lastlinkpolyptsx"],
                            df.at[int(segment_with_highest_possibility_DESB_index), "lastlinkpolyptsy"]]
    df_lane_direction = pd.DataFrame(
        columns=("from lane", 'fromlink', 'lane_no', "direction_text", 'tolink', 'tolinkname', "numlanes","connector"))
    print("df_lane_direction",df_lane_direction)
    lane_direction_condition_no = 0
    for i in all_lane_connections:  # 所有的lane
        df.at[i, "fromlane"]
        coordinates_linkconnector = [df.at[i, "firstlinkpolyptsx"], df.at[i, "firstlinkpolyptsy"],
                                     df.at[i, "lastlinkpolyptsx"], df.at[i, "lastlinkpolyptsy"]]
        lane_sets = [df.at[i, "fromlane"], df.at[i, "tolane"], df.at[i, "fromlink"], df.at[i, "tolink"]]
        #print(coordinates_linkfrom, coordinates_linkconnector)
        print("angle:", direction_angle(coordinates_linkfrom, coordinates_linkconnector))
        angle_of_connector = direction_angle(coordinates_linkfrom, coordinates_linkconnector)
        if angle_of_connector < 15 or angle_of_connector > 345:
            direction_text = "through"
        if angle_of_connector > 15 and angle_of_connector < 90:
            direction_text = "left turn"
        if angle_of_connector > 270 and angle_of_connector < 345:
            direction_text = "right turn"
        print("connecter:", df.at[i, "fromlane"], df.at[i, "tolane"], df.at[i, "numlanes"])

        lane_no = df.at[i, "fromlane"]
        splitted_lane_no = lane_no.split("-")
        for p in range(int(splitted_lane_no[1]), int(splitted_lane_no[1]) + int(df.at[i, "numlanes"])):
            #print("lane information", df.at[i, "fromlink"], p, direction_text, df.at[i, "tolink"], df.at[i, "numlanes"])
            df_lane_direction.loc[lane_direction_condition_no] = [str(df.at[i, "fromlink"]) + "-" + str(p),
                                                                  df.at[i, "fromlink"], p, direction_text,
                                                                  df.at[i, "tolink"], df.at[df[df.linkindedb == int(
                    df.at[i, "tolink"])].index.tolist()[0], "name"], df.at[i, "numlanes"],i]
            lane_direction_condition_no = lane_direction_condition_no + 1
        print("df_lane_direction",df_lane_direction)
    #print(lane_direction_text, "lane_direction_text")
    affected_lane = []
    if "right" in lane_direction_text and "turn" in lane_direction_text:
        for i in df_lane_direction[df_lane_direction['direction_text'] == "right turn"].index.tolist():
            affected_lane.append(df_lane_direction.at[i, "from lane"])
    if "left turn" in lane_direction_text and "turn" in lane_direction_text:
        for i in df_lane_direction[df_lane_direction['direction_text'] == "left turn"].index.tolist():
            affected_lane.append(df_lane_direction.at[i, "from lane"])
    if ( "thru" in lane_direction_text or "through" in lane_direction_text) and "left" not in lane_direction_text and "right" not in lane_direction_text:
        for i in df_lane_direction[df_lane_direction['direction_text'] == "through"].index.tolist():
            affected_lane.append(df_lane_direction.at[i, "from lane"])
    if "approach" in lane_direction_text or "toward" in lane_direction_text:
        for i in range(len(df_lane_direction.index)):
            print ("tolinkname",df_lane_direction.at[i, "tolinkname"].lower())
            if df_lane_direction.at[i, "tolinkname"].lower() in lane_direction_text:
                affected_lane.append(df_lane_direction.at[i, "from lane"])
    if ("thru" in lane_direction_text or "through" in lane_direction_text) and "left" in lane_direction_text:
        left_thru_lane = -1
        for i in df_lane_direction[df_lane_direction['direction_text'] == "through"].index.tolist():
            if left_thru_lane < int(df_lane_direction.at[i, "lane_no"]):
                left_thru_lane = int(df_lane_direction.at[i, "lane_no"])
        #print("left_thru_lane", left_thru_lane)
        affected_lane.append(df_lane_direction.at[df_lane_direction[
                                                      (df_lane_direction['direction_text'] == "through") & (
                                                                  df_lane_direction[
                                                                      "lane_no"] == left_thru_lane)].index.tolist()[
                                                      0], "from lane"])
    if ("thru" in lane_direction_text or "through" in lane_direction_text) and "right" in lane_direction_text:
        left_thru_lane = 100
        for i in df_lane_direction[df_lane_direction['direction_text'] == "through"].index.tolist():
            if left_thru_lane > int(df_lane_direction.at[i, "lane_no"]):
                left_thru_lane = int(df_lane_direction.at[i, "lane_no"])
        #print("left_thru_lane", left_thru_lane)
        affected_lane.append(df_lane_direction.at[df_lane_direction[
                                                      (df_lane_direction['direction_text'] == "through") & (
                                                                  df_lane_direction[
                                                                      "lane_no"] == left_thru_lane)].index.tolist()[
                                                      0], "from lane"])
    print("lane_information_from_direction:",affected_lane)
    return affected_lane,df_lane_direction


if df_kg.at[df_kg[df_kg.P == "Lane_status"].index.tolist()[0], "O"] != "Blank" :

    affected_lane_from_dir=[]
    affected_lane_from_pos=[]
    affected_lane_in_the_incident=[]

    if df_kg.at[df_kg[df_kg.P == "Lane_direction"].index.tolist()[0],"O"]!="Blank":
        lane_direction_text=df_kg.at[df_kg[df_kg.P == "Lane_direction"].index.tolist()[0],"O"]
        #lane_direction_text="left thru"
        affected_lane_from_dir,df_lane_direction=lane_direction_conditions(segment_with_highest_possibility_DESB_index,lane_direction_text)
        print("affected_lane_from_dir",affected_lane_from_dir)
    if df_kg.at[df_kg[df_kg.P == "Lane_position"].index.tolist()[0],"O"]!="Blank":
        lane_position_text=df_kg.at[df_kg[df_kg.P == "Lane_position"].index.tolist()[0],"O"]
        print ("lane_position_text",lane_position_text)
        #lane_position_text="left and center"
        affected_lane_from_pos = lane_position_conditions(segment_with_highest_possibility_DESB_index,lane_position_text)
        print ("affected_lane_from_pos",affected_lane_from_pos)
    if df_kg.at[df_kg[df_kg.P == "Lane_position"].index.tolist()[0], "O"] != "Blank" and df_kg.at[
        df_kg[df_kg.P == "Lane_direction"].index.tolist()[0], "O"] != "Blank":
        if affected_lane_from_pos != affected_lane_from_pos:
            print("remider : the lane_direction and lane_position provide different lane information")
            affected_lane_in_the_incident=list(set(affected_lane_from_dir + affected_lane_from_pos))
        else:
            affected_lane_in_the_incident=affected_lane_from_pos

    if df_kg.at[df_kg[df_kg.P == "Lane_position"].index.tolist()[0], "O"] != "Blank" and df_kg.at[
        df_kg[df_kg.P == "Lane_direction"].index.tolist()[0], "O"] == "Blank":
        affected_lane_in_the_incident=affected_lane_from_pos

    if df_kg.at[df_kg[df_kg.P == "Lane_position"].index.tolist()[0], "O"] == "Blank" and df_kg.at[
        df_kg[df_kg.P == "Lane_direction"].index.tolist()[0], "O"] != "Blank":
        affected_lane_in_the_incident=affected_lane_from_dir
    print ("affected_lane_in_the_incident",affected_lane_in_the_incident)

else:
    affected_lane_in_the_incident=[]
    print("remider : No lane-related information, and it is default that all lanes are affected.")


information2DEDB=[[],[]]
information2DEDB[0]=int(segment_with_highest_possibility_DESB_index[0])+1
information2DEDB[1]=affected_lane_in_the_incident
print("information2DEDB",information2DEDB)

#Vissim = com.gencache.EnsureDispatch("Vissim.Vissim") #
Vissim = com.Dispatch("Vissim.Vissim")
Filename = os.path.join('D:\\ZHOUSHENGHUA\\Lexington\\', 'LexingtonForUses.inpx')
Vissim.LoadNet(Filename)



if information2DEDB[1]==None:
    adjust_traffic_flow(information2DEDB[0])
else:
    for i in information2DEDB[1]:
        link_lane_no= i
        lane_no = link_lane_no.split("-")
        print("lane_no",lane_no)
        Vissim.Net.Links.ItemByKey(int(information2DEDB[0])).Lanes.ItemByKey(int(lane_no[1])).SetAttValue("BlockedVehClasses", "10,20,30,40,50")
#    Vissim.Net.Links.ItemByKey(df_lane_direction[df_lane_direction.P == "Lane_direction"].index.tolist()[0], "connector"]).Lanes.ItemByKey(int(lane_no[1])).SetAttValue("BlockedVehClasses", "10,20,30,40,50")
print("topology updated")








