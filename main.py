from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World - by Aleksa(ndra)\n"}

@app.get("/test")
def app_test():
    return{"test":"Test test 123"}
