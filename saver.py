import csv

def save_csv(output_file, data):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerows(data)