import clize
import json
import os
import csv
import sys

class BadRecordError(ValueError):
    pass

def fraction_pushable_objects(dataset):
    content_bytes = {
        'pushable': 0,
        'third_party': 0,
    }

    objects = {
        'pushable': 0,
        'third_party': 0,
    }

    for obj in dataset['objects']:
        key = 'pushable' if obj['is_first_party'] else 'third_party'
        content_bytes[key] += obj['bytes']
        objects[key] += obj['count']

    if -1 in content_bytes.values():
        raise BadRecordError("Bytes should not be negative")

    total_objects = sum(objects.values())
    total_bytes = sum(content_bytes.values())

    first_party = dataset['domain']
    return (first_party,
            objects['pushable'],
            content_bytes['pushable'],
            total_objects,
            total_bytes)


def analyse_batch_data(origin_stats_dir):
    for dataset_file in os.listdir(origin_stats_dir):
        filepath = f'{origin_stats_dir}/{dataset_file}'
        with open(filepath) as f:
            try:
                dataset = json.load(f)
            except json.decoder.JSONDecodeError as e:
                sys.stderr.write(f"failed to load {filepath}:\n{e}\n")
                sys.stderr.flush()
                continue

            try:
                row = fraction_pushable_objects(dataset)
                yield row
            except BadRecordError as e:
                continue

def main(origin_stats_dir):
    """For a dataset of domains, batch process the domain stats files
    from a list of [domain, occurences, response size, pushability] into
    rows of [first party domain, fraction pushable objects, fraction pushable
    bytes

    origin_stats_dir: location of the processed stats file

    """
    writer = csv.writer(sys.stdout, delimiter=',')
    writer.writerow(["first party domain name",
                     "pushable objects",
                     "pushable bytes",
                     "total objects",
                     "total bytes"])
    for row in analyse_batch_data(origin_stats_dir):
        writer.writerow(row)

if __name__ == '__main__':
    clize.run(main)
