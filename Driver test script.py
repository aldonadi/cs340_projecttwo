from aac_crud_driver import AnimalShelter
### CONNECT to the database

# create an animal shelter CRUD object, passing in credentials
high_security_shelter = AnimalShelter(
        { "username": "aacuser",
          "password": "i3-bNzTV6OF#V-'a00e+=iKh&JQs"
        }
)

print("FOR IMMEDEDIATE RELEASE: Notorious wombat brought to justice.")

# set up the data for the new record we will be creating
wombat_most_wanted = {
    "animal_type": "Wombat",
    "name": "Scratch McGrubbs",
    "breed": "Lasiorhinus latifrons",
    "age_upon_outcome": "4 years",
    "outcome_type": "Captured at long last",
    "outcome_subtype": "Nabbed by US Marshal",
    "color": "brown",
    "rec_num": 10001,
    "animal_id": "A799999",
    "location_lat": -31.9506,
    "location_long": 148.7583,
    "date_of_birth": "2019-05-15",
    "datetime": "2023-11-01T02:45:00",
    "sex_upon_outcome": "Male"
}
### READ a record that doesn't exist

# try to find the record we will be adding
# should return an empty list since it doesn't exist in the database yet
record = high_security_shelter.find(wombat_most_wanted)

if record == []:
    print("Ready to book the scoundrel.")
else:
    raise Exception("McGrubbs has already been booked!")
### CREATE a new record

# now create the new record and verify it is saved in the database
# we save the boolean returned by create to give an error if it failed
create_result = high_security_shelter.create(wombat_most_wanted)

if not create_result:
    raise Exception("Failed to create the new record!")
else:
    print("Booked. The long arm of the law triumphs again.")
### READ records that exist

booking_data = high_security_shelter.find(wombat_most_wanted)
print("Booking Data:")
print(booking_data)
### UPDATE a record

# make a dict of the fields with updated data

print("BREAKING: Dangerous inmate busted out by fellow outlaws!")

shocking_news = {
    "outcome_type": "Escaped",
    "outcome_subtype": "Sprung by posse"
}

# update the record with the new data
num_updated = high_security_shelter.update(wombat_most_wanted, shocking_news)

if num_updated != 1:
    raise Exception("No matching records to update!")
### DELETE a record

print("Bribe accepted; let's forget this ever happened...")

the_wombat = { "name": "Scratch McGrubbs" }

num_deleted = high_security_shelter.delete(the_wombat)

if num_deleted != 1:
    raise Exception("Failed to destroy the evidence!")

print("Scratch McGrubbs wins again.")


