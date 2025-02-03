#!/usr/bin/python3

from aac_crud_driver import AnimalShelter

a = AnimalShelter()
r = list(a.find( { "breed": "Domestic Shorthair Mix"} ))

print(r)
