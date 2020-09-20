import cv2
import os
import time
import sys
import read_vott_id_json as RVIJ
import write_vott_id_json as WVIJ

ROI_get_bbox = False

def get_algorithm_tracker(algorithm):
    if algorithm == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    elif algorithm == 'MIL':  
        tracker = cv2.TrackerMIL_create()
    elif algorithm == 'KCF':  
        tracker = cv2.TrackerKCF_create()
    elif algorithm == 'TLD':  
        tracker = cv2.TrackerTLD_create()
    elif algorithm == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    elif algorithm == 'GOTURN':
        tracker = cv2.TrackerGOTURN_create()
    elif algorithm == 'CSRT': 
        tracker = cv2.TrackerCSRT_create()
    elif algorithm == 'MOSSE':                                                                                                                              
        tracker = cv2.TrackerMOSSE_create()
    return tracker


def video_settings(video_cap, read_video_msec):
    video_cap.set(cv2.CAP_PROP_POS_MSEC, read_video_msec)    #read from read_video_msec sec
    #cap.set(cv2.CAP_PROP_POS_MSEC, 50000)    #read from 50s
    #cap.set(cv2.CAP_PROP_FPS, 15)  #not working

    wid = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    hei = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #framerate = int(cap.get(cv2.CAP_PROP_FPS))
    #framenum = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("width: %d" % wid)
    print("height: %d" % hei)

    #below framenum / framerate = video length
    #print("framerate: %d" % framerate)
    #print("framenum: %d" % framenum)
    return video_cap

def show_window_settings(window_name, width, height):
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, width, height)


def ROI_select(roi_window_name, frame):
    bbox = cv2.selectROI(roi_window_name, frame, False)
    cv2.destroyWindow(roi_window_name)
    return bbox

def fill_previous_data_to_write_json(rvij, wvij):
    
    wvij.save_parent_id(rvij.get_parent_id())
    wvij.save_parent_name(rvij.get_parent_name())
    wvij.save_parent_path(rvij.get_parent_path())
                                                                                                                                                
    wvij.save_tags(rvij.get_tags())

        
    print("fill previous data ok")


def check_which_frame(ft):

    if ft == 'mp4':
        time_count = 0
    elif ft == '066667': 
        time_count = 1
    elif ft == '133333': 
        time_count = 2
    elif ft == '2': 
        time_count = 3
    elif ft == '266667': 
        time_count = 4
    elif ft == '333333': 
        time_count = 5
    elif ft == '4': 
        time_count = 6
    elif ft == '466667': 
        time_count = 7
    elif ft == '533333': 
        time_count = 8
    elif ft == '6': 
        time_count = 9
    elif ft == '666667': 
        time_count = 10
    elif ft == '733333': 
        time_count = 11
    elif ft == '8': 
        time_count = 12
    elif ft == '866667': 
        time_count = 13
    elif ft == '933333':
        time_count = 14
    return time_count
   
def deal_with_name_format_path(rvij, wvij, time_interval_15fps, format_15fps, time_count): 
    org_asset_name = rvij.get_asset_name()
    org_timestamp = rvij.get_timestamp()
    org_asset_path = rvij.get_asset_path()
    #print('org_asset_name: %s' % org_asset_name)
    #print('org_timestamp: %.5f' % org_timestamp)
    #print('org_asset_path: %s' % org_asset_path)
    org_timestamp = int(org_timestamp)
    name_count = 0
    for i in org_asset_name:
        name_count +=1
        if i == '=':
            break
    org_asset_name = org_asset_name[:name_count]     
    now_timestamp = time_interval_15fps[time_count]
    now_timestamp = str(org_timestamp +  now_timestamp)
    now_asset_name = org_asset_name + now_timestamp
    #print('now_frame_asset_name: %s' % now_asset_name)
    #print('now_timestamp: %.2f' % now_timestamp)
    
    path_count = 0
    for i in org_asset_path:
        path_count +=1
        if i == '=':
            break
    org_asset_path = org_asset_path[:path_count]     
    now_asset_path = org_asset_path + now_timestamp
    print('now_frame_asset_path: %s' % now_asset_path)

    #this function will be created id via path by md5 method 
    wvij.save_asset_path(now_asset_path)
    wvij.save_asset_format(format_15fps[time_count])
    wvij.save_asset_name(now_asset_name)
    wvij.save_timestamp(now_timestamp)

    return time_count

