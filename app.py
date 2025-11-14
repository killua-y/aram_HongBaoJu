from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
from contextlib import contextmanager

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# 检测是否使用 PostgreSQL（生产环境）还是 SQLite（开发环境）
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # 生产环境：使用 PostgreSQL
    import psycopg2
    from psycopg2.extras import RealDictCursor
    USE_POSTGRES = True
    # 解析数据库 URL（Render 提供的格式：postgresql://user:pass@host:port/dbname）
    # 某些情况下可能是 postgres://，需要转换为 postgresql://
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
else:
    # 开发环境：使用 SQLite
    import sqlite3
    USE_POSTGRES = False
    DATABASE = 'expenses.db'


@contextmanager
def get_db():
    """数据库连接上下文管理器，支持 PostgreSQL 和 SQLite"""
    if USE_POSTGRES:
        # PostgreSQL 连接
        conn = psycopg2.connect(DATABASE_URL)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    else:
        # SQLite 连接
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


def init_db():
    """初始化数据库表（兼容 PostgreSQL 和 SQLite）"""
    if USE_POSTGRES:
        # PostgreSQL 表结构
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS records (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        amount REAL NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        note TEXT
                    )
                ''')
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_name ON records(name)
                ''')
    else:
        # SQLite 表结构
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


# 在应用启动时自动初始化数据库（适用于生产环境）
init_db()


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
                    if USE_POSTGRES:
                        with conn.cursor() as cursor:
                            cursor.execute(
                                'INSERT INTO records (name, amount, note) VALUES (%s, %s, %s)',
                                (name, amount, note)
                            )
                    else:
                        conn.execute(
                            'INSERT INTO records (name, amount, note) VALUES (?, ?, ?)',
                            (name, amount, note)
                        )
                flash(f'已添加：{name} {amount:+.2f}', 'success')
                return redirect(url_for('index'))
            except ValueError:
                flash('金额格式不正确', 'error')
            except Exception as e:
                flash(f'保存失败：{str(e)}', 'error')
    
    # 获取所有记录（按时间倒序）
    with get_db() as conn:
        if USE_POSTGRES:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            try:
                cursor.execute('SELECT * FROM records ORDER BY created_at DESC LIMIT 100')
                records = cursor.fetchall()
                
                cursor.execute('SELECT name, SUM(amount) as total FROM records GROUP BY name ORDER BY name')
                summary = cursor.fetchall()
            finally:
                cursor.close()
        else:
            records = conn.execute(
                'SELECT * FROM records ORDER BY created_at DESC LIMIT 100'
            ).fetchall()
            
            summary = conn.execute(
                'SELECT name, SUM(amount) as total FROM records GROUP BY name ORDER BY name'
            ).fetchall()
    
    return render_template('index.html', records=records, summary=summary)


@app.route('/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    """删除一条记录"""
    try:
        with get_db() as conn:
            if USE_POSTGRES:
                with conn.cursor() as cursor:
                    cursor.execute('DELETE FROM records WHERE id = %s', (record_id,))
            else:
                conn.execute('DELETE FROM records WHERE id = ?', (record_id,))
        flash('记录已删除', 'success')
    except Exception as e:
        flash(f'删除失败：{str(e)}', 'error')
    return redirect(url_for('index'))


@app.route('/clear', methods=['POST'])
def clear_all():
    """清空所有记录（危险操作）"""
    confirm = request.form.get('confirm', '')
    if confirm == '删除':
        try:
            with get_db() as conn:
                if USE_POSTGRES:
                    with conn.cursor() as cursor:
                        cursor.execute('DELETE FROM records')
                else:
                    conn.execute('DELETE FROM records')
            flash('所有记录已清空', 'success')
        except Exception as e:
            flash(f'清空失败：{str(e)}', 'error')
    else:
        flash('确认文本不正确，操作已取消', 'error')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # 启动开发服务器
    # macOS 上 5000 端口常被 AirPlay Receiver 占用，改用 5001
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
