Python 3.9.13 (tags/v3.9.13:6de2ca5, May 17 2022, 16:36:42) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> 


####################################################
#$$$$$$$$$$$$ Creare new Shot Id Sg $$$$$$$$$$$$$$$$

import shotgun_api3
# ShotGrid server and auth credentials.

SERVER_PATH = "https://.shotgrid.autodesk.com"
SCRIPT_NAME = 'pipeline'
SCRIPT_KEY =  'utakzicH#prwwmcd3dmtekumo'

# Main

sg = shotgun_api3.Shotgun("https://.shotgrid.autodesk.com",script_name="pipeline",api_key="utakzicH#prwwmcd3dmtekumo",http_proxy="10.10.4.121:3128")

# Shot with data

data = {
        'project': {"type":"Project","id": 70},
        'code': '10_010',
        'description': 'Demon test',
        'sg_status_list': 'ip'
    }
result = sg.create('Shot', data)
print("The id of the {} is {}.".format(result['type'], result['id']))

###############################################################
#$$$$$$$$$$$$$$ Shot Find In Sg $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

import shotgun_api3
# ShotGrid server and auth credentials.

SERVER_PATH = "https://.shotgrid.autodesk.com"
SCRIPT_NAME = 'pipeline'
SCRIPT_KEY =  'utakzicH#prwwmcd3dmtekumo'

# Main

sg = shotgun_api3.Shotgun("https://.shotgrid.autodesk.com",script_name="pipeline",api_key="utakzicH#prwwmcd3dmtekumo",http_proxy="10.10.4.121:3128")

# Shot with data

data = {
        'project': {"type":"Project","id": 70},
        'code': 'ast',
        'description': 'Demon test',
        'sg_status_list': 'ip'
    }
result = sg.create('Shot', data)

print(result)
fields = ["sg_sequence","entity","step","content","sg_status_list"]
filters = [['id', 'is',4389]]
result = sg.find('Task', filters,fields)
print(result)

###############################################################################

#$$$$$$$$$$$ Shot Find in Singl Deperement [Under Task Group] $$$$$$$$$$$$$

import shotgun_api3
# ShotGrid server and auth credentials.

SERVER_PATH = "https://.shotgrid.autodesk.com"
SCRIPT_NAME = 'pipeline'
SCRIPT_KEY =  'utakzicH#prwwmcd3dmtekumo'

# Main

sg = shotgun_api3.Shotgun("https://.shotgrid.autodesk.com",script_name="pipeline",api_key="utakzicH#prwwmcd3dmtekumo",http_proxy="10.10.4.121:3128")

# Shot with data

taskFilter = { 'project': {"type":"Project","id": 70},}

fields = ["id","sg_sequence","entity","step","content","sg_status_list"]
filters = [['step.Step.code', 'in',"Light"]]
result = sg.find('Task', filters,fields)
print(result)


##############################################################
#$$$$$$ finde Shots and user info [Under Version Group]$$$$$$$

import shotgun_api3

# ShotGrid server and auth credentials.

SERVER_PATH = "https://.shotgrid.autodesk.com"
SCRIPT_NAME = 'pipeline'
SCRIPT_KEY =  'utakzicH#prwwmcd3dmtekumo'

# Main

sg = shotgun_api3.Shotgun("https://.shotgrid.autodesk.com",script_name="pipeline",api_key="utakzicH#prwwmcd3dmtekumo",http_proxy="10.10.4.121:3128")



fields = ['user','sg_path_to_frames','sg_path_to_frames__for_qc']
filters = [['sg_status_list', 'is',"pcr"]]
result = sg.find('Version', filters,fields)
print(result)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#
import shotgun_api3
# ShotGrid server and auth credentials.

SERVER_PATH = "https://.shotgrid.autodesk.com"
SCRIPT_NAME = 'pipeline'
SCRIPT_KEY =  'utakzicH#prwwmcd3dmtekumo'
PROXY_SERVER="10.10.4.121:3128"

# Main

sg = shotgun_api3.Shotgun(SERVER_PATH,script_name=SCRIPT_NAME,api_key=SCRIPT_KEY,http_proxy=PROXY_SERVER)

# Shot with data

fields = ["id",'code']
filters = [['code', 'is','bunny_010_0020']]
result = sg.find('Shot', filters,fields)
print(result)

fields = ["sg_sequence","entity","step","content","sg_status_list"]
filters = [['entity', 'is',result]]
result = sg.find('Task', filters,fields)
print(result)

########################################
#get all the tasks under project name 'dev_project'  which is in 'In Progress' status

print(sg.find("Project",[["id","is",70]],["id"]))

taskFilter = { 'project': {"type":"Project","id": 70},}
fields = ['id',"content","entity"]
filters = [["project","is",{'type': 'Project', 'id': 70}],["sg_status_list","is","ip"]]

# print(('Task', filters,fields))
result = sg.find('Task', filters,fields)
print(len(result) )

SyntaxError: invalid syntax
>>> 
