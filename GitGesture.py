import cv2
import mediapipe as mp
import subprocess

mp_hands = mp.solutions.hands
gesture_rec = mp_hands.GestureRecognition('static_gestures', max_num_hands=1)

cap = cv2.VideoCapture(0)
last_gesture_time = 0
gesture_timeout = 3

while cap.isOpened():
    success, image = cap.read()

    if not success:
        print("Không thể đọc từ camera")
        break

    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5) as hands:
        # Chuyển đổi ảnh thành định dạng RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Dò tìm bàn tay trong ảnh
        results = hands.process(image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
            # Trực quan hóa các điểm đặc trưng và kết nối tay thành các đường thẳng
                mp_hands.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # Nhận diện cử chỉ
            gesture_info = gesture_rec.process(image)

            if gesture_info.gestures:
                # Lặp qua các cử chỉ được nhận diện
                for gesture in gesture_info.gestures:
                # Kiểm tra nếu là cử chỉ thumbs up và hiển thị kết quả
                    if gesture.name == 'Thumbs Up':
                        cv2.putText(image, "Thumbs Up", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                    # Kiểm tra nếu đã quá thời gian timeout giữa các cử chỉ
                        current_time = cv2.getTickCount()
                        if current_time >= last_gesture_time + gesture_timeout * cv2.getTickFrequency():
                            print("Thực hiện hành động Thumbs Up")
                            subprocess.run(["git", "push"])
                            last_gesture_time = current_time
                    else:
                        cv2.putText(image, "Not Thumbs Up", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Thumbs Up Detector", image)

    # Nếu nhấn phím 'q', thoát khỏi vòng lặp
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
