import cv2
import os
from datetime import datetime
from .models import registration_form

# All requirements for face recognition
from keras.models import load_model
# To load scikit SVM model
import pickle

# Face recognition models
base_dir = os.getcwd()
model_dir = os.path.join(base_dir, "{}\\{}".format('camera','facenet'))
face_model = load_model(model_dir)
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
prevStudentId= "Unable to detect"

# Frame image dimension for feeding into model
width = 160
height = 160
dim = (width, height)

# For image processing purpose
import numpy as np
from numpy import asarray, expand_dims

# To load SVM again
def loadSVM():
	SVM_DIR = os.path.join(base_dir, "{}\\{}".format('camera','SVM'))
	svm_model = pickle.load(open(SVM_DIR, 'rb'))
	return svm_model

# Loading all unique ids from student table
def getStudentList():
	uniqueIdList = list()
	students = registration_form.objects.all()
	for student in students:
		uniqueIdList.append(student.unique_id)
	return uniqueIdList

def getDetails():
	global prevStudentId
	svm_model = loadSVM()
	uniqueIdList = getStudentList()
	startAttendanceProcess = False
	video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
	video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
	video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
	
	while True:
		ret, frame = video_capture.read()
		final_frame, studentId = get_face_rectangle(frame, svm_model, uniqueIdList)
		cv2.imshow('Video', final_frame)

		formattedTime = int(datetime.now().strftime('%S'))
		if startAttendanceProcess == False:
			# amount of waiting time
			waitTime = 10
			tillTime = formattedTime + waitTime
			if (tillTime >= 60):
				tillTime = tillTime - 60
			startAttendanceProcess = True

		elif (formattedTime == tillTime):
			video_capture.release()
			cv2.destroyAllWindows()
			# Return name and id here
			if studentId == "":
				studentId = prevStudentId
			return studentId

		# Hit 'q' on the keyboard to quit!
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	video_capture.release()
	cv2.destroyAllWindows()

def get_face_rectangle(img, svm_model, uniqueIdList):
	global prevStudentId
	text = ""
	faces = faceCascade.detectMultiScale(
		img,
		scaleFactor=1.3,
		minNeighbors=3,
		minSize=(30,30)
	)
	for (x, y, w, h) in faces:
		text = get_name(img, svm_model, uniqueIdList)
		if text == "":
			text = prevStudentId
		font = cv2.FONT_HERSHEY_DUPLEX
		cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
		cv2.putText(img, text, (x + 6, y - 6), font, 0.6, (255, 255, 255), 1)
	return img, text

def get_name(img, svm_model, uniqueIdList):
	global prevStudentId
	face_img_emb = np.array([])
	face_img = get_face_only(img)

	if len(face_img) != 0:
		face_img_emb = get_embedding(face_img)
		face_img_emb = np.expand_dims(face_img_emb, axis=0)
		studentId = uniqueIdList[svm_model.predict(face_img_emb)[0]]
		prevStudentId = studentId
		return prevStudentId
	else:
		return prevStudentId

# Method to extraxt face from an image
def get_face_only(img):
	faces = faceCascade.detectMultiScale(
		img,
		scaleFactor=1.3,
		minNeighbors=3,
		minSize=(30,30)
	)
	for (x, y, w, h) in faces:
		crop_img = img[y:y+h, x:x+w]
		f_img = cv2.resize(crop_img, dim)
		face_img = asarray(f_img)
	return face_img

# Method to calculate face embedding for a face image
def get_embedding(face_img):
	global face_model

	face_img = np.array(face_img, dtype=np.float32)
	mean, std = face_img.mean(), face_img.std()
	face_pixels = (face_img - mean) / std
	# transform face into one sample
	samples = expand_dims(face_pixels, axis=0)
	# make prediction to get embedding
	embeds = face_model.predict(samples)
	return embeds[0]
