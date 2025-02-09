#!/usr/bin/python3

from aac_crud_driver import AnimalShelter

shelter = AnimalShelter("aacuser", "i3-bNzTV6OF#V-'a00e+=iKh&JQs")

###############################################################################
print("Inserting a new record...", end='')

the_wombat = { "breed": "wombat" }

existing_wombats = shelter.find(the_wombat)
if len(existing_wombats) > 0:
    print("FAILED. A wombat already existed...")
else:
    result = shelter.create(the_wombat)
    if result:
        print("PASSED.")
    else:
        print("FAILED.")

###############################################################################
print("Searching for the wombat...", end='')

existing_wombats = shelter.find(the_wombat)

num_wombats_found = len(existing_wombats)

if num_wombats_found == 0:
    print("FAILED.    none found!")
elif num_wombats_found > 1:
    print(f"FAILED.   {len(existing_wombats)} found!")
else:
    print("PASSED.")

###############################################################################
print("Naming the wombat...",end='')
new_name = { "name": "Reginald Fluffinstocker III" }

num_named = shelter.update(the_wombat, new_name)

if num_named == 0:
    print("FAILED.    none renamed!")
elif num_named > 1:
    print(f"FAILED.   {num_named} named!")
else:
    print("PASSED.")


###############################################################################
print("Secretly euthanizing poor Reginald Fluffinstocker the Third...",end='')
reginald = the_wombat

num_deleted = shelter.delete(reginald)

if num_deleted == 0:
    print("FAILED.    none deleted!")
elif num_deleted > 1:
    print(f"FAILED.   {num_deleted} named!")
else:
    print("PASSED.")

print("All done.")

