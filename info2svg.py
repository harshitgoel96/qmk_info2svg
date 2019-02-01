import svgwrite
import http.client
import json 

#define 1u value
BASE_KEY_UNIT=20

#define key margin
BASE_KEY_MARGIN=4

#should rotation values be considered or not
ROTATION_ENABLE=False

def createSvgForLayout(layoutName,layoutArray,sizeX,sizeY):
    dwg = svgwrite.Drawing("{}.svg".format(layoutName),size=('{}mm'.format(sizeX*BASE_KEY_UNIT), '{}mm'.format(sizeY*BASE_KEY_UNIT)), viewBox=('0 0 {} {}'.format(sizeX*BASE_KEY_UNIT,sizeY*BASE_KEY_UNIT)))
    defaultRx=0
    defaultRy=0
    for keyItem in layoutArray:
        keyItemWidthMultiplier=keyItem.get("w",1)
        keyItemHeighthMultiplier=keyItem.get("h",1)
        keyRotation=keyItem.get("r",0)
        defaultRx=keyItem.get("rx",defaultRx)
        defaultRy=keyItem.get("ry",defaultRy)
        stdLayout=keyItem.get("label","A")
        if keyRotation!=0 and ROTATION_ENABLE:
           dwg.add(dwg.rect((keyItem["x"]*BASE_KEY_UNIT+BASE_KEY_MARGIN/2,keyItem["y"]*BASE_KEY_UNIT+BASE_KEY_MARGIN/2),(keyItemWidthMultiplier*BASE_KEY_UNIT-BASE_KEY_MARGIN/2,keyItemHeighthMultiplier*BASE_KEY_UNIT-BASE_KEY_MARGIN/2), 
                stroke='gray',fill="white" ,
                stroke_width=0.5,
                transform="rotate({} {} {})".format(
                        keyRotation,
                        defaultRx*BASE_KEY_UNIT,
                        defaultRy*BASE_KEY_UNIT)
           ))
           dwg.add(dwg.text(stdLayout,
                insert=((keyItem["x"]*BASE_KEY_UNIT)+BASE_KEY_UNIT/10,
                (keyItem["y"]*BASE_KEY_UNIT)+(BASE_KEY_UNIT*0.9)),
                
                transform="rotate({} {} {})".format(
                        keyRotation,
                        defaultRx*BASE_KEY_UNIT,
                        defaultRy*BASE_KEY_UNIT)))
        else:
            dwg.add(dwg.rect(
                (keyItem["x"]*BASE_KEY_UNIT+BASE_KEY_MARGIN/2,keyItem["y"]*BASE_KEY_UNIT+BASE_KEY_MARGIN/2),
                (keyItemWidthMultiplier*BASE_KEY_UNIT-BASE_KEY_MARGIN/2,keyItemHeighthMultiplier*BASE_KEY_UNIT-BASE_KEY_MARGIN/2),  stroke='gray',fill="white" ,
                stroke_width=0.5,))
            dwg.add(
                dwg.text(
                    stdLayout,
                    insert=((keyItem["x"]*BASE_KEY_UNIT)+(BASE_KEY_UNIT/10),
                    (keyItem["y"]*BASE_KEY_UNIT)+(BASE_KEY_UNIT*0.9))
                    )
                )
        
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
        createSvgForLayout(layout,data["keyboards"][key]["layouts"][layout]['layout'],data["keyboards"][key]["width"],data["keyboards"][key]["height"])
    
print("end")