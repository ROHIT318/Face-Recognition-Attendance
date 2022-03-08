import cv2
import os
from datetime import datetime

# All requirements for face recognition
from keras.models import load_model
# To load scikit SVM model
import pickle

# Need to test this model load
base_dir = os.getcwd()
model_dir = os.path.join(base_dir, "{}\\{}".format('camera','facenet'))
face_model = load_model(model_dir)
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
svm_dir = os.path.join(base_dir, "{}\\{}".format('camera','SVM'))

# Frame image dimension for feeding into model
width = 160
height = 160
dim = (width, height)

# For image processing purpose
import numpy as np
from numpy import asarray, expand_dims

# Loading model only once
svm_model = pickle.load(open(svm_dir, 'rb'))

# For retaining old embedding
face_img_emb = np.array([])


def getdetails():
	startAttendanceProcess = False
	video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
	video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
	video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
	
	while True:
		ret, frame = video_capture.read()
		final_frame = get_face_rectangle(frame)
		# resizeFaceFrame = cv2.resize()
		cv2.imshow('Video', final_frame)

		formattedTime = int(datetime.now().strftime('%S'))
		if startAttendanceProcess == False:
			# amount of waiting time
			waitTime = 15
			tillTime = formattedTime + waitTime
			if (tillTime >= 60):
				tillTime = tillTime - 60
			startAttendanceProcess = True

		elif (formattedTime == tillTime):
			video_capture.release()
			cv2.destroyAllWindows()
			str = get_name(frame)
			return str

		# Hit 'q' on the keyboard to quit!
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	video_capture.release()
	cv2.destroyAllWindows()

def get_face_rectangle(img):
	faces = faceCascade.detectMultiScale(
		img,
		scaleFactor=1.3,
		minNeighbors=3,
		minSize=(30,30)
	)
	for (x, y, w, h) in faces:
		text = get_name(img)
		font = cv2.FONT_HERSHEY_DUPLEX
		cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
		cv2.putText(img, text, (x + 6, y - 6), font, 0.3, (255, 255, 255), 1)
	return img

def get_name(img):
	# Will have to load this from database
	name_list = ["Dwayne Johnson", "Robert Downey Jr.", "Sachin Tendulkar"]
	
	# Retaining last embedding and person name
	global svm_model, face_img_emb, person_name

	face_img = get_face_only(img)
	if len(face_img) != 0:
		face_img_emb = get_embedding(face_img)
		face_img_emb = np.expand_dims(face_img_emb, axis=0)
		person_name = name_list[svm_model.predict(face_img_emb)[0]]
		return person_name
	elif person_name == "":
		return "Unable to detect."
	else:
		return person_name

# Method to extraxt face from an image
def get_face_only(img):
	face_img = []
	faces = faceCascade.detectMultiScale(
		img,
		scaleFactor=1.3,
		minNeighbors=3,
		minSize=(30,30)
	)
	for (x, y, w, h) in faces:
		text = ""
		font = cv2.FONT_HERSHEY_DUPLEX
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
