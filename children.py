from flask import Flask, request, render_template, redirect, url_for, session
import pymysql
import bcrypt
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # 用于加密会话

# 数据库连接配置
db_config = {
    'host': '27739my894.zicp.vip',
    'port': 3306,
    'user': 'RewardsDB',
    'password': 'zBVf-ikN4ChYp5Ol',
    'database': 'RewardsDB'
}

# 数据库连接
def get_db_connection():
    return pymysql.connect(**db_config)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                session['user_id'] = user['id']
                session['role'] = user['role']
                session.permanent = True  # 设置会话为永久

                if user['role'] == 'admin':
                    return redirect(url_for('dashboard'))
                else:
                    return redirect(url_for('child_dashboard'))
            else:
                return render_template('login.html', error="用户名或密码错误")

        return render_template('login.html', error="用户名或密码错误")

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT COUNT(*) AS count FROM users")
    user_count = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) AS count FROM users WHERE role = 'admin'")
    admin_count = cursor.fetchone()['count']

    show_register_button = user_count == 0 or admin_count == 0

    cursor.close()
    conn.close()

    return render_template('login.html', show_register_button=show_register_button)

# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                session['user_id'] = user['id']
                session['role'] = user['role']
                session.permanent = True  # 设置会话为永久

                if user['role'] == 'admin':
                    return redirect(url_for('dashboard'))
                else:
                    return redirect(url_for('child_dashboard'))
            else:
                return render_template('login.html', error="用户名或密码错误")

        return render_template('login.html', error="用户名或密码错误")

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT COUNT(*) AS count FROM users")
    user_count = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) AS count FROM users WHERE role = 'admin'")
    admin_count = cursor.fetchone()['count']

    show_register_button = user_count == 0 or admin_count == 0

    cursor.close()
    conn.close()

    return render_template('login.html', show_register_button=show_register_button)

# 注销
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('login'))

# 仪表盘页面
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # 获取当前用户信息
    cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()

    # 获取所有任务
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    # 获取不是管理员的用户（即孩子）的积分信息
    cursor.execute("SELECT * FROM users WHERE role = 'child'")
    children = cursor.fetchall()

    # 获取每个孩子的积分记录
    transactions = {}
    for child in children:
        cursor.execute("SELECT * FROM transactions WHERE username = %s", (child['username'],))
        transactions[child['username']] = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('dashboard.html', user=user, tasks=tasks, children=children, transactions=transactions)

