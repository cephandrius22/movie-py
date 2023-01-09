import csv
import sqlite3
import ast


def process_metadata(cur):
    with open("data/movies_metadata.csv", "r") as f:
        reader = csv.DictReader(f)
        data = []
        ids = set()
        for row in reader:
            # there seem to be duplicates in this dataset
            if row["id"] in ids:
                continue
            ids.add(row["id"])

            data += [
                (
                    row["budget"],
                    row["title"],
                    row["release_date"],
                    row["runtime"],
                    row["id"],
                )
            ]
        cur.executemany("INSERT INTO movies VALUES(?, ?, ?, ?, ?)", data)

def process_credits(cur):
    with open("data/credits.csv", "r") as f:
        reader = csv.DictReader(f)
        ids = set()
        for row in reader:
            # there seem to be duplicates in this dataset
            if row["id"] in ids:
                continue
            ids.add(row["id"])

            crew_data = []
            crew = ast.literal_eval(row["crew"])
            for c in crew:
                crew_data += [
                    (
                        c["job"],
                        c["department"],
                        c["name"],
                        c["id"],
                        hash(c["credit_id"]),
                    )
                ]
            cur.executemany("INSERT INTO crew_credits VALUES(?, ?, ?, ?, ?)", crew_data)

            cast_data = []
            cast = ast.literal_eval(row["cast"])
            for c in cast:
                cast_data += [
                    (
                        c["character"],
                        c["name"],
                        c["id"],
                        row["id"],
                        hash(c["credit_id"]),
                    )
                ]
            cur.executemany("INSERT INTO actor_credits VALUES(?, ?, ?, ?, ?)", cast_data)


con = sqlite3.connect("instance/movies.db")
cur = con.cursor()

# Take the existant of any entry in 'movies' as proof that we have
# already populated the tables.
res = cur.execute("SELECT count(*) FROM movies")
if res.fetchone()[0] == 0:
    process_metadata(cur)
    process_credits(cur)

con.commit()
