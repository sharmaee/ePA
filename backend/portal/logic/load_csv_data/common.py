def read_data_from_csv(filepath):
    with open(filepath, 'r') as f:
        raw_data = f.readlines()
    return raw_data


def get_raw_requirements(raw_data, header_fields, header_start):
    requirements = []
    for line in raw_data:
        if line.startswith(header_start):
            continue
        record = dict(zip(header_fields, line.rstrip('\n').split(',')))
        requirements.append(record)
    return requirements
