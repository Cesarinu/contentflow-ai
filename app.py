#!/usr/bin/env python3
"""
ContentFlow AI - Aplicativo completo para geração de conteúdo para redes sociais
Desenvolvido com Flask + React
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from functools import wraps
import jwt
import bcrypt
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'contentflow_ai_secret_key_2024_secure')
app.config['DATABASE'] = 'contentflow.db'

# CORS
CORS(app, origins='*', allow_headers=['Content-Type', 'Authorization'])

# Inicializar banco de dados
def init_db():
    """Inicializa o banco de dados SQLite"""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            subscription_plan TEXT DEFAULT 'free',
            subscription_status TEXT DEFAULT 'active',
            usage_limit INTEGER DEFAULT 10,
            monthly_usage INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Tabela de conteúdo gerado
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content_type TEXT NOT NULL,
            prompt TEXT,
            generated_text TEXT,
            platform TEXT,
            tone TEXT,
            keywords TEXT,
            is_favorite BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Decorador para autenticação JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token é obrigatório'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(current_user_id, *args, **kwargs)
    return decorated

# Função para gerar conteúdo com IA (simulado)
def generate_ai_content(content_type, prompt, platform='instagram', tone='casual'):
    """Simula geração de conteúdo com IA"""
    
    if content_type == 'caption':
        templates = {
            'casual': f"🚀 {prompt} ✨\n\nVocê sabia que isso pode transformar completamente sua rotina? Aqui estão algumas dicas incríveis:\n\n📝 Primeira dica importante\n💡 Segunda dica valiosa\n🎯 Terceira dica essencial\n\nO que você achou? Comenta aqui embaixo! 👇\n\n#ContentFlow #DicasIncriveis #Transformacao",
            'professional': f"📊 {prompt}\n\nEm um mercado cada vez mais competitivo, é fundamental estar atualizado com as melhores práticas. Nosso estudo mostra que:\n\n• 85% dos profissionais que aplicam essas técnicas veem resultados\n• Aumento médio de 40% na produtividade\n• ROI positivo em até 30 dias\n\nSaiba mais nos comentários.\n\n#Profissional #Resultados #Estrategia",
            'funny': f"😂 {prompt} 🤣\n\nGente, vocês não vão acreditar no que aconteceu! Era uma vez...\n\n🎭 Plot twist número 1\n🎪 Momento épico\n🎨 Final inesperado\n\nQuem mais já passou por isso? Marca aquele amigo que precisa ver! 😅\n\n#Humor #Engracado #VidaReal"
        }
        return templates.get(tone, templates['casual'])
    
    elif content_type == 'ideas':
        ideas = [
            {
                'title': f'Tutorial sobre {prompt}',
                'description': f'Crie um passo a passo completo sobre {prompt} para iniciantes',
                'format': 'Vídeo tutorial'
            },
            {
                'title': f'Mitos e verdades sobre {prompt}',
                'description': f'Desmistifique conceitos errados relacionados a {prompt}',
                'format': 'Carrossel informativo'
            },
            {
                'title': f'Antes e depois: {prompt}',
                'description': f'Mostre transformações reais relacionadas a {prompt}',
                'format': 'Post comparativo'
            },
            {
                'title': f'5 erros comuns em {prompt}',
                'description': f'Liste os principais erros que pessoas cometem com {prompt}',
                'format': 'Lista educativa'
            },
            {
                'title': f'Tendências 2024 em {prompt}',
                'description': f'Apresente as principais tendências e novidades em {prompt}',
                'format': 'Post informativo'
            }
        ]
        return ideas
    
    elif content_type == 'hashtags':
        base_hashtags = prompt.lower().replace(' ', '').split(',')
        hashtags = []
        
        # Hashtags específicas do prompt
        for tag in base_hashtags[:3]:
            hashtags.extend([
                tag.strip(),
                f'{tag.strip()}2024',
                f'{tag.strip()}Brasil'
            ])
        
        # Hashtags gerais por plataforma
        platform_hashtags = {
            'instagram': ['insta', 'instagram', 'reels', 'stories', 'igers'],
            'tiktok': ['tiktok', 'fyp', 'viral', 'trending', 'foryou'],
            'youtube': ['youtube', 'shorts', 'subscribe', 'youtuber', 'video'],
            'linkedin': ['linkedin', 'professional', 'career', 'business', 'networking']
        }
        
        hashtags.extend(platform_hashtags.get(platform, platform_hashtags['instagram']))
        
        # Hashtags populares gerais
        hashtags.extend([
            'brasil', 'dicas', 'motivacao', 'inspiracao', 'sucesso',
            'lifestyle', 'qualidade', 'inovacao', 'criatividade', 'foco'
        ])
        
        return list(set(hashtags))[:20]  # Remove duplicatas e limita a 20
    
    elif content_type == 'script':
        return {
            'hook': f'Você sabia que {prompt} pode mudar sua vida em 30 dias?',
            'development': f'Hoje vou te mostrar exatamente como {prompt} funciona na prática. Primeiro, você precisa entender que... [desenvolvimento do conteúdo sobre {prompt}]',
            'cta': 'Se esse conteúdo te ajudou, salva o post e compartilha com quem precisa ver!',
            'visual_suggestions': [
                'Texto na tela com estatísticas',
                'Transições dinâmicas',
                'Close-up para momentos importantes',
                'Música de fundo energética'
            ]
        }
    
    return "Conteúdo gerado com sucesso!"

# Rotas de autenticação
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Registro de novo usuário"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Username, email e senha são obrigatórios'}), 400
    
    # Validações
    if len(data['password']) < 8:
        return jsonify({'error': 'Senha deve ter pelo menos 8 caracteres'}), 400
    
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    # Verificar se usuário já existe
    cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', 
                   (data['username'], data['email']))
    if cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Username ou email já existe'}), 400
    
    # Hash da senha
    password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Inserir usuário
    cursor.execute('''
        INSERT INTO users (username, email, password_hash, full_name)
        VALUES (?, ?, ?, ?)
    ''', (data['username'], data['email'], password_hash, data.get('full_name', '')))
    
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    # Gerar token JWT
    token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'message': 'Usuário criado com sucesso',
        'token': token,
        'user': {
            'id': user_id,
            'username': data['username'],
            'email': data['email'],
            'full_name': data.get('full_name', ''),
            'subscription_plan': 'free',
            'usage_limit': 10,
            'monthly_usage': 0
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login de usuário"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username e senha são obrigatórios'}), 400
    
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    # Buscar usuário (pode ser username ou email)
    cursor.execute('''
        SELECT id, username, email, password_hash, full_name, subscription_plan, 
               usage_limit, monthly_usage, subscription_status
        FROM users WHERE username = ? OR email = ?
    ''', (data['username'], data['username']))
    
    user = cursor.fetchone()
    
    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user[3].encode('utf-8')):
        conn.close()
        return jsonify({'error': 'Credenciais inválidas'}), 401
    
    # Atualizar último login
    cursor.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user[0],))
    conn.commit()
    conn.close()
    
    # Gerar token JWT
    token = jwt.encode({
        'user_id': user[0],
        'exp': datetime.utcnow() + timedelta(days=30)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'message': 'Login realizado com sucesso',
        'token': token,
        'user': {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'full_name': user[4],
            'subscription_plan': user[5],
            'usage_limit': user[6],
            'monthly_usage': user[7],
            'subscription_status': user[8]
        }
    })

# Rotas de geração de conteúdo
@app.route('/api/content/generate/<content_type>', methods=['POST'])
@token_required
def generate_content(user_id, content_type):
    """Gera conteúdo usando IA"""
    data = request.get_json()
    
    if content_type not in ['caption', 'ideas', 'hashtags', 'script']:
        return jsonify({'error': 'Tipo de conteúdo inválido'}), 400
    
    # Verificar limite de uso
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    cursor.execute('SELECT usage_limit, monthly_usage FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    
    if user_data and user_data[0] != -1 and user_data[1] >= user_data[0]:
        conn.close()
        return jsonify({'error': 'Limite mensal atingido'}), 403
    
    # Gerar conteúdo
    if content_type == 'caption':
        prompt = data.get('topic', '')
        platform = data.get('platform', 'instagram')
        tone = data.get('tone', 'casual')
        generated_content = generate_ai_content('caption', prompt, platform, tone)
        
    elif content_type == 'ideas':
        keywords = data.get('keywords', '')
        generated_content = generate_ai_content('ideas', keywords)
        
    elif content_type == 'hashtags':
        content = data.get('content', '')
        platform = data.get('platform', 'instagram')
        generated_content = generate_ai_content('hashtags', content, platform)
        
    elif content_type == 'script':
        topic = data.get('topic', '')
        generated_content = generate_ai_content('script', topic)
    
    # Salvar no banco
    cursor.execute('''
        INSERT INTO content (user_id, content_type, prompt, generated_text, platform, tone)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, content_type, data.get('topic') or data.get('keywords') or data.get('content'), 
          json.dumps(generated_content) if isinstance(generated_content, (dict, list)) else generated_content,
          data.get('platform', ''), data.get('tone', '')))
    
    # Atualizar uso mensal
    cursor.execute('UPDATE users SET monthly_usage = monthly_usage + 1 WHERE id = ?', (user_id,))
    
    conn.commit()
    conn.close()
    
    # Preparar resposta
    response = {'status': 'success'}
    
    if content_type == 'caption':
        response['caption'] = generated_content
    elif content_type == 'ideas':
        response['ideas'] = generated_content
    elif content_type == 'hashtags':
        response['hashtags'] = generated_content
    elif content_type == 'script':
        response['script'] = generated_content
    
    return jsonify(response)

@app.route('/api/content/history', methods=['GET'])
@token_required
def get_content_history(user_id):
    """Retorna histórico de conteúdo do usuário"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    content_type = request.args.get('type', '')
    
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    query = 'SELECT * FROM content WHERE user_id = ?'
    params = [user_id]
    
    if content_type:
        query += ' AND content_type = ?'
        params.append(content_type)
    
    query += ' ORDER BY created_at DESC LIMIT ? OFFSET ?'
    params.extend([per_page, (page - 1) * per_page])
    
    cursor.execute(query, params)
    contents = cursor.fetchall()
    
    # Contar total
    count_query = 'SELECT COUNT(*) FROM content WHERE user_id = ?'
    count_params = [user_id]
    if content_type:
        count_query += ' AND content_type = ?'
        count_params.append(content_type)
    
    cursor.execute(count_query, count_params)
    total = cursor.fetchone()[0]
    
    conn.close()
    
    # Formatar resposta
    formatted_contents = []
    for content in contents:
        formatted_contents.append({
            'id': content[0],
            'content_type': content[2],
            'prompt': content[3],
            'generated_text': content[4],
            'platform': content[5],
            'tone': content[6],
            'is_favorite': bool(content[8]),
            'created_at': content[9]
        })
    
    return jsonify({
        'contents': formatted_contents,
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page
    })

