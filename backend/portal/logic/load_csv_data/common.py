def read_data_from_csv(filepath):
    with open(filepath, 'r') as f:
        raw_data = f.readlines()
    return raw_data


def get_rows_from_csv_data(raw_data, header_fields):
    requirements = []
    for line in raw_data[1:]:
        record = dict(zip(header_fields, line.rstrip('\n').split(',')))
        requirements.append(record)
    return requirements
