import datetime

def detect_risks(tasks):
    task_map = {t["id"]: t for t in tasks}
    risk_report = []

    for task in tasks:
        risk_level = "low"

        if task["status"] == "delayed":
            risk_level = "high"
        else:
            for dep_id in task["depends_on"]:
                dep = task_map.get(dep_id)
                if dep and dep["status"] == "delayed":
                    risk_level = "medium"
                    break

        risk_report.append({
            "id": task["id"],
            "title": task["title"],
            "assigned_to": task["assigned_to"],
            "status": task["status"],
            "risk": risk_level
        })

    return risk_report