# Rotas de usuário
@app.route('/api/user/profile', methods=['GET'])
@token_required
def get_profile(user_id):
    """Retorna perfil do usuário"""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT username, email, full_name, subscription_plan, usage_limit, 
               monthly_usage, subscription_status, created_at, last_login
        FROM users WHERE id = ?
    ''', (user_id,))
    
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    return jsonify({
        'id': user_id,
        'username': user[0],
        'email': user[1],
        'full_name': user[2],
        'subscription_plan': user[3],
        'usage_limit': user[4],
        'monthly_usage': user[5],
        'subscription_status': user[6],
        'created_at': user[7],
        'last_login': user[8]
    })

# Rotas de sistema
@app.route('/api/health')
def health_check():
    """Health check da API"""
    return jsonify({
        'status': 'ok',
        'message': 'ContentFlow AI API funcionando',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/info')
def api_info():
    """Informações da API"""
    return jsonify({
        'name': 'ContentFlow AI',
        'version': '1.0.0',
        'description': 'API para geração de conteúdo para redes sociais usando IA',
        'features': [
            'Geração de legendas inteligentes',
            'Criação de ideias de conteúdo',
            'Geração de hashtags relevantes',
            'Roteiros para vídeos curtos',
            'Sistema de usuários completo',
            'Planos de assinatura',
            'Histórico de conteúdo'
        ],
        'endpoints': {
            'auth': ['/api/auth/register', '/api/auth/login'],
            'content': ['/api/content/generate/<type>', '/api/content/history'],
            'user': ['/api/user/profile'],
            'system': ['/api/health', '/api/info']
        }
    })

# Rota para servir frontend (se existir)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve o frontend React ou página de demonstração"""
    
    # Verificar se existe pasta static com frontend
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    
    if os.path.exists(static_dir):
        if path != '' and os.path.exists(os.path.join(static_dir, path)):
            return send_from_directory(static_dir, path)
        else:
            index_path = os.path.join(static_dir, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_dir, 'index.html')
    
    # Página de demonstração
    return '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ContentFlow AI - API</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh; color: white; padding: 2rem;
            }
            .container { max-width: 800px; margin: 0 auto; text-align: center; }
            h1 { font-size: 3rem; margin-bottom: 1rem; }
            .status { background: #4CAF50; padding: 1rem 2rem; border-radius: 25px; 
                     display: inline-block; margin-bottom: 2rem; font-weight: bold; }
            .endpoints { background: rgba(255,255,255,0.1); padding: 2rem; 
                        border-radius: 15px; margin: 2rem 0; text-align: left; }
            .endpoint { margin: 1rem 0; padding: 0.5rem; background: rgba(255,255,255,0.1); 
                       border-radius: 5px; }
            .btn { display: inline-block; padding: 1rem 2rem; background: rgba(255,255,255,0.2); 
                  color: white; text-decoration: none; border-radius: 25px; margin: 0.5rem; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="status">🟢 API Online</div>
            <h1>⚡ ContentFlow AI</h1>
            <p style="font-size: 1.2rem; margin-bottom: 2rem;">
                API para Geração de Conteúdo para Redes Sociais
            </p>
            
            <div class="endpoints">
                <h3>📋 Endpoints Disponíveis:</h3>
                <div class="endpoint"><strong>POST</strong> /api/auth/register - Registro de usuário</div>
                <div class="endpoint"><strong>POST</strong> /api/auth/login - Login</div>
                <div class="endpoint"><strong>POST</strong> /api/content/generate/caption - Gerar legenda</div>
                <div class="endpoint"><strong>POST</strong> /api/content/generate/ideas - Gerar ideias</div>
                <div class="endpoint"><strong>POST</strong> /api/content/generate/hashtags - Gerar hashtags</div>
                <div class="endpoint"><strong>POST</strong> /api/content/generate/script - Gerar roteiro</div>
                <div class="endpoint"><strong>GET</strong> /api/content/history - Histórico</div>
                <div class="endpoint"><strong>GET</strong> /api/user/profile - Perfil do usuário</div>
            </div>
            
            <a href="/api/health" class="btn">🔍 Health Check</a>
            <a href="/api/info" class="btn">📋 Informações da API</a>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    # Inicializar banco de dados
    init_db()
    
    print("🚀 Iniciando ContentFlow AI...")
    print("📱 API disponível em: http://localhost:5000")
    print("🔗 Health Check: http://localhost:5000/api/health")
    
    # Executar aplicação
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

