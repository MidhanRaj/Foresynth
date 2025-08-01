import datetime

def generate_schedule(tasks, team_members):
    scheduled_tasks = []
    member_availability = {m["id"]: m["available_from"] for m in team_members}
    task_lookup = {task["id"]: task for task in tasks}
    completed = set()

    def schedule_task(task):
        if task["id"] in completed:
            return

        # Schedule dependencies first
        for dep_id in task["depends_on"]:
            if dep_id in task_lookup:
                schedule_task(task_lookup[dep_id])

        assignee = task["assigned_to"]
        avail_date = datetime.datetime.strptime(member_availability.get(assignee, "2025-08-01"), "%Y-%m-%d")
        
        # Latest end date from dependencies
        dep_end = avail_date
        for dep_id in task["depends_on"]:
            dep_task = next((t for t in scheduled_tasks if t["id"] == dep_id), None)
            if dep_task:
                end = datetime.datetime.strptime(dep_task["end_date"], "%Y-%m-%d")
                if end > dep_end:
                    dep_end = end

        start_date = max(avail_date, dep_end)
        end_date = start_date + datetime.timedelta(days=task["duration_days"])

        task["start_date"] = start_date.strftime("%Y-%m-%d")
        task["end_date"] = end_date.strftime("%Y-%m-%d")

        member_availability[assignee] = task["end_date"]
        scheduled_tasks.append(task)
        completed.add(task["id"])

    for task in tasks:
        schedule_task(task)

    return scheduled_tasks

def enhanced_generate_schedule(tasks, team_members, priority_weights=None):
    """
    Placeholder for enhanced scheduling logic. 
    Your teammate can implement:
    - Priority-based sorting
    - Skill-weighted assignment
    - Dynamic task duration adjustments
    - Load balancing based on current_load
    """
    # For now, use basic generate_schedule
    return generate_schedule(tasks, team_members)

