from pymongo import MongoClient
import json
client = MongoClient()

client = MongoClient('localhost', 27017)

mydb = client["Project2"]
employeeData = mydb["Employee"]
departmentData = mydb["Department"]
projectData = mydb["Project"]
worksOn = mydb["Works_On"]
resultCollection = mydb["EMPLOYEES_DATA"]

finalResult_1 = []



def part2_query():
  for employee in employeeData.find():
      dict = {}
      dict["Emp_Lname"] = employee["LName"]
      dict["Emp_Fname"] = employee["FName"]
      #Department Name
      Dno = employee["DNo"]
      dict["Department_Name"]= getDeptName(Dno)

      #All Projects that Employee works on
      ssn = employee["SSN"]
      dict["Projects"] = getProjects(ssn)  
        
      finalResult_1.append(dict)


def getDeptName(Dno):
    for dnumber in departmentData.find():
        if dnumber["DepartmentNumber"] == Dno:
            return dnumber["DepartmentName"]
  
def getProjects(ssn):
    projectList=[]
    for essn in worksOn.find():
        projectdict={}
        if essn["EmployeeSSN"] == ssn:
            projectQuery = { "ProjectNumber" : essn["ProjectNumber"]}
            projectResult = projectData.find(projectQuery)
            for project in projectResult:
                projectdict["ProjectName"] = project["ProjectName"]
                projectdict["ProjectNumber"] = project["ProjectNumber"]
            projectdict["Hours"] = essn["ProjectHours"]
            projectList.append(projectdict)
    return projectList

print(" ")
print("------ Initation Join Operation for Project2 Part2 query ------")
part2_query()
print("------ Join Operation Complete ------")
print(" ")
print("------ Running the Query and Inserting into MongoDb ------")
resultCollection.insert_many(finalResult_1)
print("------ EMPLOYEES_DATA collection created in mongoDB ------")
print(" ")