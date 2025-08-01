from fastapi import FastAPI, HTTPException
from typing import List
from models.team_member import TeamMember
from models.task import Task
from agents.planner import generate_schedule, enhanced_generate_schedule
from agents.risk_detector import detect_risks
from agents.resource_manager import adjust_member_loads
import json
import os

app = FastAPI()

# File paths
DATA_FILE = os.path.join("data", "project_data.json")
TASK_FILE = os.path.join("data", "tasks.json")

# -----------------------------
# 📂 Utility functions
# -----------------------------
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_tasks():
    with open(TASK_FILE, "r") as f:
        return json.load(f)

def save_tasks(data):
    with open(TASK_FILE, "w") as f:
        json.dump(data, f, indent=2)

# -----------------------------
# 👥 Team member routes
# -----------------------------
@app.get("/team-members", response_model=List[TeamMember])
def get_team_members():
    data = load_data()
    return data.get("team", [])

@app.post("/team-members")
def update_team_members(members: List[TeamMember]):
    data = load_data()
    data["team"] = [m.dict() for m in members]
    save_data(data)
    return {"message": "Team members updated successfully"}

# -----------------------------
# ✅ Task routes
# -----------------------------
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return load_tasks()

@app.post("/tasks")
def update_tasks(tasks: List[Task]):
    save_tasks([t.dict() for t in tasks])
    return {"message": "Tasks updated successfully"}

# -----------------------------
# 🧠 Task Assignment
# -----------------------------
@app.post("/assign-tasks")
def assign_tasks():
    data = load_data()
    tasks = load_tasks()
    assigned = generate_schedule(tasks, data["team"])
    save_tasks(assigned)
    return {"message": "Tasks assigned successfully", "tasks": assigned}

# -----------------------------
# ⚠️ Risk Detection
# -----------------------------
@app.get("/risks")
def get_risks():
    tasks = load_tasks()
    risks = detect_risks(tasks)
    return {"risks": risks}

# -----------------------------
# 🛠️ Resource Optimization
# -----------------------------
@app.post("/optimize-resources")
def optimize_resources():
    data = load_data()
    tasks = load_tasks()
    adjusted_team = adjust_member_loads(data["team"], tasks)
    data["team"] = adjusted_team
    save_data(data)
    return {"message": "Resources optimized", "team": adjusted_team}

