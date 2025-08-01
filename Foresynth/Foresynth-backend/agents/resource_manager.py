def adjust_member_loads(tasks, team_members):
    """
    Recalculate current load for each team member based on assigned tasks
    that are still pending or in progress.
    """
    member_load = {m["id"]: 0 for m in team_members}

    for task in tasks:
        if task["status"] in ["pending", "in_progress"]:
            assignee = task["assigned_to"]
            if assignee in member_load:
                member_load[assignee] += 1

    # Update team member load
    for member in team_members:
        member["current_load"] = member_load[member["id"]]

    return team_members
