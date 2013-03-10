ref.txt: id -> show_name reference

In scrape.py:
get_people_by_show(show_id): return all person_id -> name reference based on a show id
retrieve_headshot(person_id, folder_path='./'): download headshot images for the person

Usage:
python scrape.py