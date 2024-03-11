from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Add your frontend origin(s) here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your other routes and endpoints go here

# MongoDB connection
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["mydb"]
collection = db["projects"]

class ProjectCreate(BaseModel):
    name: str
    email: str
    password: str

@app.post("/create_project/", response_model=dict)
async def create_project(project: ProjectCreate):
    try:
        # Insert project data into MongoDB
        result = await collection.insert_one(project.dict())
        return {"message": "Project created successfully", "project_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating project: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
