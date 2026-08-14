import json
import pandas as pd

print("Filtering CS papers from arXiv dataset...")

data = []
max_papers = 3000 

try:
    with open('arxiv-metadata-oai-snapshot.json', 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            
            if item.get('categories') and 'cs.' in item['categories']:
                data.append({
                    'id': str(item.get('id', '')),
                    'title': str(item.get('title', '')).strip().replace('\n', ' '),
                    'authors': str(item.get('authors', '')).strip().replace('\n', ' '),
                    'abstract': str(item.get('abstract', '')).strip().replace('\n', ' '),
                    'categories': str(item.get('categories', ''))
                })
                if len(data) >= max_papers:
                    break

    df = pd.DataFrame(data)
    df.to_csv('cs_papers_subset.csv', index=False)
    print(f"Successfully created 'cs_papers_subset.csv' with {len(df)} papers!")

except FileNotFoundError:
    print("Error: 'arxiv-metadata-oai-snapshot.json' file folder me nahi mili!")