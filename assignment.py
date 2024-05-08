import json
import csv
import dateutil.parser

# Initialize the dictionaries
patient_conditions = {}
encounter_times = {}

# Load the Condition.ndjson file
with open('Condition.ndjson', 'r') as f:
    for line in f:
        data = json.loads(line)
        patient_id = data['subject']['reference'].split('/')[-1]
        encounter_id = data['encounter']['reference'].split('/')[-1]
        if patient_id not in patient_conditions:
            patient_conditions[patient_id] = []
        patient_conditions[patient_id].append((encounter_id, data))

# Load the Encounter.ndjson and EncounterICU.ndjson files and assign times to conditions
for filename in ['Encounter.ndjson', 'EncounterICU.ndjson']:
    with open(filename, 'r') as f:
        for line in f:
            data = json.loads(line)
            encounter_id = data['id']
            encounter_time = dateutil.parser.parse(data['period']['start']).timestamp()
            encounter_times[encounter_id] = encounter_time

# Create the CSV file
with open('output.csv', 'w', newline='') as csvfile:
    fieldnames = ['pid', 'time', 'code', 'description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for patient_id, conditions in patient_conditions.items():
        for encounter_id, condition in conditions:
            writer.writerow({
                'pid': patient_id,
                'time': encounter_times.get(encounter_id, ''),
                'code': condition['code']['coding'][0]['code'],
                'description': condition['code']['coding'][0]['display']
            })