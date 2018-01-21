from statistics import mode

import cv2
from keras.models import load_model
import numpy as np

from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input
import urllib.request, json

import webview
import bisect
import webbrowser

# parameters for loading data and images
detection_model_path = '../trained_models/detection_models/haarcascade_frontalface_default.xml'
emotion_model_path = '../trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
emotion_labels = get_labels('fer2013')

# hyper-parameters for bounding boxes shape
frame_window = 10
emotion_offsets = (20, 40)

# loading models
face_detection = load_detection_model(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)

# getting input model shapes for inference
emotion_target_size = emotion_classifier.input_shape[1:3]

# starting lists for calculating modes
emotion_window = []

# starting video streaming
cv2.namedWindow('ezxkcd')
video_capture = cv2.VideoCapture(0)

emotion_score = 0

def emotion_score_calculator(raw, c):
    return c + (raw - 0.2) * 4 / 7

while True:
    bgr_image = video_capture.read()[1]
    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    faces = detect_faces(face_detection, gray_image)

    for face_coordinates in faces:

        x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
        gray_face = gray_image[y1:y2, x1:x2]
        try:
            gray_face = cv2.resize(gray_face, (emotion_target_size))
        except:
            continue

        gray_face = preprocess_input(gray_face, True)
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
        emotion_prediction = emotion_classifier.predict(gray_face)
        emotion_probability = np.max(emotion_prediction)
        emotion_label_arg = np.argmax(emotion_prediction)
        emotion_text = emotion_labels[emotion_label_arg]
        emotion_window.append(emotion_text)

        if len(emotion_window) > frame_window:
            emotion_window.pop(0)
        try:
            emotion_mode = mode(emotion_window)
        except:
            continue

        if emotion_text == 'angry':
            color = emotion_probability * np.asarray((255, 0, 0))
            emotion_score = emotion_score_calculator(emotion_probability, -1.0)
        elif emotion_text == 'sad':
            color = emotion_probability * np.asarray((0, 0, 255))
            emotion_score = emotion_score_calculator(emotion_probability, -0.6)
        elif emotion_text == 'happy':
            color = emotion_probability * np.asarray((255, 255, 0))
            emotion_score = emotion_score_calculator(emotion_probability, 0.2)
        elif emotion_text == 'surprise':
            color = emotion_probability * np.asarray((0, 255, 255))
            emotion_score = emotion_score_calculator(emotion_probability, 0.6)
        else:
            color = emotion_probability * np.asarray((0, 255, 0))
            emotion_score = emotion_score_calculator(emotion_probability, -0.2)

        color = color.astype(int)
        color = color.tolist()

        draw_bounding_box(face_coordinates, rgb_image, color)
        draw_text(face_coordinates, rgb_image, emotion_mode,
                  color, 0, -45, 1, 1)

    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)

    bgr_image = cv2.resize(bgr_image, (0, 0), fx=0.75, fy=0.75)
    cv2.imshow('ezxkcd', bgr_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyWindow("ezxkcd")

f = open('xkcd.txt', 'r')
all_xkcds = eval(f.read())
f.close()

all_scores = []

for xkcd in all_xkcds:
    all_scores.append(xkcd[0])

comic = all_xkcds[bisect.bisect(all_scores, emotion_score)][1]

f = open('images.txt', 'r')
all_image_urls = eval(f.read())
f.close()

image_url = all_image_urls[comic]

# with urllib.request.urlopen("https://xkcd.com/" + str(comic) + "/info.0.json") as json_url:
#     text = json_url.read()
#     data = json.loads(text)
#     image_url = data["img"]

webview.create_window("Here's your comic, young lad.", image_url)

# webbrowser.open(url)
