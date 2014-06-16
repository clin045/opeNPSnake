import os, sys, getopt
import htmlReportGen

parameters = []         #Parameters input by users
possible_params = []    #Possible parameters they could input

outputDir, inputDir = '', ''

front_extra = ' data_type="4">'
back_extra = '</'

values, count = [], []
filters = []

start_time, end_time = "", ""

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
    -p Select parameters for parsing [-p arg1,arg2,arg3]
    -c TODO Specifies config file
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

#Parses the log files
def parseFiles():
    for file in os.listdir(inputDir):
        if file.endswith('.log'):
            print("Parsing data from file: " + file)
            inputfile = open(inputDir + file)
            lines = inputfile.readlines()
            for line in lines:
                params_temp = []
                #Variable for if a filter is broken
                #False = no filters broken and the content should be added to the report
                broken_filter = False       
                for param in parameters:
                    start_tag = param
                    end_tag = back_extra + param
                    xml_value = get_xml_value(line, start_tag, end_tag)
                    index = parameters.index(param)
                    #Filter checking
                    if xml_value == filters[index] or filters[index] == "":
                        params_temp.append(xml_value)
                    else:
                        broken_filter = True
                #Adds it to the content for the report
                if not broken_filter:
                    if params_temp not in values:
                        values.append(params_temp)
                        count.append(1)
                    else:
                        index = values.index(params_temp)
                        count[index] += 1 
            inputfile.close()

#Parses the files for possible parameter types
def checkFilesForParameters():
    for file in os.listdir(inputDir):
        if file.endswith('.log'):
            inputfile = open(inputDir + file)
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
    for param in ["Timestamp", "User-Name", "Event"]:
        possible_params.remove(param)
    
#Returns a reformatted folder path
def getFolderPath(path):
    temp = path.replace('\\', '/')
    if temp[-1:] != "/":
        temp += "/"
    return temp
    
#Get the user's parameters
def getParameters(params):
    checkFilesForParameters()
    for p in params:
        p = p.lower().replace(' ','-').title()          #Puts it in the format readable by logs
        if p not in parameters and p in possible_params:
            parameters.append(p)
        elif p not in possible_params:
            print(p + " isn't a valid parameter")
    
def main():
    global filters
    global outputDir, inputDir
    #get the cmd line options
    try:
        opts, args = getopt.getopt(sys.argv[1:],'hi:o:Pp:t:')
    except:
        print(helpfile)
    #do stuff based on options
    for opt, arg in opts:
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
            global filters
            params = []
            params = arg.split(',')
            paramlst = []
            filterlst = []
            for p in params:
                paramlst.append(p.split(':')[0])
                try:
                    filterlst.append(p.split(':')[1])
                except:
                    filterlst.append('')
            filters = filterlst
            getParameters(paramlst)
        #specifies the time frame
        elif opt == '-t':
            times = arg.split(',')
            start_time = convertTime(times[0])
            end_time = convertTime(times[1])
                
            
    parseFiles()
    if outputDir == '':
        htmlReportGen.generate(values, parameters, count)
    else:
        htmlReportGen.generate(values, parameters, count, outputDir)

            
if __name__ == '__main__':
    main()
