import cv2
import os
import time
import sys
import read_vott_id_json as RVIJ

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

def main(file_path, video_path, algorithm):
    
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
    time_count = 0
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
            print(bbox[0])
            if ok:                    
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
                print("p1: %.d",p1)
            else:                     
                cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

            startTime = time.time()
            time_count = time_count + 1
            print("time_count %d" % time_count)
    
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        if time_count == 15:
            break


if __name__ == '__main__':
    video_path = '../../Drone_Project/Drone_Target/001/3dde1a6f488582de7f4c50493a348e43-asset.json'
    file_path = '../../Drone_Project/Drone_Source/001/Drone_001.mp4'
    algorithm = 'CSRT'
    main(video_path, file_path, algorithm)
