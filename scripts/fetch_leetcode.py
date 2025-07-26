import requests
import os
from datetime import datetime

USERNAME = "NiharikaNashine"  # ✅ Your LeetCode username

session = os.environ.get("LEETCODE_SESSION")
if not session:
    print("❌ LEETCODE_SESSION not found.")
    exit(1)

headers = {
    "Cookie": f"LEETCODE_SESSION={session}",
    "Referer": "https://leetcode.com",
    "User-Agent": "Mozilla/5.0"
}

query = """
query getRecentSubmission($username: String!) {
  recentAcSubmissionList(username: $username, limit: 1) {
    title
    titleSlug
    timestamp
  }
}
"""

res = requests.post(
    "https://leetcode.com/graphql",
    json={"query": query, "variables": {"username": USERNAME}},
    headers=headers
)

data = res.json()
if "data" not in data or not data["data"]["recentAcSubmissionList"]:
    print("⚠️ No recent accepted submissions found.")
    exit(0)

sub = data["data"]["recentAcSubmissionList"][0]
title = sub["title"].replace(" ", "_")
slug = sub["titleSlug"]
timestamp = datetime.now().strftime('%Y-%m-%d')

filename = f"{title}_{timestamp}.md"
filepath = os.path.join(".", filename)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(f"# {sub['title']}\n")
    f.write(f"- Problem link: https://leetcode.com/problems/{slug}/\n")
    f.write("\n✅ Solution accepted today. (Code capture not available yet)\n")

print(f"✅ Saved: {filename}")
