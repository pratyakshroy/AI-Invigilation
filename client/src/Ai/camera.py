import cv2
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
import time


faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')



class Video(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.pTime = 0
        self.RightHand = 0
        self.LeftHand = 1
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(max_num_faces=1)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)
        self.detector = HandDetector(detectionCon=0.8, maxHands=2)

        self.cheat_count = 0

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        hands, frame = self.detector.findHands(frame)

        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # imgRGB = cv2.flip(imgRGB,1)
        results = self.faceMesh.process(imgRGB)

        if results.multi_face_landmarks:
            for faceLms in results.multi_face_landmarks:
                self.mpDraw.draw_landmarks(
                    frame, faceLms, self.mpFaceMesh.FACEMESH_TESSELATION, self.drawSpec, self.drawSpec)
                face = []
                for id, lm in enumerate(faceLms.landmark):
                    # print(lm)
                    ih, iw, ic = frame.shape
                    x, y = int(lm.x * iw), int(lm.y * ih)
                    if id == 28:
                        #print(id, x, y)
                        if x <= 270 or x >= 303:
                            cv2.putText(frame, f' WARNING! CHEATING DETECTED ', (47, 420), cv2.FONT_HERSHEY_PLAIN, 2,
                                        (0, 0, 255), 2)
                          # print(id,x,y)
                            self.cheat_count += 1

        if hands:
            # Hand 1
            hand1 = hands[0]
            lmList1 = hand1["lmList"]  # list of landmarks
            handType1 = hand1["type"]  # type of hand left or right
            centerPoint1 = hand1["center"]

            if len(hands) == 2:
                hand2 = hands[1]
                lmList2 = hand2["lmList"]  # list of landmarks
                handType2 = hand2["type"]  # type of hand left or right
                centerPoint2 = hand2["center"]

            else:
                self.cheat_count += 1
                cv2.putText(frame, f' WARNING! CHEATING DETECTED ',
                            (47, 420), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            # print(cheat_count)

        else:
            self.cheat_count += 1

            cv2.putText(frame, f' WARNING! CHEATING DETECTED ',
                        (47, 420), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        cTime = time.time()
        fps = 1 / (cTime - self.pTime)
        self.pTime = cTime

    # print(a)
        cv2.putText(frame, f'FPS: {int(fps)}', (20, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0))
        cv2.putText(frame, f'{int(self.cheat_count)} cheat detected',
                    (20, 120), cv2.FONT_HERSHEY_PLAIN, 2, (247, 247, 47), 2)

        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()

    def final_counter(self):
        
        return self.cheat_count;    


