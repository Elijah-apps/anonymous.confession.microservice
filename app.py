from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI()

# Model for a confession
class Confession(BaseModel):
    id: int
    message: str
    created_at: str

# Simulating a database with an in-memory list
confessions_db = []

# Route to submit a new confession
@app.post("/api/submit-confession")
def submit_confession(confession: Confession):
    # Simulate saving the confession (in reality, this would save to a database)
    confessions_db.append(confession)
    return {"message": "Confession submitted successfully!", "confession_id": confession.id}

# Route to get a list of all confessions
@app.get("/api/confessions", response_model=List[Confession])
def get_all_confessions():
    if not confessions_db:
        raise HTTPException(status_code=404, detail="No confessions found")
    return confessions_db

# Route to get a specific confession by ID
@app.get("/api/confession/{confession_id}", response_model=Confession)
def get_confession(confession_id: int):
    confession = next((conf for conf in confessions_db if conf.id == confession_id), None)
    if confession is None:
        raise HTTPException(status_code=404, detail="Confession not found")
    return confession

# Route to get the most recent confessions
@app.get("/api/latest-confessions", response_model=List[Confession])
def get_latest_confessions(limit: Optional[int] = 5):
    if not confessions_db:
        raise HTTPException(status_code=404, detail="No confessions found")
    # Return the most recent confessions (sorted by the ID, assuming higher IDs are newer)
    return sorted(confessions_db, key=lambda x: x.id, reverse=True)[:limit]

# Root route with a welcome message
@app.get("/")
def read_root():
    return {"message": "Welcome to the Anonymous Confession Microservice!"}

# Run the app using uvicorn (this can be done directly or using the command line)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
