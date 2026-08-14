import os
import json

knowledge = []

folder = "knowledge"

for file in os.listdir(folder):
    if file.endswith(".txt"):
        with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
            knowledge.append(f.read())

with open("knowledge_db.json", "w", encoding="utf-8") as db:
    json.dump(knowledge, db, indent=4)

print("Knowledge Base Updated Successfully!")