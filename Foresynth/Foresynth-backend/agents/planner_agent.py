import datetime

def detect_risks(tasks, team_members):
    issues = []
    today = datetime.datetime.today().date()
    
    member_load = {m["id"]: 0 for m in team_members}
    for task in tasks:
        if task["status"] != "completed":
            member_load[task["assigned_to"]] += 1

        # Check if task is overdue
        if task["status"] != "completed" and task.get("end_date"):
            end_date = datetime.datetime.strptime(task["end_date"], "%Y-%m-%d").date()
            if end_date < today:
                issues.append({
                    "task_id": task["id"],
                    "issue": f"Task is overdue (was due {task['end_date']})"
                })

        # Check for missing dependencies
        for dep_id in task["depends_on"]:
            dep_task = next((t for t in tasks if t["id"] == dep_id), None)
            if dep_task and dep_task["status"] != "completed":
                issues.append({
                    "task_id": task["id"],
                    "issue": f"Depends on incomplete task '{dep_id}'"
                })

    # Check load
    for member_id, load in member_load.items():
        if load > 3:
            issues.append({
                "member_id": member_id,
                "issue": f"High task load: {load} active tasks"
            })

    return issues
