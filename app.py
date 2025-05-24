import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = 'heylink_secret_key_2025'  # Mude para uma chave mais segura em produção

# Configurações
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ADMIN_PASSWORD = 'admin123'  # Senha do painel administrativo

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Criar diretório de uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    """Inicializa o banco de dados SQLite"""
    conn = sqlite3.connect('heylink.db')
    cursor = conn.cursor()
    
    # Tabela de configurações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS config (
            id INTEGER PRIMARY KEY,
            title TEXT DEFAULT 'Meu Heylink',
            description TEXT DEFAULT 'Todos os meus links em um só lugar',
            logo_path TEXT DEFAULT ''
        )
    ''')
    
    # Tabela de links
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            url TEXT NOT NULL,
            image_path TEXT DEFAULT '',
            order_index INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Inserir configuração padrão se não existir
    cursor.execute('SELECT COUNT(*) FROM config')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO config (title, description, logo_path) 
            VALUES (?, ?, ?)
        ''', ('Meu Heylink', 'Todos os meus links em um só lugar', ''))
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Retorna conexão com o banco de dados"""
    conn = sqlite3.connect('heylink.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.before_request
def add_security_headers():
    """Adiciona headers de segurança para compatibilidade com Telegram Mini App"""
    pass

@app.after_request
def after_request(response):
    """Adiciona headers de segurança após cada requisição"""
    response.headers['Content-Security-Policy'] = "frame-ancestors 'self' https://t.me https://web.telegram.org https://work-2-mdxxuukcjoqxwbuo.prod-runtime.all-hands.dev"
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/')
def index():
    """Página principal - Landing Page"""
    conn = get_db_connection()
    
    # Buscar configurações
    config = conn.execute('SELECT * FROM config WHERE id = 1').fetchone()
    
    # Buscar links ordenados
    links = conn.execute('''
        SELECT * FROM links 
        ORDER BY order_index ASC, created_at ASC
    ''').fetchall()
    
    conn.close()
    
    return render_template('index.html', config=config, links=links)

@app.route('/admin')
def admin_login():
    """Página de login do admin"""
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    """Processa login do admin"""
    password = request.form.get('password')
    if password == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        flash('Login realizado com sucesso!', 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Senha incorreta!', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/logout')
def admin_logout():
    """Logout do admin"""
    session.pop('admin_logged_in', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """Dashboard administrativo"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    
    # Buscar configurações
    config = conn.execute('SELECT * FROM config WHERE id = 1').fetchone()
    
    # Buscar links
    links = conn.execute('''
        SELECT * FROM links 
        ORDER BY order_index ASC, created_at ASC
    ''').fetchall()
    
    conn.close()
    
    return render_template('admin_dashboard.html', config=config, links=links)

@app.route('/admin/config', methods=['POST'])
def admin_update_config():
    """Atualiza configurações gerais"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    title = request.form.get('title')
    description = request.form.get('description')
    
    conn = get_db_connection()
    
    # Processar upload do logo se houver
    logo_path = ''
    if 'logo' in request.files:
        file = request.files['logo']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            logo_path = f'uploads/{filename}'
    
    # Atualizar configurações
    if logo_path:
        conn.execute('''
            UPDATE config 
            SET title = ?, description = ?, logo_path = ?
            WHERE id = 1
        ''', (title, description, logo_path))
    else:
        conn.execute('''
            UPDATE config 
            SET title = ?, description = ?
            WHERE id = 1
        ''', (title, description))
    
    conn.commit()
    conn.close()
    
    flash('Configurações atualizadas com sucesso!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/link/add', methods=['POST'])
def admin_add_link():
    """Adiciona novo link"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    title = request.form.get('title')
    description = request.form.get('description')
    url = request.form.get('url')
    
    # Processar upload da imagem se houver
    image_path = ''
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            image_path = f'uploads/{filename}'
    
    conn = get_db_connection()
    
    # Buscar próximo order_index
    max_order = conn.execute('SELECT MAX(order_index) FROM links').fetchone()[0]
    next_order = (max_order or 0) + 1
    
    conn.execute('''
        INSERT INTO links (title, description, url, image_path, order_index)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, description, url, image_path, next_order))
    
    conn.commit()
    conn.close()
    
    flash('Link adicionado com sucesso!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/link/edit/<int:link_id>', methods=['POST'])
def admin_edit_link(link_id):
    """Edita link existente"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    title = request.form.get('title')
    description = request.form.get('description')
    url = request.form.get('url')
    
    conn = get_db_connection()
    
    # Processar upload da imagem se houver
    image_path = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            image_path = f'uploads/{filename}'
    
    # Atualizar link
    if image_path:
        conn.execute('''
            UPDATE links 
            SET title = ?, description = ?, url = ?, image_path = ?
            WHERE id = ?
        ''', (title, description, url, image_path, link_id))
    else:
        conn.execute('''
            UPDATE links 
            SET title = ?, description = ?, url = ?
            WHERE id = ?
        ''', (title, description, url, link_id))
    
    conn.commit()
    conn.close()
    
    flash('Link atualizado com sucesso!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/link/delete/<int:link_id>')
def admin_delete_link(link_id):
    """Deleta link"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM links WHERE id = ?', (link_id,))
    conn.commit()
    conn.close()
    
    flash('Link removido com sucesso!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/link/reorder', methods=['POST'])
def admin_reorder_links():
    """Reordena links"""
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    link_ids = request.json.get('link_ids', [])
    
    conn = get_db_connection()
    
    for index, link_id in enumerate(link_ids):
        conn.execute('''
            UPDATE links 
            SET order_index = ?
            WHERE id = ?
        ''', (index + 1, link_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000, debug=False)