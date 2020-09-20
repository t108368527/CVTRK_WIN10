import os, shutil
import json
import hashlib
# pip install shortuuid
import shortuuid

class write_vott_id_json():
# private
    def __clear_all_parameter_value(self):
        self.asset_id = ""
        self.asset_format = ""
        self.asset_path = ""

        self.parent_id = ""
        self.parent_name = ""
        self.parent_path = ""

        self.video_size = [3840, 2160]
        self.timestamp = 0
        
        self.regions_id = ""
        self.tags = ""
        self.boundingBox = []
        self.points = []
    def __save_asset_id(self, sid):
        self.asset_id = sid

    def __save_regions_id(self, rid):
        self.regions_id = rid

    def __create_asset_id_via_md5(self, path):
        m = hashlib.md5()
        m.update(path.encode("utf-8"))
        h = m.hexdigest()
        print("asset_id: %s" % h)
        self.__save_asset_id(h)

    def __create_shorid_for_regions_id(self):
        sid = shortuuid.uuid()
        sid = sid[:9]
        self.__save_regions_id(sid)

# public
    def __init__(self, target_path):
        self.target_path = ""
        if os.path.exists(target_path):
            self.target_path = target_path
            #print("target_path: %s" % target_path)
        else:
            print('target path is not existed!!')
        self.__clear_all_parameter_value()
    
    def create_id_json_data(self):
        try:
            #data = {"asset":{'id':'ddd', 'format':'ddd', 'state':2, 'type':3, 'name':'gg', 'path':'tt'}}
            #output = json.dumps(data, separators=(',\n', ': '))
            #print(output)
            #with open('abc.json', 'w', encoding='utf-8') as f:
            self.__create_shorid_for_regions_id()

            with open( self.target_path + self.asset_id + '-asset.json', 'w') as f:
                #json.dump(data, f)
                f.write('{\n')
                f.write('    \"asset\": {\n')
                f.write('        \"id\": ' +  '\"'+ self.asset_id + '\",\n')
                f.write('        \"format\": ' +  '\"'+ self.asset_format + '\",\n')
                f.write('        \"state\": 2,\n')
                f.write('        \"type\": 3,\n')
                f.write('        \"name\": ' +  '\"'+ self.asset_name+ '\",\n')
                f.write('        \"path\": ' +  '\"'+ self.asset_path+ '\",\n')
                f.write('        \"size\": {\n')
                f.write('            \"width\": 3840,\n')
                f.write('            \"height\": 2160\n')
                f.write('        },\n')
                f.write('        \"parent\": {\n')
                f.write('            \"format\": \"mp4\",\n')
                f.write('            \"id\": ' + '\"' + self.parent_id + '\",\n')
                f.write('            \"name\": ' + '\"' + self.parent_name + '\",\n')
                f.write('            \"path\": ' + '\"' + self.parent_path + '\",\n')
                f.write('            \"size\": {\n')
                f.write('                \"width\": 3840,\n')
                f.write('                \"height\": 2160\n')
                f.write('            },\n')
                f.write('            \"state\": 2,\n')
                f.write('            \"type\": 2\n')
                f.write('        },\n')
                f.write('        \"timestamp\": ' + str(self.timestamp) +'\n')
                f.write('    },\n')
                f.write('    \"regions\": [\n')
                f.write('        {\n')
                f.write('            \"id\": ' + '\"'+ self.regions_id +'\"'+',\n')
                f.write('            \"type\": \"RECTANGLE\",\n')
                f.write('            \"tags\": [\n')
                f.write('                \"' + self.tags + '\"\n')
                f.write('            ],\n')
                f.write('            \"boundingBox\": {\n')
                f.write('                \"height\": ' + str(self.boundingBox[0]) + ',\n')
                f.write('                \"width\": ' + str(self.boundingBox[1]) + ',\n')
                f.write('                \"left\": ' + str(self.boundingBox[2]) + ',\n')
                f.write('                \"top\": ' + str(self.boundingBox[3]) + '\n')
                f.write('            },\n')
                f.write('            \"points\": [\n')
                f.write('                {\n')
                f.write('                    \"x\": ' + str(self.boundingBox[2]) + ',\n')
                f.write('                    \"y\": ' + str(self.boundingBox[3]) + '\n')
                f.write('                },\n')

                f.write('                {\n')
                f.write('                    \"x\": ' + str(self.points[0]) + ',\n')
                f.write('                    \"y\": ' + str(self.boundingBox[3]) + '\n')
                f.write('                },\n')

                f.write('                {\n')
                f.write('                    \"x\": ' + str(self.points[0]) + ',\n')
                f.write('                    \"y\": ' + str(self.points[1]) + '\n')
                f.write('                },\n')

                f.write('                {\n')
                f.write('                    \"x\": ' + str(self.boundingBox[2]) + ',\n')
                f.write('                    \"y\": ' + str(self.points[1]) + '\n')
                f.write('                }\n')


                f.write('            ]\n')
                f.write('        }\n')
                f.write('    ],\n')
                f.write('    \"version\": \"2.2.0\"\n')
                f.write('}')


            return False
        except:
            print(' write vott id json failed ')
            return True

    
    def save_asset_format(self, sformat):
        self.asset_format = sformat
    
    def save_asset_name(self, sname):
        self.asset_name = sname

    def save_asset_path(self, spath):
        self.asset_path = spath
        self.__create_asset_id_via_md5(self.asset_path)

    def save_parent_id(self, pid):
        self.parent_id = pid

    def save_parent_name(self, pname):
        self.parent_name = pname

    def save_parent_path(self, ppath):
        self.parent_path = ppath

    def save_video_size(self, size):
        self.video_size = size

    def save_timestamp(self, timestamp):
        self.timestamp = timestamp
    
    def save_tags(self, tags):
        self.tags = tags

    def save_boundingBox(self, BX):
        self.boundingBox = []
        self.boundingBox.append(BX[0])  #height 
        self.boundingBox.append(BX[1])  #width 
        self.boundingBox.append(BX[2])  #left
        self.boundingBox.append(BX[3])  #top
    
    def save_points(self, PT):
        #self.points.append(PT[0])  #x1 = left
        #self.points.append(PT[1])  #y1 = top
        self.points = []
        self.points.append(PT[0])  #x2
        self.points.append(PT[1])  #y2

