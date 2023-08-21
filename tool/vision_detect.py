from ultralytics import YOLO
from cvzone.PoseModule import PoseDetector
import time
import json
import cv2
import os

try:
    import ranking
except:
    import tool.ranking as ranking

rope_model_path ='./model/rope_model.pt'
motion_model_path ='./model/motion_model.pt'
rope_model = YOLO(rope_model_path)
motion_model = YOLO(motion_model_path)

def process_video(input_path, output_path):
    
    json_path = os.path.splitext(output_path)[0] + '.json'
    tmp_name = os.path.splitext(output_path)[0][10:34]+'.mp4'
    print("\n\n\ntmp:"+tmp_name) 
    
    counter = 0
    counterOpen = 0
    counterCross = 0
    counterLFRB = 0
    counterRFLB = 0
    stage = None
    last_high = 0
    highest = 0
    lowest = 0
    pTime = 0
    up = False
    down = False
    err = 0
    
    detector = PoseDetector()

    cap = cv2.VideoCapture(input_path)  # webcam
    print(input_path)

    input_fps = int(cap.get(cv2.CAP_PROP_FPS))
    duration = cap.get(cv2.CAP_PROP_FRAME_COUNT)/cap.get(cv2.CAP_PROP_FPS)
    print("\n\n\nduration:"+str(duration))
    size = (720, 1280)
    
    # Below VideoWriter object will create
    # a frame of above defined The output 
    # is stored in 'filename.avi' file.
    out = cv2.VideoWriter('processed/'+tmp_name, 
                            cv2.VideoWriter_fourcc(*'mp4v'),
                            input_fps, size)
    
    while True:
        ret, frame = cap.read()
        if ret:
            # frame = cv2.rotate(frame, cv2.ROTATE_180)
            frame = cv2.resize(frame,(720,1280))
            rope_results = rope_model(frame)
            frame = rope_results[0].plot()
            motion_results = motion_model(frame)
            frame = motion_results[0].plot()
            lables = motion_results[0].boxes.cls.tolist()
            motion = -1
            if lables:
                motion = lables[0]

            frame = detector.findPose(frame)
            lmList, bboxInfo = detector.findPosition(frame)

            high = 0
            try:
                high = bboxInfo['center'][1]

                if high - last_high < -3.3:
                    up = True
                    down = False
                    highest = high
                    stage = "up"
                    err = 0
                elif high - last_high > 3.3:
                    down = True
                    if up and down and lowest - highest > 10:
                        counter = counter + 1
                        highest = lowest + 600
                        # {-1: 'None', 0: 'LF', 1: 'LFRB', 2: 'RF', 3: 'RFLB', 4: 'cross', 5: 'oepn'}
                        if motion == 0 or motion == 1 :
                            counterLFRB = counterLFRB + 1
                        if motion == 2 or motion == 3 :
                            counterRFLB = counterRFLB + 1
                        if motion == 4:
                            counterCross = counterCross + 1
                        if motion == 5:
                            counterOpen = counterOpen + 1
                    up = False
                    lowest = high
                    stage = "down"
                    err = 0

                last_high = high
            except:
                pass

            # Render curl counter
            # Setup status box
            cv2.rectangle(frame, (0,0), (1080,73), (245,117,16), -1)

            # data
            cv2.putText(frame, 'jump', (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(frame, str(counter),(10,60),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(frame, 'Open', (165, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, str(counterOpen), (160, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, 'Cross', (315, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, str(counterCross), (310, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, 'LFRB', (465, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, str(counterLFRB), (460, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, 'RFLB', (615, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, str(counterRFLB), (610, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(frame, 'STAGE', (800,12),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(frame, stage,(760,60),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(frame, f"FPS : {int(fps)}", (930, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
            frame = cv2.resize(frame, size, interpolation=cv2.INTER_CUBIC)
            out.write(frame)
            
            if __name__ == '__main__' or cv2.waitKey(1) == ord('v'):
                cv2.imshow('video', frame)
            # cv2.imshow('video', frame)
        else:
            break
        if cv2.waitKey(1) == ord('q') and __name__ == '__main__':
            break
    
    score = round((counterOpen*2+counterCross*3+(counterLFRB+counterRFLB)*5)/duration*30)
    
    filename = os.path.splitext(os.path.basename(input_path))[0]
    rank = ranking.write(filename, score)
    
    output = {"score": score,"times": counter,"open_times": counterOpen,\
        "cross_times": counterCross,"magic_cross_times": counterLFRB+counterRFLB}
    with open(json_path, "w") as f:
        json.dump(output, f, indent = 4)
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    os.system("ffmpeg -i processed/"+tmp_name+" -vcodec libx264 -f mp4 processed/out.mp4")
    os.remove("processed/"+tmp_name)
    os.rename("processed/out.mp4",output_path)
    print("The video was successfully saved")
    

if __name__ == '__main__':
    process_video('./test_vid/test0.mp4', './test_vid/output.mp4')
    
