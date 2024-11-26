from fuzzywuzzy import process

def search_passwords(passwords, query):
    password_names = [p.service_name for p in passwords]
    matches = process.extract(query, password_names, limit=5)
    matched_passwords = [p for p in passwords if p.service_name in [m[0] for m in matches]]
    return matched_passwords