#get file input                             -
#get what parameters they want              -
#find data                                  -
#store in list                              -
#generate report                            -

#test_folder = C:\Users\jeramy.lochner\Desktop\NPSLogFile

import os
import htmlReportGen

parameters = []         #Parameters input by users
possible_params = []    #Possible parameters they could input
folder = ""             #Folder where logs are located

front_extra = ' data_type="4">'         #The extras included at the end of every opening tag i.e i.e '<Computer-Name data_type="4">'
back_extra = '</'                       #The extras included at the beginning of every closing tag i.e '</Computer-Name>
values = []


# Grab the values from <''> </''> tags
# Parameters: The line of text, the <''>, and the </''>
# Helper class for parseFiles()
def get_xml_value(line, start_tag, end_tag):
    x = line.find(start_tag)            # Get index of start_tag
    if x == -1:                         # Return N/A if not there
        return "N/A"
    x += len(start_tag + front_extra)   # Get index of the end of the start tag + extra stuff
    y = line.find(end_tag)              # Get index of the end_tag
    return line[x:y]                    # Return the value between the tags

# Get the values based on which parameters were chosen
def parseFiles():
    for file in os.listdir(folder):     
        if file.endswith('.log'):       
            print("Parsing data from file: " + file)
            inputfile = open(folder + file)
            lines = inputfile.readlines()
            for line in lines:
                params_temp = []                    # Init a temporary list
                for param in parameters:            # For every parameter in the chosen parameters
                    start_tag = param
                    end_tag = back_extra + param    # Put the extras for the end_tag in front since they are ahead of the parameter
                    params_temp.append(get_xml_value(line, start_tag, end_tag))
                if params_temp not in values:       # If it isn't in the list of values already
                    values.append(params_temp)
            inputfile.close()                       # Close the opened file

# Get all the possible parameters from the files

def checkFilesForParameters():
    for file in os.listdir(folder):
        if file.endswith('.log'):
            print("Checking file: " + file + " for possible parameter types")
            inputfile = open(folder + file)
            lines = inputfile.readlines()
            lastindex = 0           # Init a temp var to hold where you are in the line
            for line in lines:
                while lastindex != -1:
                    lastindex = line.find(back_extra, lastindex)            # Find the front of the next end_tag
                    fbracket = int(line.find(back_extra, lastindex)) + 2    # Get index of the front of the next end_tag
                    sbracket = int(line.find('>', lastindex))               # Get index of the back of the next end_tag
                    if sbracket == -1:                                      # Break if there are no more end tags
                        break
                    param = line[fbracket:sbracket]                         # Get value between </ and >
                    if param not in possible_params:                        # Check to see if it's already included, don't want dupes
                        possible_params.append(param)                       
                    lastindex+=1
            inputfile.close()
    print("\n"*100)

# Gets user input of what folder it's in
def getFolderPath():
    global folder
    temp = input("Enter the folder path where the logs are stored.\n").replace('\\', '/')
    if temp[-1:] != "/":        #Append a final '/'
        temp += "/"
    folder = temp

# Gets user input on what parameters they want in the report
def getParameters():
    user_input = ""
    for param in possible_params:
        print("\t" + param.replace("-", " "))
    print("\n\n")
    print("Fully-Qualifed-User-Names is not spelled correctly in the logs\nSpell it as it is spelled here\n")
    while user_input != 'Done':
        user_input = input("Enter a parameter you would like to grab\nType 'done' when done\n\t").lower().replace(" ", "-").title()
        print(user_input)
        if user_input not in parameters and user_input in possible_params:
            parameters.append(user_input)
        elif user_input not in possible_params and user_input != 'Done':
            print("That isn't a valid parameter")
    print("\n"*100)


def main():
    getFolderPath()
    checkFilesForParameters()
    getParameters()
    parseFiles()
    htmlReportGen.generate(values, parameters)
    
if __name__ == '__main__':
    main()
