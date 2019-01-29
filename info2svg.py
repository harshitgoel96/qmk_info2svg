import svgwrite
import http.client
import json 

BASE_KEY_WIDTH=19.05
BASE_KEY_HEIGHT=19.05

def createSvgForLayout(layoutName,layoutArray,sizeX,sizeY):
    dwg = svgwrite.Drawing("{}.svg".format(layoutName),size=('{}mm'.format(sizeX*BASE_KEY_WIDTH), '{}mm'.format(sizeY*BASE_KEY_HEIGHT)), viewBox=('0 0 {} {}'.format(sizeX*BASE_KEY_WIDTH,sizeY*BASE_KEY_HEIGHT)))
    defaultRx=0
    defaultRy=0
    for keyItem in layoutArray:
        keyItemWidthMultiplier=keyItem.get("w",1)
        keyItemHeighthMultiplier=keyItem.get("h",1)
        keyRotation=keyItem.get("r",0)
        defaultRx=keyItem.get("rx",defaultRx)
        defaultRy=keyItem.get("ry",defaultRy)
        stdLayout=keyItem.get("label","A")
        if keyRotation!=0:
           dwg.add(dwg.rect((keyItem["x"]*BASE_KEY_WIDTH,keyItem["y"]*BASE_KEY_HEIGHT),(keyItemWidthMultiplier*BASE_KEY_WIDTH,keyItemHeighthMultiplier*BASE_KEY_HEIGHT), 
                stroke='gray',fill="white" ,
                stroke_width=0.5,
                transform="rotate({} {} {})".format(
                        keyRotation,
                        defaultRx*BASE_KEY_WIDTH,
                        defaultRy*BASE_KEY_HEIGHT)
           ))
           dwg.add(dwg.text(stdLayout,
                insert=((keyItem["x"]*BASE_KEY_WIDTH)+BASE_KEY_WIDTH/10,
                (keyItem["y"]*BASE_KEY_WIDTH)+(BASE_KEY_WIDTH*0.9)),
                
                transform="rotate({} {} {})".format(
                        keyRotation,
                        defaultRx*BASE_KEY_WIDTH,
                        defaultRy*BASE_KEY_HEIGHT)))
        else:
            dwg.add(dwg.rect(
                (keyItem["x"]*BASE_KEY_WIDTH,keyItem["y"]*BASE_KEY_HEIGHT),
                (keyItemWidthMultiplier*BASE_KEY_WIDTH,keyItemHeighthMultiplier*BASE_KEY_HEIGHT),  stroke='gray',fill="white" ,
                stroke_width=0.5,))
            dwg.add(
                dwg.text(
                    stdLayout,
                    insert=((keyItem["x"]*BASE_KEY_WIDTH)+(BASE_KEY_WIDTH/10),
                    (keyItem["y"]*BASE_KEY_WIDTH)+(BASE_KEY_WIDTH*0.9))
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