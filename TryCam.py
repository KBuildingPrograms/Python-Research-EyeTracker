# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 15:54:37 2025

@author: kawdi
"""

import pygame as pg
from pygame.locals import *
import cv2 
import numpy as np
import os
import sys

def resources_path(relative_path): #path guide for Pyinstaller
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path,relative_path)

class MainCamera:
    def __init__(self,pos,camera,threshold,glasses):
        self.pos = pos
        self.camera = camera
        self.threshold = threshold
        self.glasses = glasses
        self.face_cascade = cv2.CascadeClassifier(resources_path('Haarcascade/haarcascade_frontalface_default.xml'))
        self.eye_cascade = cv2.CascadeClassifier(resources_path('Haarcascade/haarcascade_eye.xml'))
        self.glasses_cascade = cv2.CascadeClassifier(resources_path('Haarcascade/haarcascade_eye_tree_eyeglasses.xml'))
        
        
        self.detector_params = cv2.SimpleBlobDetector.Params()
        self.detector_params.filterByArea = True
        self.detector_params.maxArea = 1500
        self.detector_params.filterByConvexity = False
        self.detector = cv2.SimpleBlobDetector.create(self.detector_params)
        self.pts_holder = []
        self.face_pos = []
        self.r_eye_pos = []
        self.l_eye_pos = []
        
        
    def nothing(x):
        pass
    def detect_faces(self,img):
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        coords = self.face_cascade.detectMultiScale(gray_frame, 1.3, 5) #detects face in gray frame
        if len(coords) > 1:
            biggest = (0, 0, 0, 0)
            for i in coords: #Take the biggest face in frame
                if i[3] > biggest[3]:
                    biggest = i
            biggest = np.array([i], np.int32)
        elif len(coords) == 1:
            biggest = coords
        else:
            return None
        for (x, y, w, h) in biggest:
            frame = img[y:y + h, x:x + w] #frame is the size of the face 
        self.face_pos = [w,h]
        return frame
    def detect_eyes(self, img, classifier):
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #gray the face
        eyes = classifier.detectMultiScale(gray_frame, 1.3, 5) # detect eyes
        width = np.size(img, 1) # get face frame width
        height = np.size(img, 0) # get face frame height
        left_eye = None
        right_eye = None
        for (x, y, w, h) in eyes:
            if y > height / 2:
                pass
            eyecenter = x + w / 2  # get the eye center
            if eyecenter < width * 0.5:
                left_eye = img[y:y + h, x:x + w]
                self.l_eye_pos = []
            else:
                right_eye = img[y:y + h, x:x + w]
                self.r_eye_pos = [w,h]
        return left_eye, right_eye
    def cut_eyebrows(img):
        height, width = img.shape[:2]
        eyebrow_h = int(height/4)
        img = img[eyebrow_h:height, 0:width]
        return img
    def blob_process(self,img,detector,threshold):
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        retval, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
        img = cv2.erode(img, None, iterations=3)
        img = cv2.dilate(img,None,iterations=2)
        img = cv2.medianBlur(img, 5)
        self.keypoints = detector.detect(img)
        return self.keypoints
    def render(self):
        if self.camera.isOpened():
            self.ret, self.frame = self.camera.read()
            face_frame = MainCamera.detect_faces(self,self.frame)
            if face_frame is not None:
                eyes = MainCamera.detect_eyes(face_frame,self.glasses_cascade if self.glasses else self.eye_cascade)
                for eye in eyes:
                    if eye is not None:
                        eye = MainCamera.cut_eyebrows(eye)
                        self.keypoints = MainCamera.blob_process(self,eye,self.detector,self.threshold)
                        eye = cv2.drawKeypoints(eye,self.keypoints,self.frame,(255,0,0),flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.frame = np.rot90(self.frame)
        self.frame = pg.surfarray.make_surface(self.frame)
    def draw(self,screen):
        screen.blit(self.frame, self.pos)
    def detection_freq(self):
        pts = cv2.KeyPoint_convert(self.keypoints)
        x = 1 if len(pts)>0 else 0
        return x
    def eye_positions(self):
        location = []
        if self.camera.isOpened():
            self.ret, self.frame = self.camera.read()
            face_frame = MainCamera.detect_faces(self,self.frame)
            if face_frame is not None:
                eyes = MainCamera.detect_eyes(face_frame,self.glasses_cascade if self.glasses else self.eye_cascade)
                for eye in eyes:
                    if eye is not None:
                        eye = MainCamera.cut_eyebrows(eye)
                        self.keypoints = MainCamera.blob_process(self,eye,self.detector,self.threshold)
                        pts = cv2.KeyPoint_convert(self.keypoints)
            location.append(pts)
            return location
    def l_r_positions(self):
        l_pts, r_pts = None, None
        if self.camera.isOpened():
            self.ret, self.frame = self.camera.read()
            face_frame = MainCamera.detect_faces(self,self.frame)
            if face_frame is not None:
                l_eye, r_eye = MainCamera.detect_eyes(face_frame, self.glasses_cascade if self.glasses else self.eye_cascade)
                if l_eye is not None:
                    try:
                        l_eye = MainCamera.cut_eyebrows(l_eye)
                        l_keypoints = MainCamera.blob_process(self,l_eye,self.detector,self.threshold)
                        l_pts = cv2.KeyPoint_convert(l_keypoints)
                    except:
                        pass
                if r_eye is not None:
                    try:
                        r_eye = MainCamera.cut_eyebrows(l_eye)
                        r_keypoints = MainCamera.blob_process(self,r_eye,self.detector,self.threshold)
                        r_pts = cv2.KeyPoint_convert(r_keypoints)
                    except:
                        pass
        return l_pts, r_pts
