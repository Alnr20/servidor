from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

# senha
app.secret_key = '10111213'

# usuario demonstração
users = {'marcio': '10'}

@app.route('/')
def home():

    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
           session['username'] = username # Set session
           flash('Voce esta logado com sucesso')
           return redirect(url_for('dashboard'))
        else:
            flash('usuario ou senha ivalido')
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():

    if 'username' in session:
        return f'Bem vindo Pagina dashboard,{session["username"]}'
    else:
        flash('Primeiro vc tem que fazer o login')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.pop('username',None)
    flash('Voce foi deslogado!!!')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

