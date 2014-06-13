#get file input                             -
#get what parameters they want              -
#find data
#store in list
#generate report

#test_folder = C:\Users\jeramy.lochner\Desktop\NPSLogFile

import os
import htmlReportGen

parameters = []         #Parameters input by users
possible_params = []    #Possible parameters they could input
folder = ""             #Folder where logs are located

front_extra = ' data_type="4">'
back_extra = '</'
values = []


def get_xml_value(line, start_tag, end_tag):
    x = line.find(start_tag)
    if x == -1:
        return "N/A"
    x += len(start_tag + front_extra)
    y = line.find(end_tag)
    return line[x:y]


def parseFiles():
    for file in os.listdir(folder):
        if file.endswith('.log'):
            print("Parsing data from file: " + file)
            inputfile = open(folder + file)
            lines = inputfile.readlines()
            for line in lines:
                params_temp = []
                for param in parameters:
                    start_tag = param
                    end_tag = back_extra + param
                    params_temp.append(get_xml_value(line, start_tag, end_tag))
                if params_temp not in values:
                    values.append(params_temp)
                    print(params_temp)
            inputfile.close()
                    
def checkFilesForParameters():
    for file in os.listdir(folder):
        if file.endswith('.log'):
            print("Checking file: " + file + " for possible parameter types")
            inputfile = open(folder + file)
            lines = inputfile.readlines()
            lastindex = 0
            for line in lines:
                while lastindex != -1:
                    lastindex = line.find(back_extra, lastindex)
                    fbracket = int(line.find(back_extra, lastindex)) + 2
                    sbracket = int(line.find('>', lastindex))
                    if sbracket == -1:
                        break
                    param = line[fbracket:sbracket]
                    if param not in possible_params:
                        possible_params.append(param)
                    lastindex+=1
            inputfile.close()
    print("\n"*100)
    
def getFolderPath():
    global folder
    temp = input("Enter the folder path where the logs are stored.\n").replace('\\', '/')
    if temp[-1:] != "/":
        temp += "/"
    folder = temp

def getParameters():
    user_input = ""
    for param in possible_params:
        print("\t" + param)
    print("\n\n")
    print("Fully-Qualifed-User-Names is not spelled correctly in the logs\nSpell it as it is spelled here\n")
    while user_input != 'done':
        user_input = input("Enter a parameter you would like to grab\nType 'done' when done\n\t")
        if user_input not in parameters and user_input in possible_params:
            parameters.append(user_input)
        elif user_input not in possible_params and user_input != 'done':
            print("That isn't a valid parameter")
    print("\n"*100)



getFolderPath()
checkFilesForParameters()
getParameters()
parseFiles()
htmlReportGen.generate(values, parameters)
    
