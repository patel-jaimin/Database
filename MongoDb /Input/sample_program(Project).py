import json

# the file to be converted
filename = 'PROJECT.txt'

# resultant dictionary
dict1 = []

# fields in the sample file
fields =['ProjectName', 'ProjectNumber', 'ProjectLocation', 'DepartmentNumber']




with open(filename) as fh:

    for line in fh:

        # reading line by line from the text file
        my_list = list( line.strip().split(','))
        description = [x.replace("'",'') for x in my_list]

        # for output see below
        print(description)

        # loop variable
        i = 0
        # intermediate dictionary
        dict2 = {}
        while i<len(fields):

                # creating dictionary 
                dict2[fields[i]]= description[i]
                i = i + 1

        dict1.append(dict2)
        


# creating json file
out_file = open("Project.json", "w")
json.dump(dict1, out_file, indent = 4)
out_file.close()
