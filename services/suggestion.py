def suggest_improvements(info):
    suggestions = []

    if not info["skills"]:
        suggestions.append("Nên bổ sung kỹ năng chuyên môn")

    if len(info["experience"]) == 0:
        suggestions.append("Nên thêm kinh nghiệm làm việc")

    if len(info["education"]) == 0:
        suggestions.append("Nên thêm thông tin học vấn")

    return suggestions