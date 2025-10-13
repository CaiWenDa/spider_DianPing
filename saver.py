import csv

def save_csv(file_path, rows):
    with open(file_path, 'w', newline='', encoding='gbk') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)