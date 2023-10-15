import json

import numpy as np
import requests
import datetime
import matplotlib.pyplot as plt
from collections import Counter

def fun1():
    payload = {'jql': 'project=KAFKA AND status=Closed ORDER BY createdDate', 'maxResults': '1000',
               'fields': 'resolutiondate,created'}

    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
    data = json.loads(response.text)
    count = len(data['issues'])
    list_data = []
    for elem in data['issues']:
        created = elem['fields']['created']
        resolutiondate = elem['fields']['resolutiondate']
        created_t = datetime.datetime.strptime(created, '%Y-%m-%dT%H:%M:%S.%f%z')
        resolutiondate_t = datetime.datetime.strptime(resolutiondate, '%Y-%m-%dT%H:%M:%S.%f%z')
        time = resolutiondate_t - created_t
        list_data.append(time.total_seconds() / (3600 * 24))

    max_el = max(list_data)

    plt.hist(list_data, color='blue', edgecolor='black', bins=25)
    plt.title('Гистограмма 1')
    plt.xlabel('Время решения (дни)')
    plt.xticks(np.arange(0, int(max_el), int(max_el / 20)))
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    list_data.sort()
    middle_index = int(count / 1.2)
    first_patr = list_data[:middle_index]
    max_el = max(first_patr)
    plt.hist(first_patr, color='green', edgecolor='black', bins=25)
    plt.title('Гистограмма 2')
    plt.xlabel('Время решения (дни)')
    plt.xticks(np.arange(0, int(max_el), int(max_el / 20)))
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()


