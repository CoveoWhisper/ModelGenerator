from collections import defaultdict

import requests


def is_link_working(link):
    try:
        response = requests.get(link)
        return response.status_code == 200
    except:
        return False

def remove_broken_links_documents_clicks(documents_clicks, is_verbose):
    query_counter = 0
    keep_links = defaultdict(bool)
    for link in documents_clicks:
        query_counter = query_counter + 1
        if is_verbose:
            print("Querying link number " + str(query_counter) + "...")
        keep_links[link] = is_link_working(link)
    broken_links_count = 0
    for link, keep in keep_links.items():
        if not keep:
            documents_clicks.pop(link)
            broken_links_count = broken_links_count + 1
    if is_verbose:
        print("Removed " + str(broken_links_count) + " broken links in documents clicks mapping.")

def remove_broken_links_documents_searches_mapping(documents_searches_mapping, documents_clicks, is_verbose):
    remove_searches = []
    for search, links in documents_searches_mapping.items():
        remove_links = []
        for link in links:
            if link not in documents_clicks:
                remove_links.append(link)
        for link in remove_links:
            links.pop(link)
        if not links:
            remove_searches.append(search)
    for search in remove_searches:
        documents_searches_mapping.pop(search)

    if is_verbose:
        print("Removed " + str(len(remove_links)) + " broken links in documents searches mapping.")
        print("Removed " + str(len(remove_searches)) + " searches in documents searches mapping.")
