1. Fork the repo
2. Clone it to your local machine
3. Open your CMD and type following command
	```python
	pip install virtualenvwrapper-win
	```
4. ```python
	mkvirtualenv <virtual-env-name>
	```
5. Navigate to folder `\<virtual-env-name>\Scripts\`
	* There open `CMD` and write `activate`. CMD environemt should be showing now as `<virtual-env-name>`
6. Run command "
	```bash
	pip install -r requirements.txt
	```
	* This will take a lot of time depending on you internet speed, download size upto 800 MB.
7. Download attendance.zip(160+ MB) provided by me before, unzip navigate inside it. Copy `camera\facenet_keras.h5`, `camera\SVM`, `camera\facenet` inside your cloned repo.
8. Web app uses postgresql at backend make sure you have it installed and running at defualt `port: 5432`. Use password `1234` when prompted to enter a password or change it in `attendance/settings.py` file, if you enter a different password.
9. create a database named `rohit` or change it in `attendance/settings.py` file, if you created a database of different name.
10. Come to root folder of your repo, run following command in sequence
	```python
	python manage.py makemigrations
	```
	```python
	python manage.py sqlmigrate
	```
	```python
	python manage.py migrate
	```
	> Schemas should have been created by now in your database.
11. After that, run command 
	```bash
	python manage.py runserver
	```
12. Web app should be running at `http://localhost:8000/`

# All Web Pages and Details: (For the time being) 
**1) Home Page: (This will be the Index page of website)**
> Will contain only three cards:
1. Start Attendance
2. Register Teacher
3. Register Student

**2) Start Attendance: (This page will open after button 1 of Home Page is pressed)**
> Will contain three input type text, a button:
1.	Teacher Username (input)
2.	Subject Code (Dropdown menu)
3.	Password (Input)
4.	Start Attendance (Button)

**3) Camera Starts: (This page will start after “Start Attendance” button 4 of 2nd procedure is pressed)**
> Camera window will pop up, after ϰ seconds it will automatically close and will send the name of the person to backend.

**4) Attendance Show Page: (This page will show the details of students present or attendance done in the current class.)**
> At top there will be two buttons:
1.	Stop Attendance (Button)
2.	Take Attendance (Button)
> Followed by a table containing all the details of the student:

Cin_id | Name | Subject Code | Date | Time
-------|------|--------------|------|------
XXXX | Rohit Sharma | CMSMXXXX | 28/02/22 | 21:38
YYYY | Sanjibani Mishra | CMSMXXXX | 28/02/22 | 21:40
ZZZZ | Atrimoy Saha | CMSMXXXX | 28/02/22 | 21:45

**5) Register Teacher: (A page where teacher can register by pressing button 2 of Home Page)**
> Will contain six input type text, one button:
1. t_id (Text)
2. t_name (Text)
3. t_department (Dropdown menu)
4. t_subjectcode (Dropdown menu)
5. t_pswd (Input type password at least 2)
6. Register (Button)

**6) Register Student: (To enter student details)**
> Will contain two input type text, one button:
1. unique_id (Text)
2. student_name (Text)

**7) For registration of student more web page views will be added later.**