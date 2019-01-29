import svgwrite
import http.client
import json 

BASE_KEY_WIDTH=19.05
BASE_KEY_HEIGHT=19.05

def createSvgForLayout(layoutName,layoutArray):
    dwg = svgwrite.Drawing("{}.svg".format(layoutName))
    defaultRx=0
    defaultRy=0
    for keyItem in layoutArray:
        keyItemWidthMultiplier=keyItem.get("w",1)
        keyItemHeighthMultiplier=keyItem.get("h",1)
        keyRotation=keyItem.get("r",0)
        defaultRx=keyItem.get("rx",defaultRx)
        defaultRy=keyItem.get("ry",defaultRy)
        if keyRotation!=0:
           dwg.add(dwg.rect((keyItem["x"]*BASE_KEY_WIDTH,keyItem["y"]*BASE_KEY_HEIGHT),(keyItemWidthMultiplier*BASE_KEY_WIDTH,keyItemHeighthMultiplier*BASE_KEY_HEIGHT), 
                stroke='red', 
                stroke_width=1,
                transform="rotate({} {} {})".format(
                        keyRotation,
                        defaultRx*BASE_KEY_WIDTH,
                        defaultRy*BASE_KEY_HEIGHT)
           ))
           
        else:
            dwg.add(dwg.rect(
                (keyItem["x"]*BASE_KEY_WIDTH,keyItem["y"]*BASE_KEY_HEIGHT),
                (keyItemWidthMultiplier*BASE_KEY_WIDTH,keyItemHeighthMultiplier*BASE_KEY_HEIGHT), stroke='red', stroke_width=1))
    dwg.save()
#connection = http.client.HTTPSConnection("api.qmk.fm")
#connection.request("GET", "/v1/keyboards/ergodone")
#response = connection.getresponse()
#print("Status: {} and reason: {}".format(response.status, response.reason))
#data=json.loads(response.read().decode())

#connection.close()
with open('info.json', encoding='utf-8') as data_file:
    data = json.loads(data_file.read())
print(data)
listOfKeys=data["keyboards"].keys()
for key in listOfKeys:
    keebLayouts=data["keyboards"][key]["layouts"].keys()  
    for layout in keebLayouts:
        #print("===========\n{}\n{}\n".format(layout,data["keyboards"][key]["layouts"][layout]['layout']))
        createSvgForLayout(layout,data["keyboards"][key]["layouts"][layout]['layout'])
    
print("end")