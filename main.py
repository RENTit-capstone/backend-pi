from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Locker API running on Raspberry PI"}

@app.post("/unlock")
def unlock_locket(locker_id: int):
    return {"status": "unlocked", "locker_id": locker_id}

