# ContentFlow AI - Aplicativo Completo

## 🚀 Sobre o Projeto

ContentFlow AI é um aplicativo web completo para geração de conteúdo para redes sociais usando Inteligência Artificial. Desenvolvido com Flask (Python) no backend e preparado para integração com frontend React.

## ✨ Funcionalidades

- 📝 **Geração de Legendas**: Legendas inteligentes para posts
- 💡 **Ideias de Conteúdo**: Sugestões criativas baseadas em palavras-chave
- #️⃣ **Hashtags Inteligentes**: Hashtags relevantes por plataforma
- 🎬 **Roteiros de Vídeo**: Scripts para TikTok, Reels e Shorts
- 👥 **Sistema de Usuários**: Registro, login e perfis
- 📊 **Planos de Assinatura**: Controle de cotas e limitações
- 📈 **Histórico**: Gerenciamento de conteúdo gerado

## 🛠️ Tecnologias

- **Backend**: Flask + SQLite
- **Autenticação**: JWT + bcrypt
- **IA**: Simulação de geração de conteúdo (pronto para OpenAI)
- **Deploy**: Heroku, Vercel, Railway

## 📦 Instalação Local

### 1. Clone ou baixe os arquivos
```bash
# Criar diretório
mkdir contentflow-ai
cd contentflow-ai

# Copiar todos os arquivos fornecidos
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Executar aplicação
```bash
python app.py
```

### 4. Acessar
- API: http://localhost:5000
- Health Check: http://localhost:5000/api/health

## 🌐 Deploy em Hospedagens Gratuitas

### 🔥 Railway (Recomendado)

1. **Criar conta**: https://railway.app
2. **Novo projeto**: "Deploy from GitHub repo"
3. **Conectar repositório** com os arquivos
4. **Deploy automático**: Railway detecta Python e faz deploy
5. **URL pública**: Gerada automaticamente

### ⚡ Vercel

1. **Criar conta**: https://vercel.com
2. **Novo projeto**: Import Git Repository
3. **Configurar**:
   - Framework Preset: Other
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: `.`
4. **Deploy**: Automático

### 🟣 Heroku

1. **Criar conta**: https://heroku.com
2. **Instalar Heroku CLI**
3. **Comandos**:
```bash
heroku create contentflow-ai-app
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

### 🔵 Render

1. **Criar conta**: https://render.com
2. **Novo Web Service**
3. **Conectar repositório**
4. **Configurações**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

## 📋 Endpoints da API

### Autenticação
- `POST /api/auth/register` - Registro
- `POST /api/auth/login` - Login

### Geração de Conteúdo
- `POST /api/content/generate/caption` - Legendas
- `POST /api/content/generate/ideas` - Ideias
- `POST /api/content/generate/hashtags` - Hashtags
- `POST /api/content/generate/script` - Roteiros

### Usuário
- `GET /api/user/profile` - Perfil
- `GET /api/content/history` - Histórico

### Sistema
- `GET /api/health` - Status
- `GET /api/info` - Informações

## 🧪 Testando a API

### Registro de usuário
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "teste",
    "email": "teste@email.com",
    "password": "12345678",
    "full_name": "Usuário Teste"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "teste",
    "password": "12345678"
  }'
```

### Gerar legenda (com token)
```bash
curl -X POST http://localhost:5000/api/content/generate/caption \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "topic": "Dicas de produtividade",
    "platform": "instagram",
    "tone": "casual"
  }'
```

## 🔧 Configurações

### Variáveis de Ambiente
```bash
SECRET_KEY=sua_chave_secreta_aqui
PORT=5000
```

### Banco de Dados
- SQLite (criado automaticamente)
- Arquivo: `contentflow.db`

## 🚀 Próximos Passos

1. **Integrar OpenAI**: Substituir simulação por API real
2. **Frontend React**: Criar interface completa
3. **Pagamentos**: Integrar Stripe
4. **Cache**: Implementar Redis
5. **Testes**: Adicionar testes automatizados

## 📞 Suporte

- **Documentação**: Este README
- **Issues**: Reportar problemas
- **Email**: suporte@contentflow.ai

## 📄 Licença

Projeto desenvolvido como demonstração técnica.

---

**ContentFlow AI** - Transformando ideias em conteúdo viral! 🚀

