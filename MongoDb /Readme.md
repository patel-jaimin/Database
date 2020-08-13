## Project2 Repository Summer 2020 

### This Project was part of Database models and Implementation Techniques coursework in UTA under Prof Ramirez Elmasari.

#### Problem Statement ####

The input to your program will be data files in flat relational format (text files in .csv format - comma separated values) 
for the COMPANY database from the textbook. The schemas for this data are the same as for the COMPANY database in the textbook
in chapters 5 and 6 for the tables DEPARTMENT, EMPLOYEE, PROJECT, AND WORKS_ON. You will need to design two document (complex object) 
schemas corresponding to this data and store each as a document collection in MongoDB:


1) The PROJECTS document collection will store a collection of PROJECT documents.
Each PROJECT document will include the following data about each PROJECT object (document):
PNAME, PNUMBER, DNAME (for the controlling DEPARTMENT), and a collection of the workers (EMPLOYEES) who work on the project.
This will be nested within the PROJECT object (document) and will include for each worker: EMP_LNAME, EMP_FNAME, HOURS.

2) The EMPLOYEES document collection will store a collection of EMPLOYEE documents.
Each EMPLOYEE document will include the following data about each EMPLOYEE object (document):
EMP_LNAME, EMP_FNAME, DNAME (department where the employee works), and a collection of the projects that the employee works on.
This will be nested within the EMPLOYEE object (document) and will include for each project: PNAME, PNUMBER, HOURS.
