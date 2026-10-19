from fastapi import FastAPI

app = FastAPI()
print("hello")
app.get("/")
def serverRunning():
    print("Server is running successfully")