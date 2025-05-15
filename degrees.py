import csv
import sys
from collections import deque

# Data structures
names = {}      
scientists = {} 
papers = {}     

def load_data():
    """Load data from CSV files into memory."""
    # Load scientists
    with open("scientists.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            scientist_id = row["scientist_id"]
            name = row["name"]
            scientists[scientist_id] = {
                "name": name,
                "papers": set()
            }
            lower = name.strip().lower()
            if lower not in names:
                names[lower] = {scientist_id}
            else:
                names[lower].add(scientist_id)

    # Load papers
    with open("papers.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            paper_id = row["paper_id"]
            title = row["title"]
            year = row["year"]
            papers[paper_id] = {
                "title": title,
                "year": year,
                "authors": set()
            }

    # Load authors
    with open("authors.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            scientist_id = row["scientist_id"]
            paper_id = row["paper_id"]
            if scientist_id in scientists and paper_id in papers:
                scientists[scientist_id]["papers"].add(paper_id)
                papers[paper_id]["authors"].add(scientist_id)

def person_id_for_name(name):
    """Return the scientist_id for a name, resolving duplicates."""
    scientist_ids = list(names.get(name.strip().lower(), set()))
    if len(scientist_ids) == 0:
        return None
    elif len(scientist_ids) > 1:
        print(f"Which '{name}'?")
        for sid in scientist_ids:
            s = scientists[sid]
            print(f"ID: {sid}, Name: {s['name']}")
        chosen_id = input("Intended Scientist ID: ").strip()
        if chosen_id in scientist_ids:
            return chosen_id
        else:
            return None
    else:
        return scientist_ids[0]

def neighbors_for_person(scientist_id):
    """Return (paper_id, scientist_id) pairs for co-authors."""
    neighbor_set = set()
    for paper_id in scientists[scientist_id]["papers"]:
        for author_id in papers[paper_id]["authors"]:
            if author_id != scientist_id:
                neighbor_set.add((paper_id, author_id))
    return neighbor_set

def shortest_path(source, target):
    """
    Return shortest list of (paper_id, scientist_id) from source to target.
    Uses Breadth-First Search (BFS).
    """
    frontier = deque([[(None, source)]])
    visited = set()

    while frontier:
        path = frontier.popleft()
        current = path[-1][1]

        if current == target:
            return path[1:]  # remove (None, source)

        visited.add(current)

        for paper_id, neighbor in neighbors_for_person(current):
            if neighbor not in visited:
                new_path = path + [(paper_id, neighbor)]
                if neighbor == target:
                    return new_path[1:]
                frontier.append(new_path)

    return None

def main():
    print("Loading data...")
    load_data()
    print("Data loaded.")

    source_name = input("Name: ")
    source_id = person_id_for_name(source_name)
    if source_id is None:
        sys.exit("Scientist not found.")

    target_name = input("Name: ")
    target_id = person_id_for_name(target_name)
    if target_id is None:
        sys.exit("Scientist not found.")

    path = shortest_path(source_id, target_id)

    if path is None:
        print("Not connected.")
    else:
        print(f"{len(path)} degrees of separation.")
        current_id = source_id
        for i, (paper_id, person_id) in enumerate(path, 1):
            person1 = scientists[current_id]["name"]
            person2 = scientists[person_id]["name"]
            paper_title = papers[paper_id]["title"]
            print(f"{i}: {person1} and {person2} co-authored \"{paper_title}\"")
            current_id = person_id

if __name__ == "__main__":
    main()


