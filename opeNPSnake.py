#get file input
#get what parameters they want
#find data
#store in list
#generate report
parameters = []

def getParameters():
    user_input = ""
    while user_input != 'done':
        user_input = input("Enter a parameter you would like to grab\nType 'done' when done\n\t")
        if user_input not in parameters:
            parameters.append(user_input)



getParameters()
print(parameters)
