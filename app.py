from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')  # 用于 flash 消息

# 数据库文件路径
DATABASE = 'expenses.db'


@contextmanager
def get_db():
    """数据库连接上下文管理器"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # 让查询结果可以像字典一样访问
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """初始化数据库表"""
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                amount REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                note TEXT
            )
        ''')
        conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_name ON records(name)
        ''')


@app.route('/', methods=['GET', 'POST'])
def index():
    """主页：显示表单和所有记录"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        amount_str = request.form.get('amount', '0').strip()
        note = request.form.get('note', '').strip()
        
        # 验证输入
        if not name:
            flash('请输入名字', 'error')
        elif not amount_str:
            flash('请输入金额', 'error')
        else:
            try:
                amount = float(amount_str)
                # 保存到数据库
                with get_db() as conn:
                    conn.execute(
                        'INSERT INTO records (name, amount, note) VALUES (?, ?, ?)',
                        (name, amount, note)
                    )
                flash(f'已添加：{name} {amount:+.2f}', 'success')
                return redirect(url_for('index'))  # 重定向避免重复提交
            except ValueError:
                flash('金额格式不正确', 'error')
    
    # 获取所有记录（按时间倒序）
    with get_db() as conn:
        records = conn.execute(
            'SELECT * FROM records ORDER BY created_at DESC LIMIT 100'
        ).fetchall()
        
        # 计算每个人的总盈亏
        summary = conn.execute(
            'SELECT name, SUM(amount) as total FROM records GROUP BY name ORDER BY name'
        ).fetchall()
    
    return render_template('index.html', records=records, summary=summary)


@app.route('/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    """删除一条记录"""
    with get_db() as conn:
        conn.execute('DELETE FROM records WHERE id = ?', (record_id,))
    flash('记录已删除', 'success')
    return redirect(url_for('index'))


@app.route('/clear', methods=['POST'])
def clear_all():
    """清空所有记录（危险操作）"""
    confirm = request.form.get('confirm', '')
    if confirm == '删除':
        with get_db() as conn:
            conn.execute('DELETE FROM records')
        flash('所有记录已清空', 'success')
    else:
        flash('确认文本不正确，操作已取消', 'error')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # 首次运行初始化数据库
    init_db()
    # 启动开发服务器
    # macOS 上 5000 端口常被 AirPlay Receiver 占用，改用 5001
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)

