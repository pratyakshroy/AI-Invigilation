import cv2
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
pTime = 0
RightHand = 0
LeftHand = 1

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)
detector = HandDetector(detectionCon=0.8, maxHands=2)

cheat_count = 0

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # imgRGB = cv2.flip(imgRGB,1)
    results = faceMesh.process(imgRGB)

    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(
                img, faceLms, mpFaceMesh.FACEMESH_TESSELATION, drawSpec, drawSpec)
            face = []
            for id, lm in enumerate(faceLms.landmark):
                # print(lm)
                ih, iw, ic = img.shape
                x, y = int(lm.x * iw), int(lm.y * ih)
                if id == 28:
                    print(id, x, y)
                    if x <= 270 or x >= 303:
                        cv2.putText(img, f' WARNING! CHEATING DETECTED ', (47, 420), cv2.FONT_HERSHEY_PLAIN, 2,
                                    (0, 0, 255), 2)
                        # print(id,x,y)
                        cheat_count += 1

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
            cheat_count += 1
            cv2.putText(img, f' WARNING! CHEATING DETECTED ',
                        (47, 420), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            # print(cheat_count)

    else:
        cheat_count += 1

        cv2.putText(img, f' WARNING! CHEATING DETECTED ', (47, 420),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # print(a)
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0))
    cv2.putText(img, f'{int(cheat_count)} cheat detected',
                (20, 120), cv2.FONT_HERSHEY_PLAIN, 2, (247, 247, 47), 2)

    # (20,70) position
    # cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)  # change the frame rate by this
