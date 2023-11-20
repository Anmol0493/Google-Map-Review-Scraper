import json, csv

with open('Details.json', 'r', encoding='utf-8') as d:
    details = json.load(d)

with open('Details.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(["name", "category", "phone", "email", "website", "rating", "total_reviews", "url"])

    for detail in details:
        writer.writerow([
            detail["name"],
            detail["category"],
            # detail["phone"],
            f'"{detail["phone"]}"',
            detail["email"],
            detail["website"],
            detail["rating"],
            detail["total_reviews"],
            detail["url"],
        ])

print(f"CSV data has been written to Details.csv")