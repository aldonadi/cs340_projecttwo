from quick_filter_buttons import QuickFilter, QuickFilters
from aac_crud_driver import AnimalShelter
import pprint

filters = QuickFilters.load()

print(f"Loaded {len(filters)} filters:")

for filter in filters:
    print(f"entry ({type(filter)}:")
    print(f"  raw:  {pprint.pprint(filter)}")
    print(f"  json: {filter.query_json()}")

print("Obtaining matching records from database...", end='')
shelter = AnimalShelter()
matches = shelter.find(filters[0].query_json())

print(f"got {len(matches)} matches")
print("First match:")
pprint.pprint(matches[0])
