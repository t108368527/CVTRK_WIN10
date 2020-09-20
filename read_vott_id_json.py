import os, shutil
import json
import numpy as np
from collections import defaultdict

class read_vott_id_json():
# private
    def __clear_all_parameter_value(self):
        self.id = ""
        self.asset_path = ""
        self.video_size = [3840, 2160]
        self.timestamp = 0
        self.tags = ""
        self.regions_id = ""
        self.boundingBox = [0,0,0,0]
        #self.points = [0,0,0,0]

    def __print_read_parameter_from_json(self):
        print("id: %s" % self.id)
        print("path: %s" % self.asset_path)
        print("width: %d" % self.video_size[0])
        print("height: %d" % self.video_size[1])
        print("timestamp: %.5f" % self.timestamp)
        print("tags: %s" % self.tags)
        print("boundingBox height: %s" % self.boundingBox[0])
        print("boundingBox width: %s" % self.boundingBox[1])
        print("boundingBox left: %s" % self.boundingBox[2])
        print("boundingBox top: %s" % self.boundingBox[3])


# public
    def __init__(self, file_path):
        self.file_path = ""
        if os.path.exists(file_path):
            self.file_path = file_path
            self.__clear_all_parameter_value()
            print("file_path: %s" % file_path)
        else:
            print('file is not existed!!')
    
    def read_from_id_json_data(self):
        try:
            with open(self.file_path, 'r') as reader:
                print("open_ok")
                jf = json.loads(reader.read())
                self.id = jf['asset']['id']
                self.asset_path = jf['asset']['format']
                self.video_size[0] = jf['asset']['size']['width']
                self.video_size[1] = jf['asset']['size']['height']
                self.timestamp = jf['asset']['timestamp']

                self.tags = jf['regions'][0]['tags'][0]
                self.boundingBox[0] = jf['regions'][0]['boundingBox']["height"]
                self.boundingBox[1] = jf['regions'][0]['boundingBox']["width"]
                self.boundingBox[2] = jf['regions'][0]['boundingBox']["left"]
                self.boundingBox[3] = jf['regions'][0]['boundingBox']["top"]

                self.__print_read_parameter_from_json()
                
            return False
        except:
            print(' wrong format: '+ self.file_path)
            return True

    def get_id(self):
        return self.id

    def get_asset_path(self):
        return self.asset_path

    def get_video_size(self):
        return self.video_size

    def get_timestamp(self):
        return self.timestamp
    
    def get_tags(self):
        return self.tags

    def get_boundingBox(self):
        BX = [0,0,0,0]
        BX[0] = self.boundingBox[2]     #x1=left
        BX[1] = self.boundingBox[3]     #y1=top    
        BX[2] = self.boundingBox[1]     #x2=width    
        BX[3] = self.boundingBox[0]     #y2=height 
        return BX

