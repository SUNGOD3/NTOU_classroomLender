# NTOU_classLender

A platform that allow the people check the classroom's status and lend classroom
<br/><br/>
## 需要填的config
```
backend/api/config.yml
backend/database/docker-compose.yml
```

## API
```
先用pyenv把python版本切換到3.8
pipenv --python 3.8
```
前置作業
```
download the wsl and upgrade it to wsl2
download docker
```
cd backend/api/
pipenv install
pipenv run python initDatabase.py
```
## Database
啟用前記得先設定docker-compose.yml
```
cd backend/database/
docker-compose up
```
```
cd backend/api/
pipenv run python app.py

or

pipenv shell
python app.py
```

## Port
 - 13588 : API
 - 3306 &nbsp; : MySQL
 - 5001 &nbsp; : PhpMyAdmin
