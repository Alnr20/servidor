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
def token_requerido(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Obtendo o token do cabeçalho da requisição
        if 'Authorization' in request.headers:
            token = request.headers['Autorization']. slipt(" ") [1]

        if not token:
            return jsonify({"mensagem": "Token é necessario"})
        
        try:
            # Descondificando e validando o token 
            dados = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.userid = dados["userid"]
        except jwt.ExpiredSignatureError:
            return jsonify({mensagem: "Token expirado"})
        except jwt.InvalidTokenError:
            returnjsonify({"mensagem": "Token invalido"})
        
        return f(*args, **kwargs)

    return decorated

# rota protegida (domente acessivel com o token válido)
@app.route('/protegido',methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email= data.get('email')
    password = data.get('password')

    if not username or not email or not password:
       return jsonify({'error': 'Username,email and password are required'}) #, 400

    # hash da senha antes de salvar no db
    hashed_password = generate_password_hash(password)

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO users (username, email,password) VALUES (?, ?, ?)',
                   (username, email, hashed_password))
    db.comit()

    return jsonify({'id': cursor.lastrowid, 'username':username, 'email':email}) #,200 


