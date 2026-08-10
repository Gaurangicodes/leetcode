import requests
from pathlib import Path

USERNAME = "Gaurangicodes"
URL = "https://leetcode.com/graphql"

QUERY = """
query userProfile($username: String!) {
    matchedUser(username: $username) {
        username
        submitStatsGlobal {
            acSubmissionNum {
                difficulty
                count
            }
        }
    }
}
"""


def get_leetcode_stats():
    response = requests.post(
        URL,
        json={
            "query": QUERY,
            "variables": {
                "username": USERNAME
            },
        },
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
        },
    )

    response.raise_for_status()

    data = response.json()

    if "errors" in data:
        raise RuntimeError(data["errors"])

    user = data["data"]["matchedUser"]

    if not user:
        raise RuntimeError(f"User not found: {USERNAME}")

    stats = {}

    for item in user["submitStatsGlobal"]["acSubmissionNum"]:
        stats[item["difficulty"].lower()] = item["count"]

    return stats


def update_readme(stats):
    readme_path = Path("README.md")

    content = readme_path.read_text(encoding="utf-8")

    total = stats.get("all", 0)
    easy = stats.get("easy", 0)
    medium = stats.get("medium", 0)
    hard = stats.get("hard", 0)

    new_progress = f"""| Difficulty | Solved |
|------------|-------:|
| 🟢 Easy | {easy} |
| 🟡 Medium | {medium} |
| 🔴 Hard | {hard} |
| **Total** | **{total}** |"""

    start_marker = "<!-- LEETCODE_STATS_START -->"
    end_marker = "<!-- LEETCODE_STATS_END -->"

    if start_marker in content and end_marker in content:
        start = content.index(start_marker)
        end = content.index(end_marker) + len(end_marker)

        replacement = (
            f"{start_marker}\n"
            f"{new_progress}\n"
            f"{end_marker}"
        )

        content = content[:start] + replacement + content[end:]
    else:
        print("⚠️ README markers not found.")
        print("Add these markers around your progress table.")

    readme_path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    stats = get_leetcode_stats()

    print("LeetCode stats:")
    print(f"Easy: {stats.get('easy', 0)}")
    print(f"Medium: {stats.get('medium', 0)}")
    print(f"Hard: {stats.get('hard', 0)}")
    print(f"Total: {stats.get('all', 0)}")

    update_readme(stats)

    print("\n✅ README updated!")