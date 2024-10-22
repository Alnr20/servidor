# inicializar banco de dados 
def int_db():
    with app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.excute('''
             CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINTREMENT,
                      username TEXT NOT NULL,
                      email TEXT NOT NULL,
                      password TEXT NOT NULL -- Adicionando campo de senha
            )
        ''')
        db.comit()

# Fechar conexão com o banco de dados ao finalizar a requisição 
@app. teardown_appcontext
def close_connection(exeption):
    db = getattr(g, '_database' , None)
    if db is not None:
        db.close()

# Função para gerar um token JTW (JSON WEB TOKEN - aqui é  o acessToken)
def generate_token(username,userid):
    payload = {
        'username': username,
        'userrid':userid,
        'exp': datetime.datetime.utcnow() + datetime.datetime(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm= 'HS256')
#Middleware para validar o token JWT
def token_requerido(f)
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Obtendo o token do cabeçalho da requisição
        if 'Authorization' in request.headers:
            token = request.headers['Autorization']. slipt(" ") [1]

        if not token:
            return jsonify({"mensagem": "Token é necessario"})
