import os, sys, getopt, configparser
import htmlReportGen


possible_params = []            #Possible parameters they could input
parameters = {}                 #Dictionary that holds the parameters:their filters

outputDir, inputDir = '', ''    #Folder where to report, folder where logs are

front_extra = ' data_type="4">' #Needed for parsing xml values, the front tags end
back_extra = '</'               #Needed for parsing xml values, the back tags front

values, count = [], []          #Values holds the lines in the report
                                #Count is how many times an identical line appeared


start_time, end_time = "", ""   #Start and end time frames given by user

#When -h is called or the user doesn't do something right
helpfile="""
               ,   .,---.,---.          |         
,---.,---.,---.|\  ||---'`---.,---.,---.|__/ ,---.
|   ||   ||---'| \ ||        ||   |,---||  \ |---'
`---'|---'`---'`  `'`    `---'`   '`---^`   ``---'
     |

Parses NPS logs and generates useful reports

Usage: python opeNPSnake.py -i "filepath" [options]

Options:
    -h Prints out this help file
    -i Input file/directory (YOU MUST QUOTE THE FILE PATH)
    -o Output directory (Defaults to the current working directory)
    -P Prints list of log parameterss
    -p Select parameters for parsing [-p arg1:filter1,arg2:filter2:filter3,arg3]
    -c Specifies config file (see sample.conf)
    -t Specify the time frame [-t "* * * * *,* * * * *"] Minute, Hour, Day, Month, Year

Note: Fully-Qualifed-User-Names is not spelled correctly in the logs.
     
"""

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
def parseFiles():
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
                    if xml_value in parameters[param] or len(parameters[param]) <= 0:
                        values_temp.append(xml_value)
                    else:
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

#Parses the files for possible parameter types
def checkFilesForParameters():
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

#Returns a reformatted folder path
def getFolderPath(path):
    #Replace the \ slashes with / so we don't get unicode errors
    temp = path.replace('\\', '/')
    #Add a / to the end if there isn't one
    if temp[-1:] != "/":
        temp += "/"
    return temp

#Checks the parameters that the user specified and drops the ones that
#Aren't in the logs
def getParameters(params):
    checkFilesForParameters()
    global parameters
    for p in params:
        if p not in parameters and p in possible_params:
            parameters[p] = params[p]
        else:
            print(p + " is not a valid parameter")
            
#loads config file
def loadConf(loc):
    loc = loc.replace('\\', '/')
    c = configparser.ConfigParser()
    c.read(loc)
    section='Config'
    options=c.options(section)
    global inputDir,outputDir
    paramlst = {}
    for o in options:
        if o == 'parameters':
            arg = c.get(section,o)
            params = arg.split(',')
            for p in params:
                filterlst=[]
                try:
                    filterlst=p.split(':')[1:]
                except:
                    filterlst.append('')

                paramlst[p.split(':')[0].lower().replace(' ', '-').title()]=filterlst
        if o == 'input':
            print(c.get(section,o))
            inputDir = getFolderPath(c.get(section,o))
        if o == 'output':
            print(c.get(section,o))
            outputDir = getFolderPath(c.get(section,o))
    getParameters(paramlst)
#Main
#We should probably split this up but whatever
def main():
    global filters
    global outputDir, inputDir
    global start_time, end_time
    #get the cmd line options
    #try:
    opts, args = getopt.getopt(sys.argv[1:],'hi:o:Pp:t:c:')
    #except:
    #    print(helpfile)
    #do stuff based on options
    for opt, arg in opts:
        paramlst = {}
        #print help file
        if opt == '-h':
            print(helpfile)
        #get input directory
        elif opt == '-i':
            inputDir = getFolderPath(arg)
        #get output directory
        elif opt == '-o':
            outputDir = getFolderPath(arg)
        #prints out list of parameters
        elif opt == '-P':
            checkFilesForParameters()
            print()
            for param in possible_params:
                print(param.replace("-", " "))
        #selects parameters for parsing
        elif opt == '-p':
            params = arg.split(',')
            for p in params:
                filterlst=[]
                try:
                    filterlst=p.split(':')[1:]
                except:
                    filterlst.append('')

                paramlst[p.split(':')[0].lower().replace(' ', '-').title()]=filterlst

            
        #specifies the time frame
        elif opt == '-t':
            times = arg.split(',')
        #Load parameters/filters from a config file
        elif opt == '-c':
            loadConf(arg)
    #Make sure they specified a -p parameter
    getParameters(paramlst)
    if len(parameters) > 0:
        parseFiles()
        #Generating the reports
        #If there wasn't a specified outputDir we just use the default(cwd)
        if outputDir == '':
            htmlReportGen.generate(values, parameters, count)
        else:
            htmlReportGen.generate(values, parameters, count, outputDir)

    else:
        print(helpfile)
        print("You did not specify any parameters")

            
if __name__ == '__main__':
    main()
