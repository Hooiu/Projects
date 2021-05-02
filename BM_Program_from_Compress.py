import xml.etree.ElementTree as ET
import glob

file_name = '01-T-051 (5900 10200 7200 x 32000 - SKIRT)'
tree = ET.parse(file_name + '.xml')
root_pv = tree.find('pressureVessel')

# List에서 중복값 제거 (순서 상관O)

def Remove (word_list):
    new_list = []
    for i in word_list:
        if i not in new_list:
            new_list.append(i)
    return(new_list)
    


#전체 XML에서 원하는 Tag 검색 --> 중복값 삭제 --> 하나의 값으로 변환

def Findall(word):
    word_list = []
    for i in root_pv.findall('.//{}'.format(word)):
        word_list.append(i.text)
    new_list = []
    for i in word_list:
        if i not in new_list:
            new_list.append(i)
    word_join = '/'.join(new_list)   
    return(word_join)

#전체 XML에서 원하는 Tag 검색 --> 총 합계 구하기

def Findall_N_Sum(word):
    word_list = []
    for i in root_pv.findall('.//{}'.format(word)):
        word_list.append(i.text)
    word_sum = sum(list(map(float, word_list)))
    return(word_sum)

#특정 Root의 하위 폴더의 Tag 검색 후 중복값 제거

def Findall_AllChild(word):
    word_list = []
    new_list = []
    root_word = root_pv.find('.//{}'.format(word))
    for i in root_word.findall('.//'):
        word_list.append(i.text)
    
    for i in word_list:
        if i not in new_list:
            new_list.append(i)
    word_join = '/'.join(new_list)   
    return(word_join)
        


# Root Level 1
root_geninfo = root_pv.find('generalVesselInfo')
root_chamber = root_pv.find('pressureChamberConditions')
root_vesselResults = root_pv.find('vesselResults')


# General Vessel Info
Item_No = root_geninfo.find('identifier').text
EQ_Type = root_geninfo.find('orientation').text
TL_TL = root_geninfo.find('tangentToTangentLength').text 
Overall_Length = root_geninfo.find('structureHeight').text

# Root Level 2 of pressureChamberConditions - Material
root_material = root_chamber.find('materials')

# pressureChamberConditions - Materials

Material = Findall_AllChild('materials')
print(Material)

# Material_Shell = root_material.find('cylinders').text
# Material_Head = root_material.find('heads').text
# Material_Support = root_material.find('support').text
# Material_Transitions = root_material.find('transitions').text

# VesselResult
Weight_Operating = root_vesselResults.find('weightOperatingNew').text
Weight_Empty = root_vesselResults.find('weightEmptyNew').text
Weight_Full_Water = root_vesselResults.find('weightTestNew').text
Volume = root_vesselResults.find('capacityNew').text
Liquid_Weight = root_vesselResults.find('liquidWeightOperatingNew').text


# Shell ID 찾기

ID = Findall('cylinder/standardComponentData/innerDiameter')

# DP DT 찾기


DP = Findall('cylinder/standardComponentData/designPressure')
DT = Findall('cylinder/standardComponentData/designTemperature')
Ext_P = Findall('cylinder/standardComponentData/externalPressure')
Ext_T = Findall('cylinder/standardComponentData/externalTemperature')

DP = DP + ' / ' + Ext_P
DT = DT + ' / ' + Ext_T

# Support Type & Height

root_support = root_pv.find('support')

for support in root_support:
    Support_Type = support.tag
    
Support_Height = Findall_N_Sum('{}'.format(Support_Type)+'/length')

# Insulation 적용 여부

Insulation = root_pv.findall('.//insulation/thickness')
Insulation_Thk = []
for i in Insulation :
    Insulation_Thk.append(i.text)

Insulation_Thk = list(set(Insulation_Thk))   # 중복값 제거 list --> set(순서 상관x, 중복x) --> list

# Platform Ladder

Platform_Total_Weight = Findall_N_Sum('platformLadder/weight')

# BM Title

Title_General = ['Item_No', 'Reqn_No', 'Unit', 'Service', 'Qty_Item', 'Qty_Set']
Title_Size = ['ID', 'TL_TL', 'Support_H']
Title_Type = ['EQ_Type', 'Support_Type']
Title_P_T = ['Design Press', 'Design_Temp']
Title_Weight = ['Wt_Erection', 'Wt_Empty', 'Wt_Operating', 'Wt_Test', 'Wt_Erection_Total']
Title_Platform = ['PF_Weight', 'PF_Weight_Total']
Title_Electric = ['Elec_Power', 'Motor Power', 'Qty']
Title_Material = ['Material_Main', 'Material_Aux']
Title_Spec = ['Overall_Length', 'SpecA', 'SpecB', 'SpecB',
              'SpecC', 'SpecC', 'SpecD', 'SpecD']
Title_Insulation = ['Ins_Sys1', 'Ins_Thk', 'Ins_Area',
                    'Ins_Sys2', 'Ins_Thk', 'Ins_Area']

# Intergrity of Title

BM_Titles = []
BM_Titles.extend(Title_General+Title_Size+Title_Type+Title_P_T+
                 Title_Weight+Title_Platform+Title_Electric+Title_Material+Title_Spec+Title_Insulation)


Item_General = [Item_No, 'INPUT!!', 'INPUT!!', 'INPUT!!', 'INPUT!!', 'INPUT!!']
Item_Size = [ID, TL_TL, Support_Height]
Item_Type = [EQ_Type, Support_Type]
Item_P_T = [DP, DT]
Item_Weight = ['INPUT!!',Weight_Empty, Weight_Operating, Weight_Full_Water, 'N/A']
Item_Electric = ['INPUT!!', 'INPUT!!', 'INPUT!!']
Item_Platform = [Platform_Total_Weight,'수기입력']
Item_Material = [Material,'INPUT!!']
Item_Spec = [Overall_Length, 'INPUT!!', 'INPUT!!', 'INPUT!!', 'INPUT!!', 'INPUT!!', 'INPUT!!', 'INPUT!!']
if len(Insulation_Thk) > 1 :
    Item_Insulation = ['INPUT!!', Insulation_Thk[0], 'INPUT!!', 'INPUT!!', Insulation_Thk[1], 'INPUT!!']
else :
    Item_Insulation = ['INPUT!!', Insulation_Thk[0], 'INPUT!!', 'INPUT!!', 'INPUT!!', 'INPUT!!']
    
# Intergrity of Item

BM_Items = []
BM_Items.extend(Item_General+Item_Size+Item_Type+Item_P_T+
                Item_Weight+Item_Platform+Item_Electric+Item_Material+Item_Spec+Item_Insulation)
print(BM_Titles)
print(BM_Items)
print('Title Column 수 : ', len(BM_Titles))
print('내용 Column 수 : ', len(BM_Items))


# Data Frame 생성

import pandas as pd
import numpy as np

BM_Items_Arr = np.array([BM_Items])

my_df = pd.DataFrame(BM_Items_Arr, columns = BM_Titles)

my_df.to_csv('{}.csv'.format(file_name), index=False, encoding='utf-8')