def deal_with_BX_PT(wvij, bbox): 
    BX = []
    BX.append(bbox[3])  #height BX[0]
    BX.append(bbox[2])  #width BX[1]
    BX.append(bbox[0])  #left BX[2]
    BX.append(bbox[1])  #top BX[3]

    wvij.save_boundingBox(BX)

    PT =[]
    PT.append(BX[1]+BX[2])
    PT.append(BX[0]+BX[3])
    wvij.save_points(PT)

def main(target_path, file_path, video_path, algorithm):
    time_interval_15fps = [0, 0.066667, 0.133333, 0.2, 0.266667, 0.333333,
                       0.4, 0.466667, 0.533333, 0.6, 0.666667, 0.733333,
                       0.8, 0.866667, 0.933333]
    
    format_15fps = ['mp4', '066667', '133333', '2', '266667', '333333',
                       '4', '466667', '533333', '6', '666667', '733333',
                       '8', '866667', '933333']

    
    video_cap = cv2.VideoCapture(video_path)
    if not video_cap.isOpened():
        print("open video failed.")
        sys.exit()
    bbox = ()
    get_timestamp = 0
    if ROI_get_bbox == False:
        rvij = RVIJ.read_vott_id_json(file_path)
        if rvij.read_from_id_json_data():
            print('read json file failed')
            sys.exit()

        get_bbox = rvij.get_boundingBox()
        bbox = (get_bbox[0], get_bbox[1], get_bbox[2],  get_bbox[3])
        get_timestamp = rvij.get_timestamp()
    else:
        roi_window_name = 'ROI select'
        bbox = ROI_select(roi_window_name, frame)

    tracker = get_algorithm_tracker(algorithm)

    video_cap = video_settings(video_cap, get_timestamp * 1000)

    ok,frame = video_cap.read()
    if not ok:
        print("open video failed.")
        sys.exit()

    #try:
    #    frame = cv2.resize(frame, (1280, 720))
    #except:
    #    print("frame resize failed")
    
    window_name = "frame"
    show_window_settings(window_name, 1280, 720)

    tracker.init(frame, bbox)

    fps = 0.066667  #1sec(15frame) 1/15
    print("fps %.5f" % fps)
    startTime = time.time()
    time_count = check_which_frame(rvij.get_asset_format())
    print("time_count: %d" % time_count)

    wvij = WVIJ.write_vott_id_json(target_path)
    fill_previous_data_to_write_json(rvij, wvij)

    

    while True:
        #ok,frame = cap.read()
    #   try:
    #        frame = cv2.resize(frame, (1280, 720))
    #    except:
    #        print("frame resize failed")
        nowTime = time.time()
        if float(nowTime - startTime) > fps:
            ok,frame = video_cap.read()
            if not ok:
                print("open video failed.")
                sys.exit()

            ok, bbox = tracker.update(frame)
            #print(bbox[0])
            if ok:                    
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
                #print("p1: %.d",p1)
            else:                     
                cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

            startTime = time.time()
            time_count = time_count + 1
            deal_with_name_format_path(rvij, wvij, time_interval_15fps, format_15fps, time_count)
            deal_with_BX_PT(wvij, bbox) 
            print("time_count %d" % time_count)
            wvij.create_id_json_data()
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        if time_count == 14:
            break


if __name__ == '__main__':
    #file_path = '../../Drone_Project/Drone_Target/001/3dde1a6f488582de7f4c50493a348e43-asset.json'
    
    target_path = '../../Drone_Project/Drone_Target/001/'
    file_path = target_path
    if len(sys.argv[1]) > 1:
        file_path = file_path + sys.argv[1]
        print("file_path: %s" % file_path)
    #if len(sys.argv[2]) > 1:
        #algorithm = sys.argv[2]
        #print(algorithm)

    video_path = '../../Drone_Project/Drone_Source/001/Drone_001.mp4'
    algorithm = 'CSRT'
    main(target_path, file_path, video_path, algorithm)