# 管理员加分操作
@app.route('/admin/add_points', methods=['POST'])
def add_points():
    if 'role' in session and session['role'] == 'admin':
        user_id = request.form['user_id']
        task_id = request.form['task_id']

        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # 获取任务积分和描述
        cursor.execute("SELECT points, description FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
        points = task['points'] if task else 0
        task_description = task['description'] if task else ''

        # 获取用户信息
        cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        username = user['username'] if user else ''

        # 更新用户积分
        cursor.execute("UPDATE users SET points = points + %s WHERE id = %s", (points, user_id))
        conn.commit()

        # 记录交易
        cursor.execute("INSERT INTO transactions (username, task_id, description, points_change) VALUES (%s, %s, %s, %s)",
                       (username, task_id, task_description, points))
        conn.commit()

        # 记录到TXT文件
        with open('points_log.txt', 'a') as f:
            f.write(f"User ID: {user_id}, Task ID: {task_id}, Points Change: {points}, Date: {datetime.now()}\n")

        cursor.close()
        conn.close()

        return redirect(url_for('dashboard'))

    return '无权限操作。'

# 兑换积分
@app.route('/reward', methods=['POST'])
def reward():
    if 'user_id' in session:
        user_id = request.form['user_id']
        reward_id = request.form['reward_id']

        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # 获取奖励项目
        cursor.execute("SELECT * FROM rewards WHERE id = %s", (reward_id,))
        reward = cursor.fetchone()

        # 获取用户积分
        cursor.execute("SELECT points FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        message = ""
        if user and reward:
            if user['points'] >= reward['points_needed']:
                # 扣除积分
                new_points = user['points'] - reward['points_needed']
                cursor.execute("UPDATE users SET points = %s WHERE id = %s", (new_points, user_id))

                # 添加兑换记录
                cursor.execute("INSERT INTO reward_logs (user_id, description, timestamp) VALUES (%s, %s, %s)",
                               (user_id, f"兑换 {reward['description']}，消费了 {reward['points_needed']} 分", datetime.now()))

                message = "兑换成功！"
            else:
                message = "积分不足，无法兑换。"

            # 添加兑换记录（包括失败消息）
            cursor.execute("INSERT INTO reward_logs (user_id, description, timestamp) VALUES (%s, %s, %s)",
                           (user_id, message, datetime.now()))
        else:
            message = "无效的奖励项目或用户信息。"
            cursor.execute("INSERT INTO reward_logs (user_id, description, timestamp) VALUES (%s, %s, %s)",
                           (user_id, message, datetime.now()))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('child_dashboard'))

    return redirect(url_for('login'))

# 查看积分奖励记录
@app.route('/rewards_log', methods=['GET'])
def rewards_log():
    if 'role' in session and session['role'] == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # 从 users 表中获取 role 为 'child' 的 username
        cursor.execute("SELECT username FROM users WHERE role = 'child'")
        user_rows = cursor.fetchall()
        usernames = [row['username'] for row in user_rows]

        # 从 tasks 表中获取所有的 description
        cursor.execute("SELECT description FROM tasks")
        task_rows = cursor.fetchall()
        descriptions = [row['description'] for row in task_rows]

        # 获取搜索的 username，如果有的话
        search_username = request.args.get('search_username', '')

        # 根据用户搜索请求过滤记录
        if search_username:
            cursor.execute("""
                SELECT t.username, t.description, t.points_change, t.timestamp
                FROM transactions t
                WHERE t.username = %s
                ORDER BY t.timestamp DESC
            """, (search_username,))
        else:
            cursor.execute("""
                SELECT t.username, t.description, t.points_change, t.timestamp
                FROM transactions t
                ORDER BY t.timestamp DESC
            """)
        records = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('rewards_log.html', usernames=usernames, descriptions=descriptions, records=records)

    return '无权限访问。'

# 儿童仪表盘
@app.route('/child_dashboard', methods=['GET'])
def child_dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # 获取用户信息，包括名字
        cursor.execute("SELECT username, points FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        total_points = user['points'] if user else 0
        username = user['username'] if user else ''

        # 获取消费积分项目
        cursor.execute("SELECT * FROM rewards WHERE type = 'consumption' ORDER BY points_needed ASC")
        rewards = cursor.fetchall()

        # 获取兑换记录
        cursor.execute("SELECT * FROM reward_logs WHERE user_id = %s ORDER BY timestamp DESC", (user_id,))
        logs = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('child_dashboard.html', username=username, total_points=total_points, rewards=rewards, logs=logs, user_id=user_id)

    return redirect(url_for('login'))


# 兑换积分
@app.route('/redeem', methods=['POST'])
def redeem():
    if 'user_id' in session:
        user_id = request.form['user_id']
        reward_id = request.form['reward_id']

        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # 获取奖励项目
        cursor.execute("SELECT * FROM rewards WHERE id = %s", (reward_id,))
        reward = cursor.fetchone()

        # 获取用户积分
        cursor.execute("SELECT points FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        message = ""
        if user and reward:
            if user['points'] >= reward['points_needed']:
                # 扣除积分
                new_points = user['points'] - reward['points_needed']
                cursor.execute("UPDATE users SET points = %s WHERE id = %s", (new_points, user_id))

                # 添加兑换记录
                cursor.execute("INSERT INTO reward_logs (user_id, description, timestamp) VALUES (%s, %s, %s)",
                               (user_id, f"兑换 {reward['description']}，消费了 {reward['points_needed']} 分", datetime.now()))

                message = "兑换成功！"
            else:
                message = "积分不足，无法兑换。"

            # 添加兑换记录（包括失败消息）
            cursor.execute("INSERT INTO reward_logs (user_id, description, timestamp) VALUES (%s, %s, %s)",
                           (user_id, message, datetime.now()))
        else:
            message = "无效的奖励项目或用户信息。"
            cursor.execute("INSERT INTO reward_logs (user_id, description, timestamp) VALUES (%s, %s, %s)",
                           (user_id, message, datetime.now()))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('child_dashboard'))

    return redirect(url_for('login'))

@app.route('/add_reward', methods=['GET', 'POST'])
def add_reward():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        description = request.form['description']
        points_needed = request.form['points_needed']

        cursor.execute("INSERT INTO rewards (description, points_needed, type) VALUES (%s, %s, %s)", (description, points_needed, "consumption"))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('dashboard'))

    cursor.close()
    conn.close()
    return render_template('add_reward.html')


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        description = request.form['description']
        points = request.form['points']

        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("INSERT INTO tasks (description, points) VALUES (%s, %s)", (description, points))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('dashboard'))

    return render_template('add_task.html')
# 注册用户
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']  # 角色字段

        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # 检查用户名是否已存在
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()
            return render_template('register.html', error="用户名已存在")

        # 加密密码
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # 插入新用户，保存加密后的密码
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                       (username, hashed_password, role))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('dashboard'))

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5566)  # 修改为需要的端口
