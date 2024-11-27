- pytorch chatbot 위한 fastapi와 mongoDB 연계하는 기본 설정
- URI 통한 image 접속 제공
  
#### Main package
- python:3.11
- mongo:7
- fastapi

#### connect remote Docker container
```
~$ uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- @ http://localhost:8888/
- @ http://localhost:8888/images/empty.txt
- @ mongodb://localhost:27017/ or mongodb://mongodb:27017/

#### samples
- [app/samples/sample_mongodb_connection.py](./app/samples/sample_mongodb_connection.py)
- [app/main.py](./app/main.py)
