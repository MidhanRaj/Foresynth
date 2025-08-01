from fastapi import FastAPI, HTTPException
from models.team_member import TeamMember
from typing import List
import json
import os

app = FastAPI()

DATA_FILE = os.path.join("data", "project_data.json")

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.get("/team-members", response_model=List[TeamMember])
def get_team_members():
    data = load_data()
    return data.get("team_members", [])

@app.post("/team-members")
def add_team_member(member: TeamMember):
    data = load_data()
    if any(m["id"] == member.id for m in data["team_members"]):
        raise HTTPException(status_code=400, detail="Team member ID already exists")
    data["team_members"].append(member.dict())
    save_data(data)
    return {"message": "Team member added successfully"}

