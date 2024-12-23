import os
import socket
import time
import cv2
import queue
import heapq
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image
from threading import Thread
from pyzbar import pyzbar


matplotlib.use('TkAgg')

# 常量定义
TIME_FACTOR = 0.1 / 1.2
RESOLUTION = (480, 480)

# 图定义
GRAPH = {
        'A': {'B': 117, '01': 111},
        'B': {'A': 116, 'C': 121, '02': 121},
        'C': {'B': 120, 'D': 117, '03': 122},
        'D': {'C': 116, 'F': 114},
        'E': {'F': 25, 'I': 581, '04': 87, '07': 301},
        'F': {'D': 113, 'E': 24, 'G': 86},
        'G': {'F': 85, 'H': 300, '05': 163, '06': 157},
        'H': {'G': 299, 'J': 272, '06': 151, '08': 210, '09': 131},
        'I': {'E': 580, 'J': 120, 'K': 117, '07': 282, '10': 88},
        'J': {'H': 271, 'I': 119, '09': 161, '11': 120},
        'K': {'I': 116, '12': 61, '13': 243},
        '01': {'A': 110},
        '02': {'B': 120, '03': 122},
        '03': {'C': 121, '02': 121},
        '04': {'E': 86},
        '05': {'G': 162},
        '06': {'G': 156, 'H': 150},
        '07': {'E': 300, 'I': 281},
        '08': {'H': 209},
        '09': {'H': 112, 'J': 160},
        '10': {'I': 87},
        '11': {'J': 129},
        '12': {'K': 60},
        '13': {'K': 242}
        }

#节点相对方向
DIRECTION = {'A': {'B': 'w', '01': 'a'},
             'B': {'A': 's', 'C': 'w', '02': 'a'},
             'C': {'B': 's', 'D': 'd', '03': 'a'},
             'D': {'C': 'a', 'F': 'd'},
             'E': {'F': 's', 'I': 'd', '04': 'w', '07': 'd'},
             'F': {'D': 'a', 'E': 'w', 'G': 's'},
             'G': {'F': 'w', 'H': 'd', '05': 's', '06': 'd'},
             'H': {'G': 'a', 'J': 'd', '06': 'a', '08': 's', '09': 'd'},
             'I': {'E': 'a', 'J': 's', 'K': 'd', '07': 'a', '10': 'w'},
             'J': {'H': 'a', 'I': 'w', '09': 'a', '11': 's'},
             'K': {'I': 'a', '12': 'w', '13': 's'},
             '01': {'A': 'd'},
             '02': {'B': 'd', '03': 'w'},
             '03': {'C': 'd', '02': 's'},
             '04': {'E': 's'},
             '05': {'G': 'w'},
             '06': {'G': 'a', 'H': 'd'},
             '07': {'E': 'a', 'I': 'd'},
             '08': {'H': 'w'},
             '09': {'H': 'a', 'J': 'd'},
             '10': {'I': 's'},
             '11': {'J': 'w'},
             '12': {'K': 's'},
             '13': {'K': 'a'}
             }

#节点
NODES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13']

#内科：01    外科：02    急诊：03    口腔科：04    儿科：05    妇科：06    影像科：07
#检验科：08    骨科：09    耳鼻喉科：10    皮肤科：11    药房：12    眼科：13

#项目时长
TIME_LIST = {
        '01': 10,
        '02': 10,
        '03': 10,
        '04': 30,
        '05': 10,
        '06': 10,
        '07': 20,
        '08': 10,
        '09': 20,
        '10': 10,
        '11': 10,
        '12': 10,
        '13': 10
        }


def dijkstra(graph, start, end):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    predecessors = {vertex: None for vertex in graph}

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_vertex == end:
            path = []
            while current_vertex is not None:
                path.append(current_vertex)
                current_vertex = predecessors[current_vertex]
            return path[::-1]

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    return None


def traverse(medical_tests, graph, time_list):
    distance = []
    general_route = []
    num = 0

    for i in medical_tests:
        for k in graph[i]:
            graph[i][k] += time_list[i] / TIME_FACTOR

    for a in medical_tests:
        for b in medical_tests:
            if a != b:
                path = dijkstra(graph, a, b)
                if path:
                    general_route.append(path)
                    distance.append(sum(graph[path[i]][path[i + 1]] for i in range(len(path) - 1)))
                    num += 1

    return general_route, distance


