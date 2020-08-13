import sys
import json as j
import lxml.etree as e
from json2xml import json2xml
from json2xml.utils import readfromjson
sys.stdout = open("Test_Query.xml", "w")
with open("Employee.json") as json_format_file:
  d={}
  d = j.load(json_format_file)
  print(json2xml.Json2xml(d, wrapper="all", pretty=True, attr_type= True).to_xml())
  sys.stdout.close()
  
