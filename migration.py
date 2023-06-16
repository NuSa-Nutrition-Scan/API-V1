import csv

import firebase_admin
from firebase_admin import credentials, firestore


def get_firebase_instance():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(credential=cred)
    fb_instance = firebase_admin.get_app()
    return fb_instance


def get_firestore(firebase_app):
    return firestore.client(app=firebase_app)


if __name__ == "__main__":
    db = get_firestore(get_firebase_instance())

    collection_ref = db.collection("food_collection")

    with open("food_raw.csv", "r") as f:
        csvreader = csv.reader(f)

        _ = next(csvreader)

        for row in csvreader:
            id, name, calories = row[1], row[2], int(row[8])
            protein, lemak, karbohidrat = (
                int(round(float(row[9]))),
                int(round(float(row[10]))),
                int(round(float(row[11]))),
            )

            # vitamin ganti serat
            # mineral pake air

            vitamin = int(round(float(row[12])))
            mineral = int(round(float(row[7])))

            table = collection_ref.document(name)

            table.set(
                {
                    "id": id,
                    "name": name,
                    "calories": calories,
                    "calories_for_2x": calories * 4,
                    "calories_for_3x": int(calories * 2.7),
                    "calories_for_4x": calories * 2,
                    "protein": protein,
                    "lemak": lemak,
                    "karbohidrat": karbohidrat,
                    "vitamin": vitamin,
                    "mineral": mineral,
                }
            )

    f.close()

    print("Job finished")
