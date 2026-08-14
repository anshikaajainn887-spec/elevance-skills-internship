import json

with open("knowledge_db.json", "r", encoding="utf-8") as db:
    knowledge = json.load(db)

while True:
    query = input("You: ")

    if query.lower() == "exit":
        break

    found = False

    for item in knowledge:
        if query.lower() in item.lower():
            print("Bot:", item)
            found = True
            break

    if not found:
        print("Bot: Information not found.")