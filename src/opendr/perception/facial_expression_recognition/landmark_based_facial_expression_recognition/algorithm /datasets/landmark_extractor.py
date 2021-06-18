"""
Modified based on: Adrian Rosebrock, Facial landmarks with dlib, OpenCV, and Python, PyImageSearch,
https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/, accessed on 27 August 2020
"""

import os
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2


def landmark_extractor(input_path, output_path, predictor_path):
    # initialize dlib's face detector (HOG-based) and then create
    detector = dlib.get_frontal_face_detector()
    # the facial landmark predictor
    predictor = dlib.shape_predictor(predictor_path)
    image = cv2.imread(input_path)
    image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)
    for (i, rect) in enumerate(rects):
        # determine the facial landmarks for the face region
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        print(output_path)
        np.save(output_path, shape)
        # draw the face bounding box
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # draw rectangles and landmarks on the image
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        for (x, y) in shape:
            cv2.circle(image, (x, y), 3, (0, 0, 255), -1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Facial landmark extractor')
    parser.add_argument('--dataset_name', default='CASIA')
    parser.add_argument("-p", "--shape_predictor", required=True,
                        default='./data/shape_predictor_68_face_landmarks.dat',
                        description="path to facial landmark predictor")
    parser.add_argument("-i", "--frames_folder", required=True, default='./data/CASIA/',
                        description="path to input image")
    parser.add_argument("-o", "--landmark_folder", required=True, default='./data/CASIA_landmarks/',
                        description="path to output")

    arg = vars(parser.parse_args())
    if not os.path.exists(arg.landmark_folder):
        os.makedirs(arg.landmark_folder)
    part = ['Train', 'Val']
    if arg.dataset_name == 'CASIA':
        num_subjects = len(os.listdir(arg.frames_folder))
        classes = ['Angry', 'Fear', 'Happy', 'Sad', 'Surprise', 'Disgust']
        for s in range(num_subjects):
            for c in range(classes):
                image_path = arg.frames_folder + '/{}/{}'.format(s, c)
                for root, _, files in os.walk(image_path):
                    for file in files:
                        if '.jpg' in file:
                            imgpth = os.path.join(root, file)
                            outpth = arg.landmark_folder + '/{}/{}'.format(s, c)
                            if not os.path.exists(outpth):
                                os.makedirs(outpth)
                            frameidx = file.split(".")
                            landmark_extractor(imgpth, outpth + frameidx[0] + '.npy', arg.shape_predictor)
    elif arg.dataset_name == 'CK+':
        num_subjects = len(os.listdir(arg.frames_folder))
        for s in range(num_subjects):
            image_path = arg.frames_folder + '/{}'.format(s)
            for _, dirs, _ in os.walk(image_path):
                for root, _, files in os.walk(dirs):
                    for file in files:
                        if '.jpg' in file:
                            imgpth = os.path.join(root, file)
                            outpth = arg.landmark_folder + '/{}/{}'.format(s, dirs)
                            if not os.path.exists(outpth):
                                os.makedirs(outpth)
                            frameidx = file.split(".")
                            landmark_extractor(imgpth, outpth + frameidx[0] + '.npy', arg.shape_predictor)
    elif arg.dataset_name == 'AFEW':
        classes = ['Angry', 'Fear', 'Happy', 'Sad', 'Surprise', 'Disgust', 'Neutral']
        for p in part:
            for c in classes:
                image_path = arg.frames_folder + '/{}/{}'.format(p, c)
                for _, dirs, _ in os.walk(image_path):
                    for root, _, files in os.walk(dirs):
                        for file in files:
                            if '.jpg' in file:
                                imgpth = os.path.join(root, file)
                                outpth = arg.landmark_folder + '/{}/{}/{}'.format(p, c, dirs)
                                if not os.path.exists(outpth):
                                    os.makedirs(outpth)
                                frameidx = file.split(".")
                                landmark_extractor(imgpth, outpth + frameidx[0] + '.npy', arg.shape_predictor)
