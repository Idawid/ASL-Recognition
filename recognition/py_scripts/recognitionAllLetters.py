import numpy as np
import cv2
import keras
from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf

background = None
accumulated_weight = 0.5

ROI_top = 100
ROI_bottom = 300
ROI_right = 150
ROI_left = 350

word_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H',
             8: 'I', 9: 'K', 10: 'L', 11: 'M', 12: 'N', 13: 'O', 14: 'P',
             15: 'Q', 16: 'R', 17: 'S', 18: 'T', 19: 'U', 20: 'V', 21: 'W',
             22: 'X', 23: 'Y'}


def cal_accum_avg(frame, accumulated_weight):
    global background

    if background is None:
        background = frame.copy().astype("float")
        return None

    cv2.accumulateWeighted(frame, background, accumulated_weight)


def segment_hand(frame, threshold=25):
    global background

    diff = cv2.absdiff(background.astype("uint8"), frame)

    _, thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

    # Fetching contours in the frame (These contours can be of hand or any other object in foreground) ...
    contours, hierarchy = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If length of contours list = 0, means we didn't get any contours...
    if len(contours) == 0:
        return None
    else:
        # The largest external contour should be the hand 
        hand_segment_max_cont = max(contours, key=cv2.contourArea)

        # Returning the hand segment(max contour) and the thresholded image of hand...
        return thresholded, hand_segment_max_cont


def start_recognition_live(is_abc):
    start_recognition(None, False, is_abc)


def start_recognition_video(filename, is_abc):
    return start_recognition(filename, True, is_abc)


def start_recognition_photo(dirname, is_abc):
    return start_recognition(dirname, False, is_abc)


def start_recognition(path, is_video, is_abc):
    if not is_abc:
        model = keras.models.load_model(r"recognition/models/model_EfficientNetB0.h5")
    else:
        model = keras.models.load_model(r"recognition/models/best_model_ABC.h5")

    if not path:
        cam = cv2.VideoCapture(0)

    if path and is_video:
        res_filename = path.replace('.mp4', '') + '_result.avi'
        cam = cv2.VideoCapture(path)
        frame_width = int(cam.get(3))
        frame_height = int(cam.get(4))

        size = (frame_width, frame_height)
        result = cv2.VideoWriter(res_filename,
                                 cv2.VideoWriter_fourcc(*'MJPG'),
                                 60, size)

    num_frames = 0
    while True:
        ret, frame = cam.read()

        if not ret:
            break

        # filpping the frame to prevent inverted image of captured frame...
        if not path:
            frame = cv2.flip(frame, 1)

        frame_copy = frame.copy()

        # ROI from the frame
        roi = frame[ROI_top:ROI_bottom, ROI_right:ROI_left]

        gray_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (9, 9), 0)

        if num_frames < 70:

            cal_accum_avg(gray_frame, accumulated_weight)

            if not path:
                cv2.putText(frame_copy, "FETCHING BACKGROUND...PLEASE WAIT", (80, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 0, 255), 2)

        else:
            # segmenting the hand region
            hand = segment_hand(gray_frame)

            # Checking if we are able to detect the hand...
            if hand is not None:
                thresholded, hand_segment = hand

                # Drawing contours around hand segment
                cv2.drawContours(frame_copy, [hand_segment + (ROI_right, ROI_top)], -1, (255, 0, 0), 1)

                if not path:
                    cv2.imshow("Thesholded Hand Image", thresholded)

                thresholded = cv2.resize(thresholded, (64, 64))
                thresholded = cv2.cvtColor(thresholded, cv2.COLOR_GRAY2RGB)
                thresholded = np.reshape(thresholded, (1, thresholded.shape[0], thresholded.shape[1], 3))

                pred = model.predict(thresholded)
                cv2.putText(frame_copy, word_dict[np.argmax(pred)], (170, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Draw ROI on frame_copy
        if not path:
            cv2.rectangle(frame_copy, (ROI_left, ROI_top), (ROI_right, ROI_bottom), (255, 128, 0), 3)

        # incrementing the number of frames for tracking
        num_frames += 1

        # Display the frame with segmented hand
        cv2.putText(frame_copy, "DataFlair hand sign recognition", (10, 20), cv2.FONT_ITALIC, 0.5, (0, 0, 0), 1)
        if not path:
            cv2.imshow("Sign Detection", frame_copy)
        if is_video:
            result.write(frame_copy)

        # Close windows with Esc
        if not path:
            k = cv2.waitKey(1) & 0xFF

            if k == 27:
                break

    # Release the camera and destroy all the windows
    cam.release()
    if is_video:
        result.release()
    cv2.destroyAllWindows()

    if not path:
        return

    if is_video:
        return res_filename
