from aac_crud_driver import AnimalShelter

a = AnimalShelter()
r = list(a.find( { "breed": "Labradore Retriever Mix"} ))
