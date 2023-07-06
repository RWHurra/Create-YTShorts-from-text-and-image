import os
import csv

class DirectoryCreator():
    def create_directories(csv_file, textedit):
        with open(csv_file, "r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Extract joke details from the CSV row
                setup = row["Setup"]
                punchline = row["Punchline"]
                os.makedirs(setup.rstrip('?'), exist_ok=True)
                with open(setup.rstrip('?') + '/' + 'dad-joke.txt', 'w') as f:
                    f.write('"' + setup + '", "' + punchline + '"')
        textedit.setPlainText("Created directories from " + csv_file)