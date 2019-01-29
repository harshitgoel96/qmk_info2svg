import svgwrite
import http.client
import json 

BASE_KEY_WIDTH=20
BASE_KEY_HEIGHT=20

def createSvgForLayout(layoutName,layoutArray):
    dwg = svgwrite.Drawing("{}.svg".format(layoutName))
    for keyItem in layoutArray:
       keyItemWidthMultiplier=keyItem.get("w",1)
       keyItemHeighthMultiplier=keyItem.get("h",1)
       dwg.add(dwg.rect((keyItem["x"]*BASE_KEY_WIDTH,keyItem["y"]*BASE_KEY_HEIGHT),(keyItemWidthMultiplier*BASE_KEY_WIDTH,keyItemHeighthMultiplier*BASE_KEY_HEIGHT), stroke='red', stroke_width=1))
    dwg.save()
connection = http.client.HTTPSConnection("api.qmk.fm")
connection.request("GET", "/v1/keyboards/ergodone")
response = connection.getresponse()
print("Status: {} and reason: {}".format(response.status, response.reason))
data=json.loads(response.read().decode())

connection.close()

listOfKeys=data["keyboards"].keys()
for key in listOfKeys:
    keebLayouts=data["keyboards"][key]["layouts"].keys()  
    for layout in keebLayouts:
        #print("===========\n{}\n{}\n".format(layout,data["keyboards"][key]["layouts"][layout]['layout']))
        createSvgForLayout(layout,data["keyboards"][key]["layouts"][layout]['layout'])
    
print("end")