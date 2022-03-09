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
8. Come to root folder of your repo, run command 
	```bash
	python manage.py runserver
	```
9) Web app should be running at `http://localhost:8000/` 