from pymongo import MongoClient
import json
client = MongoClient()

client = MongoClient('localhost', 27017)

mydb = client["Project2"]
employeeData = mydb["Employee"]
departmentData = mydb["Department"]
projectData = mydb["Project"]
worksOn = mydb["Works_On"]
resultCollection = mydb["PROJECT_DATA"]

finalResult_1 = []



def part1_query():
  for project in projectData.find():
      dict = {}
      # project data
      dict["Project_Name"] = project["ProjectName"]
      dict["Project_Number"] = project["ProjectNumber"]

      #Department Name
      Dno = project["DepartmentNumber"]
      dict["Department_Name"]= getDeptName(Dno)

      # Employee works on project Data
      ProNo = project["ProjectNumber"]
      dict["Employees"] = getEmployee(ProNo)     
      finalResult_1.append(dict) 

def getDeptName(Dno):
    for dnumber in departmentData.find():
        if dnumber["DepartmentNumber"] == Dno:
            return dnumber["DepartmentName"]
            
def getEmployee(ProNo):
    employeeList=[]
    for pronumber in worksOn.find():
        employeedict={}
        if pronumber["ProjectNumber"] == ProNo:
            ssnQuery = { "SSN" : pronumber["EmployeeSSN"]}
            ssnResult = employeeData.find(ssnQuery)
            for ssn in ssnResult:
                employeedict["LName"] = ssn["LName"]
                employeedict["FName"] = ssn["FName"]
            employeedict["Hours"] = pronumber["ProjectHours"]
            employeeList.append(employeedict)
    return employeeList


print(" ")
print("------ Initation Join Operation for Project2 Part1 query ------")
part1_query()
print("------ Join Operation Complete ------")
print(" ")
print("------ Running the Query and Inserting into MongoDb ------")
resultCollection.insert_many(finalResult_1)
print("------ PROJECT_DATA collection created in mongoDB ------")
print(" ")