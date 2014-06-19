import os

front_extra = ' data_type="4">' #Needed for parsing xml values, the front tags end
back_extra = '</'               #Needed for parsing xml values, the back tags front

#Gets the xml values from the logs
#Expects the line of text from the log, the starting <' '> tag and ending </' '> tag
def get_xml_value(line, start_tag, end_tag):
    x = line.find(start_tag)
    if x == -1:                     #Returns N/A if that tag isn't there
        return "N/A"
    x += len(start_tag + front_extra)
    y = line.find(end_tag)
    return line[x:y]

#Parses the files and pulls the desired values
def parseFiles(inputDir, parameters):
    values, count = [], []
    for file in os.listdir(inputDir):
        if file.endswith('.log'):
            print("Parsing data from file: " + file)
            inputFile = open(inputDir + file)
            lines = inputFile.readlines()       #List of lines in the file
            for line in lines:
                #Temp variable to store the values that will be reported
                values_temp = []
                #Boolean for checking if a filter has been broken
                #False = the values get reported
                #True = A filter has been broken
                broken_filter = False
                for param in parameters:
                    #The front <' '> tag
                    start_tag = param
                    #The back </' '> tag
                    end_tag = back_extra + param
                    #temp storage for the values
                    xml_value = get_xml_value(line, start_tag, end_tag)
                    #Checks to see if it gets passed the filter or there is no filter
                    for filt in parameters[param]:
                        if filt == xml_value:
                            values_temp.append(xml_value)
                        if filt[:1] == '!':
                            if filt[1:] == xml_value:
                                broken_filter = True
                            elif filt[1:] != xml_value:
                                values_temp.append(xml_value)
                    if len(parameters[param]) <= 0:
                        values_temp.append(xml_value)
                if len(values_temp) < len(parameters):
                    broken_filter = True
                if not broken_filter:
                    #Checks to see if this is a duplicate line
                    if values_temp not in values:
                        values.append(values_temp)
                        count.append(1)
                    #Adds one to count if it is
                    else:
                        index = values.index(values_temp)
                        count[index] += 1 
            inputFile.close()
    return values, count

#Parses the files for possible parameter types
def checkFilesForParameters(inputDir):
    possible_params = []
    for file in os.listdir(inputDir):
        if file.endswith('.log'):
            inputfile = open(inputDir + file)
            #List that holds all the lines in the file
            lines = inputfile.readlines()
            #temp variable to hold a place in a line so we progress through the line
            lastindex = 0
            for line in lines:
                while lastindex != -1:
                    #Where the last item was
                    lastindex = line.find(back_extra, lastindex)
                    #Next items first <' '>
                    fbracket = int(line.find(back_extra, lastindex)) + 2
                    #Next items second </' '>
                    sbracket = int(line.find('>', lastindex))
                    #Break if there are no more values
                    if sbracket == -1:
                        break
                    param = line[fbracket:sbracket]
                    #No duplicates
                    if param not in possible_params:
                        possible_params.append(param)
                    lastindex+=1
            inputfile.close()
    #These variable break or are specified through another cmdline argument
    for param in ["Timestamp", "User-Name", "Event"]:
        possible_params.remove(param)
    return possible_params
