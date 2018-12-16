import csv
from collections import defaultdict


def get_clicks_counts(csv_path):
    clicks_counts = defaultdict(int)
    with open(csv_path, encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, escapechar="\\")
        headers = next(csv_reader)
        document_url_column_index = headers.index("documentUrl")
        for row in csv_reader:
            document_url = row[document_url_column_index]
            clicks_counts[document_url] += 1
    return clicks_counts
