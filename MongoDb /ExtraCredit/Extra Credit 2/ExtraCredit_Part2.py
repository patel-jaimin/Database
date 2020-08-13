from pymongo import MongoClient
import json
client = MongoClient()

client = MongoClient('localhost', 27017)

mydb = client["Project2"]
employeeData = mydb["Employee"]
departmentData = mydb["Department"]
resultCollection = mydb["DEPARTMENT_DATA"]

finalResult_1 = []

def ExtraCredit_part2():
    for department in departmentData.find():
      dict = {}
      # project data
      dict["Dep_Name"] = department["DepartmentName"]
      dict["Dep_Number"] = department["DepartmentNumber"]

      # Manager Last Name and First Name.  
      mgr_ssn = department["Manager_SSN"]
      dict["MGR_Lname"],dict["MGR_Fname"] = getName(mgr_ssn)

      # Employee works on specific Department.  
      dno = department["DepartmentNumber"]
      dict["EmpWorksForDept"] = getEmployee(dno)
      finalResult_1.append(dict)


def getName(mgr_ssn):
    ssnQuery = { "SSN" : mgr_ssn }
    ssnResult = employeeData.find(ssnQuery)
    for mngr_ssn in ssnResult:
        return mngr_ssn["LName"],mngr_ssn["FName"] 

def getEmployee(dno):
    employeeList=[]
    for employee in employeeData.find():
        employeedict={}
        if employee["DNo"] == dno:
            employeedict["Lname"] = employee["LName"]
            employeedict["Fname"] = employee["FName"]
            employeedict["Salary"] = employee["Salary"]
            employeeList.append(employeedict)
    return employeeList

print(" ")
print("------ Initation Join Operation------")
ExtraCredit_part2()
print("------ Join Operation Complete ------")
print(" ")
print("------ Running the Query and Inserting into MongoDb ------")
resultCollection.insert_many(finalResult_1)
print("------ DEPARTMENT_DATA collection created in mongoDB ------")
print(" ")