from xml.etree import ElementTree
from xml.dom import minidom
from datetime import datetime
from lxml import etree
import random, string, datetime, os.path, os, glob, SetVariables
import xml.etree.ElementTree as ET


#Generates random string of Uppercase letters and digits with the length equal to the parameter stringLength
def randomString(stringLength):
    try:
        possibleChars = string.ascii_uppercase + string.digits
        result = ''.join(random.choice(possibleChars) for i in range(stringLength))
        return result
    except:
        print("Not a valid input")

#Generates random number with the number length equal to the parameter numLength
def randomNumber(numLength):
    try:
        result = ''.join(random.choice(string.digits) for i in range(numLength))
        return result
    except:
        print("Not a valid input")

#Returns the current date and time in the format M/D/Y H:M:S
def getDateTime():
    current = datetime.datetime.now()
    result = current.strftime("%m/%d/%Y %H:%M:%S")
    return result

#Method to generate a attribute with a random value
def GenerateAttrib(attributes):
    try:
        if(type(attributes) != dict):
            raise TypeError("Parameter was not valid dict")
        newAttributes = attributes

        #For each attribute in the list, set the value to be a random value
        for attrib in newAttributes:
            attributes[attrib] = GenerateRandomValue(attributes[attrib])
        if("SecTyp" in attributes):
            attributes["SecTyp"] = "9CF"

    #Return the new Attributes with random values
        return newAttributes
    except:
        print("Not a valid input")

#Method to generate random value of the same type as the provided value
def GenerateRandomValue(value):
    try:
        #Checks to see if the value is a float
        float(value)
        #Returns random number with length equal to that of the provided value
        return randomNumber(len(value))
    except ValueError:
        pass
    try:
        #Checks if the value is a date or time
        datetime.datetime.strptime(value,"%m/%d/%Y %H:%M:%S")
        #Returns current date and time
        return getDateTime()
    except ValueError:
        #Returns random string of the same length as the provided value
        return randomString(len(value))

# Method to format the element tree
def prettify(elem):
    try:
        elemString = ElementTree.tostring(elem, 'utf-8')
        reparsedElem = minidom.parseString(elemString)
        return '\n'.join([line for line in reparsedElem.toprettyxml(indent=' '*2).split('\n') if line.strip()])
    except:
        print("Not a valid input")

# Method to Generate files based on a provided sample file
def GenerateFiles(sourceFile):
    try:
        #Parses the sample XML file to an element tree
        tree = ET.parse(sourceFile)
        # For each attribute in the element tree, generates a random value
        for elem in tree.iter():
            elem.attrib = GenerateAttrib(elem.attrib)
        # parser = etree.XMLParser(remove_blank_text=True)
        # for elem in tree.iter():
        #     xmlstr = ElementTree.tostring(elem, encoding = "utf8", method="xml")
        #     elem = etree.XML(xmlstr, parser=parser)
        # Gets the root of the new element tree
        root = tree.getroot()
    except:
        print("Incompatible File")
    filepath = SetVariables.GeneratedFilesLocation
    filename = "FiXMLSample"
    try:
        #Gets the current number of generated files in the directory
        numberOfFiles = len(glob.glob(filepath + "*.xml"))
    except:
        #Sets the number of files to 0
        numberOfFiles = 0

    try:
        #Creates the complete file name so that it can be saved
        completeName = os.path.join(filepath, filename + str(numberOfFiles + 1) + ".xml")
        #Creates the directory if it does not exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        #Writes the XML file
        with open(completeName, "w") as newFile:
            newFile.write(prettify(root))
    except:
        print(Exception)

