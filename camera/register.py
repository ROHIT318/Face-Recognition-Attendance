import os
import cv2
import time
from numpy import asarray
from .getdetails import get_face_only, get_embedding, face_model
from .models import registration_form
from sklearn.preprocessing import Normalizer, LabelEncoder

from sklearn.metrics import accuracy_score

# To load faceNet model
from keras.models import load_model
# To load scikit SVM model
from sklearn.svm import SVC
# To store and load trained SVM model
import pickle

# Frame image dimension for feeding into model
width = 160
height = 160
dim = (width, height)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def storeImage(str1, str2):
	global BASE_DIR
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
		ret, frame = video_capture.read()
		cv2.imshow('Video', frame)
		# For testing purpose taking full image
		img = get_face_only(frame)
		if img!=[]:
			img = frame
		else:
			img = []

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


		if img!=[] and i==6:
			img_6 = "pics/" + str(i) + "_" + uniqueId + ".jpg"
			img_6_link = link + str(i) + "_" + uniqueId + ".jpg"
			cv2.imwrite(img_6_link, img)
			i = i + 1
			time.sleep(waitTime)

		elif img!=[] and i==7:
			img_7 = "pics/" + str(i) + "_" + uniqueId + ".jpg"
			img_7_link = link + str(i) + "_" + uniqueId + ".jpg"
			cv2.imwrite(img_7_link, img)
			i = i + 1
			time.sleep(waitTime)

		elif i==8:
			# Storing Image in Database Here
			student = registration_form.objects.create(unique_id=uniqueId, name=studentName, 
				img_1=img_1, img_2=img_2, img_3=img_3, img_4=img_4, img_5=img_5, 
				img_6=img_6, img_7=img_7)
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


def createDataset():
	registeredStudents = registration_form.objects.all()
	images, labels = list(), list()

	for reg in registeredStudents:
		faces, label = list(), list()
		# images, labels = list(), list()
		# Remove get_face_only when not testing and print statements
		faces.append(get_face_only(cv2.imread(BASE_DIR + reg.img_1.url)))
		print(reg.img_1.url)
		print("ONE")
		faces.append(get_face_only(cv2.imread(BASE_DIR + reg.img_2.url)))
		print(reg.img_2.url)
		print("TWO")
		faces.append(get_face_only(cv2.imread(BASE_DIR + reg.img_3.url)))
		print(reg.img_3.url)
		print("THREE")
		faces.append(get_face_only(cv2.imread(BASE_DIR + reg.img_4.url)))
		print(reg.img_4.url)
		print("FOUR")
		faces.append(get_face_only(cv2.imread(BASE_DIR + reg.img_5.url)))
		print(reg.img_5.url)
		print("FIVE")
		faces.append(get_face_only(cv2.imread(BASE_DIR + reg.img_6.url)))
		print(reg.img_6.url)
		print("SIX")
		faces.append(get_face_only(cv2.imread(BASE_DIR + reg.img_7.url)))
		print(reg.img_7.url)
		print("SEVEN")
		for i in range(7):
			label.append(reg.unique_id)
		print(label)
		labels.extend(label)
		images.extend(faces)
		print("Once Done!")
	print(labels)
	return asarray(images), asarray(labels)


def startTraining():
	trainEmbeddings = list()
	trainImages, trainLabels = createDataset()
	print("Dataset Created!")

	# Get embeding for each training images
	for faceImage in trainImages:
		embedding = get_embedding(faceImage)
		trainEmbeddings.append(embedding)
	trainEmbeddings = asarray(trainEmbeddings)
	print("Embeddings Created!")

	# Normalizing face embedding vectors
	inputEncoder = Normalizer(norm='l2')
	trainEmbeddings = inputEncoder.transform(trainEmbeddings)
	print("Face Embedding Vector Normalized!")

	# Target name should be converted to integers
	outputEncoder = LabelEncoder()
	outputEncoder.fit(trainLabels)
	trainLabels = outputEncoder.transform(trainLabels)
	print("Target Name Converted To Integers!")

	# Using Linear Support Vector Machine for predicting using embeddings
	model = SVC(kernel='linear')
	model.fit(trainEmbeddings, trainLabels)
	print("SVM Model Training Done!")

	# Tesing model accuracy
	predictTrain = model.predict(trainEmbeddings)
	# predictTest = model.predict(testEmbeddings)

	trainAcc = accuracy_score(trainLabels, predictTrain)
	# testAcc = accuracy_score(testy, predict_test)

	# Storing and loading SVM model
	SVM_DIR = os.path.join(BASE_DIR, "{}\\{}".format('camera','SVM'))
	# filename = 'SVM'
	with open(SVM_DIR, 'wb') as files:
		pickle.dump(model, files)
	# joblib.dump(model, filename)
	print("SVM Model Saved!")

	return trainAcc