import datetime

def suggest_member(task, team_members, tasks):
    best_match = None
    best_score = -1

    member_load = {m["id"]: 0 for m in team_members}
    member_avail = {m["id"]: m["available_from"] for m in team_members}

    for t in tasks:
        if t["status"] != "completed":
            member_load[t["assigned_to"]] += 1

    for member in team_members:
        score = 0

        # Skill match
        match_count = len(set(task["skills_required"]) & set(member["skills"]))
        score += match_count * 2

        # Availability (earlier is better)
        avail_date = datetime.datetime.strptime(member_avail[member["id"]], "%Y-%m-%d").date()
        days_until_free = (avail_date - datetime.date.today()).days
        score -= days_until_free // 2  # penalize later dates

        # Task load (fewer tasks = better)
        score -= member_load[member["id"]]

        if score > best_score:
            best_score = score
            best_match = member["id"]

    return best_match
