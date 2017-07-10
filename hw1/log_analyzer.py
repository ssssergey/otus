#!/usr/bin/env python
# -*- coding: utf-8 -*-


# log_format ui_short '$remote_addr $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';

import os
import gzip
from collections import defaultdict
import itertools
import json
from datetime import datetime

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log"
}


def median(numbers):
    numbers = sorted(numbers)
    center = len(numbers) / 2
    if len(numbers) % 2 == 0:
        return sum(numbers[center - 1:center + 1]) / 2.0
    else:
        return numbers[center]


def parse_gzip(fullpath):
    f = gzip.open(fullpath, 'rb')
    file_content = f.readlines()
    mapping = defaultdict(list)
    for line in file_content:
        url = line.split(' ')[7]
        request_time = float(line.split(' ')[-1])
        mapping[url].append(request_time)
    values = mapping.values()
    values = list(itertools.chain(*values))
    total_count = len(values)
    total_time = sum(values)
    result_list = []
    for url, times in mapping.items():
        item = {'url': url,
                'count': len(times),
                'count_perc': "%.3f" % (float(len(times)) / float(total_count)),
                'time_avg': "%.3f" % (sum(times) / float(len(times))),
                'time_max': "%.3f" % max(times),
                'time_med': "%.3f" % median(times),
                'time_perc': "%.3f" % (float(sum(times)) / float(total_time)),
                'time_sum': "%.3f" % sum(times)
                }
        result_list.append(item)

    result_list = sorted(result_list, key=lambda x: x['time_avg'], reverse=True)
    json_str = json.dumps(result_list)

    new_report_name = datetime.now().strftime('report-%Y.%m.%d.html')
    with open(os.path.join(config['REPORT_DIR'], "report.html"), "r") as template, open(
            os.path.join(config['REPORT_DIR'], new_report_name), "w") as new_report:
        content = template.read()
        content = content.replace('$table_json', json_str)
        new_report.write(content)


def main():
    filename = os.listdir(config['LOG_DIR'])[0]
    fullpath = os.path.join(config['LOG_DIR'], filename)
    if fullpath.endswith('.gz'):
        parse_gzip(fullpath)
    else:
        pass


if __name__ == "__main__":
    main()
