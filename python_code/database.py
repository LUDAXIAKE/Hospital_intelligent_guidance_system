import sqlite3
import json

# 创建数据库连接
conn = sqlite3.connect('example.db')
cursor1 = conn.cursor()

# 插入数据
user_name1 = 'patient1'
data1 = ['01', '04', '06', '07', '12', '13']
user_name2 = 'patient2'
data2 = ['05', '07', '08', '12']

def data_filter(user_name, data, cursor):
    cursor.execute('SELECT data FROM users WHERE user_name = ?', (user_name,))
    row = cursor.fetchone()

    if row:
        data = json.loads(row[0])
        if data == []:
            cursor.execute('DELETE FROM users WHERE user_name = ?', (user_name,))
            print(f"Deleted user with user_name {user_name} because data is empty.")
            conn.commit()
    else:
        data_json = json.dumps(data)  # 将列表转换为JSON字符串

        cursor.execute('''
        INSERT INTO users (user_name, data)
        VALUES (?, ?)
        ''', (user_name, data_json))

        cursor.execute('SELECT * FROM users WHERE user_name = ?', (user_name,))
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        conn.commit()


def completed_test_deleter(user_name, cursor):
    cursor.execute('SELECT data FROM users WHERE user_name = ?', (user_name,))
    row = cursor.fetchone()

    if row:
        # 读取并修改数据
        data = json.loads(row[0])
        print(f"Original data: {data}")
        if data == []:
            cursor.execute('DELETE FROM users WHERE user_name = ?', (user_name,))
            print(f"Deleted user with user_name {user_name} because data is empty.")
            conn.commit()

        del data[0]
        new_data_json = json.dumps(data)

        cursor.execute('''
        UPDATE users
        SET data = ?
        WHERE user_name = ?
        ''', (new_data_json, user_name))

        cursor.execute('SELECT * FROM users WHERE user_name = ?', (user_name,))
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        # 提交事务
        conn.commit()
    else:
        print(f"No user found with user_name {user_name}")


def data_queries(user_name, cursor):
    cursor.execute('SELECT data FROM users WHERE user_name = ?', (user_name,))
    row = cursor.fetchone()

    if row:
        cursor.execute('SELECT data FROM users WHERE user_name = ?', (user_name,))
        row = cursor.fetchone()
        data = json.loads(row[0])
        print(data)
        return data


if __name__ == '__main__':
    print("data_filter")