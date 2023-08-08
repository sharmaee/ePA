# get file from s3 /data/raw_data/requirements.csv
# load file into memory
# create list of objects to save
# for each line in file:
    # split line into columns
    # assign values to columns
    # split column 3 on ; and create separate dicts for each state
    # split column 2 on ; and create separate dicts for each insurance plan type
    # if value in column 4 get json from s3 and write to requirements_flow or set to empty string
    # if value in column 5 get json from s3 and write to requirements_checklist or set to empty string
    # for each state:
        # for each insurance plan type:
            # create url slug
            # create dict of data
                # "model": "portal.PriorAuthRequirement"
                # "fields": {
                    # "url_slug": url_slug
                    # "insurance_provider": column 1
                    # "insurance_plan_type": insurance plan type
                    # "insurance_coverage_state": state
                    # "requirements_flow": requirements_flow
                    # "requirements_checklist": requirements_checklist
                    # "requirements_flow_file_location": column 6
                # }
             # add to list of objects to save
# add field pk to each dict based on index in list of objects to save + 1
# write list of objects to save to json file requirements.json
# upload file to s3 /data/fixtures/requirements.json

# get file from portal/fixtures/data/raw_data/requirements.csv
# load file into memory
# create list of objects to save
# for each line in file:
    # split line into columns
    # assign values to columns
    # split column 3 on ; and create separate dicts for each state
    # split column 2 on ; and create separate dicts for each insurance plan type
    # if value in column 4 get json from portal/fixtures/data/graphs/ + value in column and write to requirements_flow or set to empty string
    # if value in column 5 get json from portal/fixtures/data/checklists/ + value in column and write to requirements_checklist or set to empty string
    # for each state:
        # for each insurance plan type:
            # create url slug
            # create dict of data
                # "model": "portal.PriorAuthRequirement"
                # "fields": {
                    # "url_slug": url_slug
                    # "insurance_provider": column 1
                    # "insurance_plan_type": insurance plan type
                    # "insurance_coverage_state": state
                    # "requirements_flow": requirements_flow
                    # "requirements_checklist": requirements_checklist
                    # "requirements_flow_file_location": column 6
                # }
             # add to list of objects to save
# add field pk to each dict based on index in list of objects to save + 1
# write list of objects to save to json file portal/fixtures/requirements.json

def get_file_header(f):
    header_fields = [
        'medication',
        'insurance_provider',
        'insurance_plan_type',
        'insurance_coverage_state',
        'requirements_flow',
        'requirements_checklist',
        'requirements_flow_file_location'
    ]
    for line in f:
        if line.startswith("Drug"):
            break

    return header_fields

def get_raw_data():
    with open('portal/fixtures/data/raw_data/requirements.csv', 'r') as f:
        raw_data = f.readlines()
    return raw_data


def get_requirements(raw_data):
    pass

