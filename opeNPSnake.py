import os, sys, getopt
import htmlReportGen


possible_params = []    #Possible parameters they could input
parameters = {}

outputDir, inputDir = '', ''

front_extra = ' data_type="4">'
back_extra = '</'

values, count = [], []


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
    -p Select parameters for parsing [-p arg1:filter1,arg2:filter2:filter3,arg3]
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

def parseFiles():
    for file in os.listdir(inputDir):
        if file.endswith('.log'):
            print("Parsing data from file: " + file)
            inputFile = open(inputDir + file)
            lines = inputFile.readlines()
            for line in lines:
                params_temp = []
                broken_filter = False
                for param in parameters:
                    start_tag = param
                    end_tag = back_extra + param
                    xml_value = get_xml_value(line, start_tag, end_tag)

                    if xml_value in parameters[param] or len(parameters[param]) <= 0:
                        params_temp.append(xml_value)
                    else:
                        broken_filter = True
                if not broken_filter:
                    if params_temp not in values:
                        values.append(params_temp)
                        count.append(1)
                    else:
                        index = values.index(params_temp)
                        count[index] += 1
            inputFile.close()

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

def getParameters(params):
    checkFilesForParameters()
    global parameters
    for p in params:
        p = p.lower().replace(' ', '-').title()
        if p not in parameters and p in possible_params:
            parameters[p] = params[p]
        else:
            print(p + " is not a valid parameter")

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
            params = []
            params = arg.split(',')
            paramlst = {}
            filterlst = []
            for p in params:
                filterlst=[]
                try:
                    filterlst=p.split(':')[1:]
                except:
                    filterlst.append('')
                paramlst[p.split(':')[0]]=filterlst
            print(paramlst)
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
