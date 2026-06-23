import re

skills = [
    "python",
    "sql",
    "java",
    "aws",
    "docker",
    "git",
    "machine learning",
    "flask",
    "fastapi"
]

resume = open(
    "resume.txt",
    "r",
    encoding="utf-8"
).read().lower()

found = []

for skill in skills:

    if re.search(skill, resume):
        found.append(skill)

print("\nDetected Skills:\n")

for s in found:
    print("✓", s)

print(
    "\nTotal Skills Found:",
    len(found)
)
