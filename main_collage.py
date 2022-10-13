import cv2
import numpy as np
from tkinter import messagebox


class Collage:
    def __init__(self, image):
        self.image = image

    def Collage_vertical(self):
        img2 = cv2.imread('test1.jpg')
        dimensions1 = self.image.shape
        width_cutoff1 = dimensions1[1] // 2
        s1 = self.image[:, :width_cutoff1]
        cv2.imwrite("D:\changed_images\_1_part.jpg", s1)

        dimensions2 = self.image.shape
        width_cutoff2 = dimensions2[1] // 2
        s2 = img2[:, width_cutoff2:]
        cv2.imwrite("D:\changed_images\_2_part.jpg", s2)

        ph1 = cv2.imread('D:\changed_images\_1_part.jpg')
        ph2 = cv2.imread('D:\changed_images\_2_part.jpg')
        v_img = np.concatenate((ph1, ph2), axis=1)

        cv2.imshow("test", v_img)
        cv2.waitKey(0)
        cv2.imwrite("D:\changed_images\_two_ph.jpg", v_img)

    def Collage_horizontal(self):
        img2 = cv2.imread('test1.jpg')
        dimensions1 = self.image.shape
        height_cutoff1 = dimensions1[0] // 2
        s1 = self.image[:height_cutoff1, :]
        cv2.imwrite("D:\changed_images\_1_hori_part.jpg", s1)

        dimensions2 = img2.shape
        height_cutoff2 = dimensions2[0] // 2
        s2 = img2[height_cutoff2:, :]
        cv2.imwrite("D:\changed_images\_2_hori_part.jpg", s2)

        ph1 = cv2.imread('D:\changed_images\_1_hori_part.jpg')
        ph2 = cv2.imread('D:\changed_images\_2_hori_part.jpg')
        v_img = np.concatenate((ph1, ph2), axis=0)

        cv2.imshow("test", v_img)
        cv2.waitKey(0)
        cv2.imwrite("D:\changed_images\_two_ph_hor.jpg", v_img)


class FaceDetection:
    def __init__(self, image):
        self.image = image

    def Face_detection(self):
        cascPath = 'haarcascade_frontalface_default.xml'
        faceCascade = cv2.CascadeClassifier(cascPath)
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=3,
            minSize=(30, 30)
        )
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow("Face detection.", self.image)
            cv2.waitKey(0)
            #cv2.imwrite("D:\changed_images\_faces_detected.jpg", self.image)
            cv2.imwrite("redacted_photos/faces_detected.jpg", self.image)
        else:
            messagebox.showinfo('Помилка!', 'Не знайдено жодного обличчя на фото!')

# вирізана ф-я
# def Face_detection_on_camera():
#    face_cascade_db = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#    cap = cv2.VideoCapture(0)
#    while True:
#        success, img = cap.read()
#
#        faces = face_cascade_db.detectMultiScale(img, 1.1, 19)
#        for (x, y, w, h) in faces:
#            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
#        cv2.imshow('Face Detection', img)
#        # cv2.waitKey(0)
#        if cv2.waitKey(1) & 0xff == ord('q'):
#            break
