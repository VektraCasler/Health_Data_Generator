Scripts included within this toolset:

-------
main.py
-------

Eventually, this will be a master script to launch all others in sequence.  This will create all files as necessary with default values.

-------------------
person_generator.py
-------------------

This is a tool for generating a list of people.  Entries for each person include:

- First Name
- Surname
- Middle Name
- Suffix (II, III, Jr., Sr.)

- Social Security Number (SSN)
- Medical Record Number (MRN)

- Sex
- Date of Birth (DOB)
- Race
- Ethnicity

- Street Address
- City
- County
- State
- Country

- Cell Phone Number
- Work Phone Number
- Home Phone Number
- Email Address

Note: Where possible data is generated from weighted tables pulled from documented web sources.  See resources.txt files in each of REFERENCE folders for the source web addresses.

Future Additions:
- Explore the idea of record generation column-by-column, may facilitate faster generation by allowing for columns to be turned off.
- Additional column: Gender identity column



---------------------
provider_generator.py  (not yet created)
---------------------

This test will skim off a number of appropriately aged individuals from the OUTPUT/person_list.csv file and add additional columns to each entry.  These additional data fields will include:

- Provider Number
- Provider Type (nurse, doctor, phlebotomist, med-tech, PA)
- Provider ID (per CMS guidelines -- 00X0000 or 0000000)
- Provider Location
- Specialty

<more to follow>

Note: It would be nice to generate doctors based on weighted values as to their specialty, if such information exists.


-----------------------------
hospital_system_generation.py (not yet created)
-----------------------------

This script will generate a number of hospital buildings to include: emergency rooms, general floors, specialty floors, central labs, draw stations, blood banks, and stat labs.

Note: It might be possible to model a couple of different styles of health-care systems, based on expected patient bed count.  


-----------------------
data_curve_generator.py
-----------------------

Currently, this tool is a test of normal curve distribution randomization, with a matplotlib graph to verify.  Eventually, I would like to make this a collection of mathematical model distribution equations, which would be callable by other scripts using the import command.  That way, referencing our LOINC code list, we could choose the appropriate math model for data randomization during test result generation.

Math models to emulate:

- Normal Distribution
- Inverse relationship distribution
- Skewed/tailed Normal distributions

<more to follow>


------------------------
test_result_generator.py  (not yet created)
------------------------

This will be the final generator, drawing in pregenerated resources from all other scripts.  It will first check for outputs from the prior scripts, running those as necessary, in order to generate any missing data.  Finally, it will pull all output resources together, choose important locations, and begin generating patient stays in care facilities.  For each day of inpatient stay, it will generate randomly chosen lab tests.  Outpatient testing can likewise be incorporated into this list.

Ultimately, the final output will be a highly complex, multi-field flat database (CSV), with as many entries as the tool-user decides.