def fun2():
    list_open = []
    list_in_progress = []
    list_resolved = []
    list_resolved_day = []
    list_reopened = []
    list_patch_available = []
    list_patch_available_day = []

    payload = {'jql': 'project=KAFKA AND status=Closed ORDER BY createdDate', 'maxResults': '1000',
               'expand': 'changelog',
               'fields': 'changelog,created'}

    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
    data = json.loads(response.text)

    time_start = None
    time_stop = None

    for elem in data['issues']:
        sum_time_open = 0
        sum_time_in_progress = 0
        sum_time_resolved = 0
        sum_time_reopened = 0
        sum_time_patch_available = 0

        time_start = datetime.datetime.strptime(elem['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
        for history in elem['changelog']['histories']:
            history_time = datetime.datetime.strptime(history['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
            for item in history['items']:
                if item['field'] == 'status':
                    time_stop = history_time
                    time = (time_stop - time_start).total_seconds()
                    status = item['fromString']
                    if status == 'Open':
                        sum_time_open = sum_time_open + time
                    elif status == 'In Progress':
                        sum_time_in_progress = sum_time_in_progress + time
                    elif status == 'Resolved':
                        sum_time_resolved = sum_time_resolved + time
                    elif status == 'Reopened':
                        sum_time_reopened = sum_time_reopened + time
                    elif status == 'Patch Available':
                        sum_time_patch_available = sum_time_patch_available + time
                    time_start = time_stop

        if sum_time_open != 0:
            list_open.append(sum_time_open / (3600 * 24))
        if sum_time_patch_available != 0:
            list_patch_available_day.append(sum_time_patch_available / (3600 * 24))
            list_patch_available.append(sum_time_patch_available / 3600)
        if sum_time_reopened != 0:
            list_reopened.append(sum_time_reopened / (3600 * 24))
        if sum_time_resolved != 0:
            list_resolved.append(sum_time_resolved)
            list_resolved_day.append(sum_time_resolved / (3600 * 24))
        if sum_time_in_progress != 0:
            list_in_progress.append(sum_time_in_progress / (3600 * 24))

    # print(list_open)
    # print(list_resolved)
    # print(list_reopened)
    # print(list_in_progress)
    # print(list_patch_available)

    ###### Open
    plt.hist(list_open, color='blue', edgecolor='black', bins=30)
    plt.title('Диаграмма Open 1')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    list_open.sort()
    middle_index = int(len(list_open) / 1.2)
    first_patr = list_open[:middle_index]
    plt.hist(first_patr, color='blue', edgecolor='black', bins=80)
    plt.title('Диаграмма Open 2')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    ###### Resolved
    plt.hist(list_resolved_day, color='green', edgecolor='black', bins=30)
    plt.title('Диаграмма Resolved 1')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    list_resolved.sort()
    middle_index = int(len(list_resolved) / 1.6)
    first_patr = list_resolved[:middle_index]
    plt.hist(first_patr, color='green', edgecolor='black', bins=80)
    plt.title('Диаграмма Resolved 2')
    plt.xlabel('Время решения (секунды)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    middle_index = int(len(list_resolved) / 1.8)
    second_patr = list_resolved[:middle_index]
    plt.hist(second_patr, color='green', edgecolor='black', bins=80)
    plt.title('Диаграмма Resolved 3')
    plt.xlabel('Время решения (секунды)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    ###### Reopened
    plt.hist(list_reopened, color='yellow', edgecolor='black', bins=175)
    plt.title('Диаграмма Reopened')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    #### In Progress
    plt.hist(list_in_progress, color='purple', edgecolor='black', bins=50)
    plt.title('Диаграмма In Progress 1')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    list_in_progress.sort()
    second_patr = list_in_progress[:len(list_in_progress) - 4]
    plt.hist(second_patr, color='purple', edgecolor='black', bins=80)
    plt.title('Диаграмма In Progress 2')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    ###### Patch Available
    plt.hist(list_patch_available_day, color='orange', edgecolor='black', bins=30)
    plt.title('Диаграмма Patch Available 1')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    list_patch_available.sort()
    middle_index = int(len(list_patch_available) / 1.3)
    second_patr = list_patch_available[:middle_index]
    plt.hist(second_patr, color='orange', edgecolor='black', bins=40)
    plt.title('Диаграмма Patch Available 2')
    plt.xlabel('Время решения (часы)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()



def fun3():
    # за последние 90 дней

    NUM_DAYS = 90

    list_open_by_day = []
    list_dates = []
    current_date = datetime.date.today()

    for i_day in range(0, -NUM_DAYS, -1):
        jql_str = f'project=KAFKA AND created>startOfDay("{i_day}d") AND created<startOfDay("{i_day + 1}d")'
        payload = {'jql': jql_str, 'maxResults': '1000',
                   'fields': 'created'}
        response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
        data = json.loads(response.text)
        list_open_by_day.append(data['total'])
        date = current_date + datetime.timedelta(days=i_day)
        list_dates.append(date)

    list_open_by_day.reverse()

    list_dates.reverse()

    plt.plot(list_open_by_day, linewidth=3.0, color='red')
    # plt.title(f'График созданных задач за последние {NUM_DAYS} дней')
    # plt.xlabel('Дата')
    # plt.ylabel('Количество задач')

    # x_list=[]
    # for i in range(NUM_DAYS):
    # x_list.append(i)

    # plt.xticks (x_list,labels=list_dates,rotation=45)
    # plt.show()

    #####
    close_list_dates = []
    payload = {'jql': 'project=KAFKA AND status=Closed ORDER BY createdDate', 'maxResults': '1000',
               'expand': 'changelog',
               'fields': 'changelog'}

    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
    data = json.loads(response.text)

    for elem in data['issues']:
        for history in elem['changelog']['histories']:
            history_time = datetime.datetime.strptime(history['created'], '%Y-%m-%dT%H:%M:%S.%f%z').date()
            for item in history['items']:
                if item['field'] == 'status':
                    status = item['toString']
                    if status == 'Closed':
                        close_list_dates.append(history_time)

    close_list_dates.sort()
    close_list_dates.reverse()
    # даты закрытия задач
    # for i in close_list_dates:
    #     print(i)

    current_date = datetime.date.today()

    list_close_by_day = []
    for i in range(NUM_DAYS):
        date = current_date - datetime.timedelta(days=i)
        k = 0
        for el in close_list_dates:
            if el == date:
                k = k + 1
            if el < date:
                break
        list_close_by_day.append(k)

    list_close_by_day.reverse()

    plt.plot(list_close_by_day, linewidth=3.0, color='green')
    plt.title(f'Графики открытых и закрытых задач за последние {NUM_DAYS} дней')
    plt.xlabel('Дата')
    plt.ylabel('Количество задач')

    x_list = []
    for i in range(NUM_DAYS):
        x_list.append(i)

    plt.xticks(x_list, labels=list_dates, rotation=90, size=8)
    plt.show()

    summary_list_open = []
    summary_list_close = []
    summ = 0
    for elem in list_open_by_day:
        summ = summ + elem
        summary_list_open.append(summ)

    summ = 0
    for elem in list_close_by_day:
        summ = summ + elem
        summary_list_close.append(summ)

    plt.plot(summary_list_open, linewidth=3.0, color='red')
    plt.plot(summary_list_close, linewidth=3.0, color='green')
    plt.title(f'Графики накопления открытых и закрытых задач за последние {NUM_DAYS} дней')
    plt.xlabel('Дата')
    plt.ylabel('Количество задач')

    plt.xticks(x_list, labels=list_dates, rotation=90, size=8)
    plt.show()



def fun4():
    payload = {'jql': 'project=KAFKA AND NOT assignee=null AND NOT reporter=null', 'maxResults': '1',
               'fields': 'reporter,assignee'}

    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
    data = json.loads(response.text)
    total = int(data['total'])

    list_users = []

    for start_at in range(0, total, 1000):
        payload = {'jql': 'project=KAFKA AND NOT assignee=null AND NOT reporter=null', 'maxResults': '1000',
                   'startAt': f'{start_at}',
                   'fields': 'reporter,assignee'}

        response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
        data = json.loads(response.text)
        for elem in data['issues']:
            reporter = elem['fields']['reporter']['key']
            assignee = elem['fields']['assignee']['key']
            if reporter == assignee:
                list_users.append(reporter)

    counted_values = Counter(list_users)
    arr = counted_values.most_common(30)
    list_users_30 = []
    list_count_30 = []
    for elem in arr:
        list_users_30.append(elem[0])
        list_count_30.append(elem[1])

    plt.plot(list_count_30, linewidth=3.0, color='green')
    plt.title(f'График пользователи и задачи')
    plt.xlabel('Пользователь')
    plt.ylabel('Количество задач')
    x_list = []
    for i in range(30):
        x_list.append(i)
    plt.xticks(x_list, labels=list_users_30, rotation=45, size=8)
    plt.show()


def fun5():
    list_5 = []
    payload = {'jql': 'project=KAFKA AND status=Closed AND NOT assignee=null', 'maxResults': '1000',
               'fields': 'assignee'}

    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
    data = json.loads(response.text)
    for elem in data['issues']:
        assignee = elem['fields']['assignee']['key']
        list_5.append(assignee)

    counted_values = Counter(list_5)
    print(counted_values)

    ##################

    payload = {'jql': 'project=KAFKA AND status=Closed AND assignee=nehanarkhede', 'maxResults': '1000',
               'expand': 'changelog',
               'fields': 'resolutiondate,created'}

    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
    data = json.loads(response.text)

    times_list = []

    for elem in data['issues']:
        resolutiondate = datetime.datetime.strptime(elem['fields']['resolutiondate'], '%Y-%m-%dT%H:%M:%S.%f%z')
        created = datetime.datetime.strptime(elem['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
        for hist in elem['changelog']['histories']:
            created_hist = datetime.datetime.strptime(hist['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
            for item in hist['items']:
                if item['field'] == 'assignee' and item['to'] == 'nehanarkhede':
                    created = created_hist

        time_delta = (resolutiondate - created).total_seconds()
        if time_delta > 0:
            times_list.append(time_delta / 3600)

    plt.hist(times_list, bins=100, edgecolor='black', color='blue')

    plt.title('Гистограмма пользователь nehanarkhede')
    plt.xlabel('Время решения (часы)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()


def fun6():
    payload = {'jql': 'project=KAFKA', 'maxResults': '1', 'fields': 'priority'}
    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
    data = json.loads(response.text)
    total = int(data['total'])

    list_prio = []

    for start_at in range(0, total, 1000):
        payload = {'jql': 'project=KAFKA', 'maxResults': '1000', 'startAt': f'{start_at}', 'fields': 'priority'}

        response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
        data = json.loads(response.text)
        for elem in data['issues']:
            list_prio.append(elem['fields']['priority']['name'])

    # print(list_prio)
    # print(set(list_prio))
    counted_values = Counter(list_prio)

    list_x = ['Trivial', 'Minor', 'Major', 'Critical', 'Blocker']
    list_y = []
    list_y.append(counted_values['Trivial'])
    list_y.append(counted_values['Minor'])
    list_y.append(counted_values['Major'])
    list_y.append(counted_values['Critical'])
    list_y.append(counted_values['Blocker'])

    plt.plot(list_y, linewidth=3.0, color='green')
    plt.title(f'График количество задач по степени серьезности')
    plt.xlabel('Приоритет')
    plt.ylabel('Количество задач')
    x_list = [0, 1, 2, 3, 4]
    plt.grid(True)
    plt.yticks(list_y)
    plt.xticks(x_list, labels=list_x)
    plt.show()



while 1:
    mode = input("Какую диаграмму строить?\nВыберите: 1,2,3,4,5,6? 0-exit\n>")
    if mode == '1':
        fun1()
    elif mode == '2':
        fun2()
    elif mode == '3':
        fun3()
    elif mode == '4':
        fun4()
    elif mode == '5':
        fun5()
    elif mode == '6':
        fun6()
    elif mode == '0':
        exit(0)


