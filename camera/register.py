import os
import cv2
# import numpy as np
import time
from .getdetails import get_face_only
from .models import registration_form
from django.core.files.base import ContentFile

# Frame image dimension for feeding into model
width = 160
height = 160
dim = (width, height)


def showImage(str1, str2):
	uniqueId = str1
	studentName = str2
	# Face image variable
	img = []
	i = 1
	# Time to wait after taking one face frame
	waitTime = 2
	regForm = registration_form()
	video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
	video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
	video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

	while True:
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

		ret, frame = video_capture.read()
		cv2.imshow('Video', frame)
		img = get_face_only(frame)

		# Strorage location
		link = BASE_DIR + "\\media\\pics\\"

		if img!=[] and i==1:
			img_1 = "pics/" + str(i) + "_" + uniqueId + ".jpg"
			img_1_link = link + str(i) + "_" + uniqueId + ".jpg"
			cv2.imwrite(img_1_link, img)
			i = i + 1
			time.sleep(waitTime)

		elif img!=[] and i==2:
			img_2 = "pics/" + str(i) + "_" + uniqueId + ".jpg"
			img_2_link = link + str(i) + "_" + uniqueId + ".jpg"
			cv2.imwrite(img_2_link, img)
			i = i + 1
			time.sleep(waitTime)

		elif img!=[] and i==3:
			img_3 = "pics/" + str(i) + "_" + uniqueId + ".jpg"
			img_3_link = link + str(i) + "_" + uniqueId + ".jpg"
			cv2.imwrite(img_3_link, img)
			i = i + 1
			time.sleep(waitTime)

		elif img!=[] and i==4:
			img_4 = "pics/" + str(i) + "_" + uniqueId + ".jpg"
			img_4_link = link + str(i) + "_" + uniqueId + ".jpg"
			cv2.imwrite(img_4_link, img)
			i = i + 1
			time.sleep(waitTime)

		elif img!=[] and i==5:
			img_5 = "pics/" + str(i) + "_" + uniqueId + ".jpg"
			img_5_link = link + str(i) + "_" + uniqueId + ".jpg"
			cv2.imwrite(img_5_link, img)
			i = i + 1
			time.sleep(waitTime)

		elif i==6:
			# Storing Image in Database Here
			student = registration_form.objects.create(unique_id=uniqueId, name=studentName, 
				img_1=img_1, img_2=img_2, img_3=img_3, img_4=img_4, img_5=img_5)
			student.save()

			video_capture.release()
			cv2.destroyAllWindows()
			return "Student recorded successfully"

		# Hit 'q' on the keyboard to quit!
		elif cv2.waitKey(1) & 0xFF == ord('q'):
			break

		img = []

	video_capture.release()
	cv2.destroyAllWindows()