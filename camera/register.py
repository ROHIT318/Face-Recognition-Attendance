import os
import cv2
import time
from numpy import asarray
from .getdetails import get_face_only, get_embedding
from .models import registration_form
from sklearn.preprocessing import Normalizer, LabelEncoder

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

# Face recognition model
base_dir = os.getcwd()
model_dir = os.path.join(base_dir, "{}\\{}".format('camera','facenet'))
face_model = load_model(model_dir)


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


def createDataset():
	registeredStudents = registration_form.objects.all()
	images, labels = list(), list()

	for reg in registeredStudents:
		images, labels = list(), list()
		# Remove get_face_only when not testing
		images.extend(get_face_only(cv2.imread(BASE_DIR + reg.img_1.url)))
		images.extend(get_face_only(cv2.imread(BASE_DIR + reg.img_2.url)))
		images.extend(get_face_only(cv2.imread(BASE_DIR + reg.img_3.url)))
		images.extend(get_face_only(cv2.imread(BASE_DIR + reg.img_4.url)))
		images.extend(get_face_only(cv2.imread(BASE_DIR + reg.img_5.url)))
		for i in range(5):
			labels.extend(reg.unique_id)
	return asarray(images), asarray(labels)


def startTraining():
	trainEmbeddings = list()
	trainImages, trainLabels = createDataset()

	# Get embeding for each training images
	for faceImage in trainImages:
		embedding = get_embedding(faceImage)
		trainEmbeddings.append(embedding)
	trainEmbeddings = asarray(trainEmbeddings)

	# Normalizing face embedding vectors
	inputEncoder = Normalizer(norm='l2')
	trainImages = inputEncoder.transform(trainImages)

	# Target name should be converted to integers
	outputEncoder = LabelEncoder()
	outputEncoder.fit(trainLabels)
	trainLabels = outputEncoder.transform(trainLabels)

	# Using Linear Support Vector Machine for predicting using embeddings
	model = SVC(kernel='linear')
	model.fit(trainImages, trainEmbeddings)

	# Storing and loading SVM model
	filename = 'SVM'
	pickle.dump(model, open(filename, 'wb'))

	return "Training successfull."