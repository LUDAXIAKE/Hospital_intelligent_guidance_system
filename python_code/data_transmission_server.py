import socket
import json
import sqlite3


def data_queries(id, cursor, table_name):
    if table_name == 'users':
        query = 'SELECT data FROM {} WHERE id = ?'.format(table_name)
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            data = eval(row[0])
            print(data)
            return data

    if table_name == 'number_of_people_waiting':
        query = 'SELECT data FROM {} WHERE id = ?'.format(table_name)
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            print('row:', row)
            data = row[0]
            print(data)
            return data


if __name__ == '__main__':
    conn1 = sqlite3.connect('example.db')
    cursor1 = conn1.cursor()

    # 创建socket对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定IP地址和端口
    server_socket.bind(('localhost', 8888))
    # 监听端口
    server_socket.listen(1)

    print("服务器已启动，等待客户端连接...")

    # 接受客户端连接
    conn, addr = server_socket.accept()
    print(f"已连接客户端: {addr}")

    while True:
        # 接收客户端消息
        data_get = eval(conn.recv(1024).decode('utf-8'))
        print(f"收到客户端消息: {data_get}")
        if not data_get:
            break
        data = str(data_queries(data_get[0], cursor1, data_get[1]))
        # 发送回复消息
        conn.send(data.encode('utf-8'))

    # 关闭连接
    conn.close()
    server_socket.close()