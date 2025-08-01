def suggest_reassignments(tasks, team_members, max_load=3):
    overloaded = {m["id"]: m["current_load"] for m in team_members if m["current_load"] > max_load}
    suggestions = []

    for task in tasks:
        assignee = task["assigned_to"]
        if assignee in overloaded:
            for m in team_members:
                if m["id"] != assignee and m["current_load"] < max_load:
                    if all(skill in m["skills"] for skill in task["title"].lower().split()):
                        suggestions.append({
                            "task_id": task["id"],
                            "from": assignee,
                            "to": m["id"]
                        })
                        m["current_load"] += 1
                        overloaded[assignee] -= 1
                        break

    return suggestions