def find_shortest_path(general_route, distance, medical_tests, position):
    final_route = []
    hd = []

    for i in range(len(general_route)):
        if general_route[i][0] == medical_tests[0]:
            hd.append(distance[i])

    if hd:
        s_num = distance.index(min(hd))
        final_route.append(general_route[s_num])
        medical_tests.remove(final_route[-1][0])

    for _ in range(len(medical_tests) - 1):
        hd = []
        for k in range(len(general_route)):
            if general_route[k][0] == final_route[-1][-1] and general_route[k][-1] in medical_tests:
                hd.append(distance[k])

        if hd:
            s_num = distance.index(min(hd))
            final_route.append(general_route[s_num])
            medical_tests.remove(final_route[-1][0])

    first_terminal = final_route[0][0]
    fist_path = dijkstra(GRAPH, position, first_terminal)
    final_route.insert(0, fist_path)

    return final_route


def show_direction(final_route, direction):
    ff = []
    i = 1

    # 合并最终路线列表
    for j in range(0, len(final_route)):
        ff += final_route[j]

    # 删除重复的顶点
    while i < len(ff):
        if ff[i] == ff[i - 1]:
            del ff[i]
        else:
            i += 1

    direction_list = []

    # 根据最终路线生成方向列表
    for k in range(0, len(ff) - 1):
        direction_list.append(direction[ff[k]][ff[k + 1]])
    return ff, direction_list


def all_values_zero(d):
    return all(value == 0 for value in d.values())


def user_to_do_acquisition(user_name):
    data_annotated = str(data_annotation(user_name, 'users'))
    client_socket.send(data_annotated.encode('utf-8'))
    data = eval(client_socket.recv(1024).decode('utf-8'))
    return data


def wait_time_acquisition(office_number, time_list):
    data_annotated = str(data_annotation(office_number, 'number_of_people_waiting'))
    client_socket.send(data_annotated.encode('utf-8'))
    try:
        wait_time = int(client_socket.recv(1024).decode('utf-8')) * time_list[office_number]
        return wait_time
    except Exception as e:
        print(f"Wait time acquisition error: {e}")
        return None


def data_annotation(data, annotation):
    return [data, annotation]



def path_calculate(graph_used, direction_used, time_list_used, position_used, test_need):
    test = ''
    keys = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13']
    values = [wait_time_acquisition(key, time_list_used) for key in keys]
    wait_time = dict(zip(keys, values))
    print(wait_time)


    if test_need:
        time_list_get = time_list_used.copy()
        if test != test_need:
            if not all_values_zero(wait_time):
                for test in test_need:
                    time_list_get[test] += wait_time[test]
            general_route, distance = traverse(test_need, graph_used, time_list_get)
            final_route = find_shortest_path(general_route, distance, test_need, position_used)
            ff, direction_list = show_direction(final_route, direction_used)

            if position_used in ff:
                key = direction_list[ff.index(position_used)]
                return key


def data_send(key, server_socket):
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr} has been established!")
    client_socket.send(key.encode('utf-8'))
    client_socket.close()


if __name__ == '__main__':
    last_scaned = {}

    #位置信息实际为机器自带值，这里仅是方便演示
    position = input('请输入位置信息')
    while position not in NODES:
        position = input('请输入位置信息')

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8888))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5001))
    server_socket.listen(1)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, RESOLUTION[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOLUTION[1])
    
    while True:
        ret, image = cap.read()

        if not ret:
            print("Error: Failed to capture frame.")
            break

        qrcodes = pyzbar.decode(image)

        for qrcode in qrcodes:
            user_name = qrcode.data.decode('utf-8')
            current_time = time.time()

            if user_name in last_scaned and current_time - last_scaned[user_name] < 10:
                continue

            last_scaned[user_name] = current_time

            medical_test_need_to_be_done = user_to_do_acquisition(user_name)
            key = path_calculate(GRAPH, DIRECTION, TIME_LIST, position, medical_test_need_to_be_done)
            data_send(key, server_socket)

        cv2.imshow('Camera', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()