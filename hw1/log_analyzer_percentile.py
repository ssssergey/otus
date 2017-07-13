#!/usr/bin/env python
# -*- coding: utf-8 -*-


# log_format ui_short '$remote_addr $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';
import glob
import os
import gzip
import re
from collections import defaultdict
import itertools
import json
from datetime import datetime
import math

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log"
}

log_pattern = re.compile(r'\[.+?\] "[A-Z]+? (/.+?)(?= HTTP).*? ([(\d\.)]+)$')


def percentile(numbers, percent, key=lambda x: x):
    """
    Вычисляет персентиль
    """
    if not numbers:
        return None
    k = (len(numbers) - 1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return key(numbers[int(k)])
    d0 = key(numbers[int(f)]) * (c - k)
    d1 = key(numbers[int(c)]) * (k - f)
    return d0 + d1


def get_file():
    path_template = os.path.join(config['LOG_DIR'], '*.gz')
    paths = glob.iglob(path_template)
    mapping = ((datetime.strptime(path[-11:-3], '%Y%m%d'), path) for path in paths)
    return max(mapping)[1]


def parse(file_object):
    """ Парсим содержимое файла """
    mapping = defaultdict(list)
    total_count = 0
    total_time = 0
    # Делаем маппинг url к списку всех времен запросов к нему
    for line in file_object:
        groups = log_pattern.search(line.strip())
        if groups:
            url = groups.group(1)
            request_time = float(groups.group(2))
            mapping[url].append(request_time)
            total_count += 1
            total_time += request_time

    # Собираем список urls с расчитанными для каждого показателями
    result_list = []
    for url, times in mapping.items():
        item = {'url': url,
                'count': len(times),
                'count_perc': "%.3f" % (float(len(times)) / float(total_count)),
                'time_max': "%.3f" % max(times),
                'time_p50': "%.3f" % percentile(times, 0.5),
                'time_p95': "%.3f" % percentile(times, 0.95),
                'time_p99': "%.3f" % percentile(times, 0.99),
                'time_perc': "%.3f" % (float(sum(times)) / float(total_time)),
                'time_sum': "%.3f" % sum(times)
                }
        result_list.append(item)
    result_list = sorted(result_list, key=lambda x: x['time_sum'], reverse=True)
    json_str = json.dumps(result_list[:config['REPORT_SIZE']])
    return json_str


def main():
    # Формируем полный путь для будущего репорта
    new_report_name = datetime.now().strftime('report-%Y.%m.%d.html')
    new_report_path = os.path.join(config['REPORT_DIR'], new_report_name)
    # Начинаем парсинг, только если репорта с таким именем не существует
    if not os.path.exists(new_report_path):
        log_path = get_file()
        if log_path.endswith('.gz'):
            # Для gzip
            f = gzip.open(log_path, 'rb')
        else:
            # Для plain
            f = open(log_path, 'r')
        json_str = parse(f)
        f.close()

        # Формируем html-файл
        with open(os.path.join(config['REPORT_DIR'], "report.html"), "r") as template, open(new_report_path,
                                                                                            "w") as new_report:
            content = template.read()
            content = content.replace('$table_json', json_str)
            new_report.write(content)
        print 'File has been created.'
    else:
        print 'File already exists.'


if __name__ == "__main__":
    main()
