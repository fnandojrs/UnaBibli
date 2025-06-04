from nicegui import ui
import mysql.connector
from mysql.connector import Error
import hashlib

# logo abaixo dos imports
user_session = {"tipo": None, "usuario_id": None}


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def conectar():
    return mysql.connector.connect(
        host='metro.proxy.rlwy.net',
        port=25858,
        user='root',
        password='bojFqQXsCRiLKyzbmgsPidyeQLJAVlsE',
        database='railway'
    )

@ui.page('/')
def login_page():
    ui.add_head_html('<link rel="stylesheet" href="/static/custom.css">')

    with ui.element('div').classes('login-container'):
        with ui.element('div').classes('login-box'):
            ui.label('Login').classes('text-2xl mb-4')

            email = ui.input('Email').props('outlined').classes('w-full')

            # Container da linha com campo de senha e ícone
            with ui.row().classes('items-center w-full'):
                # Campo de senha com largura flexível
                senha_input = ui.input('Senha', password=True).props('outlined').classes('flex-grow')

                

                
                

            def login():
                try:
                    conn = conectar()
                    cursor = conn.cursor()

                    if email.value == '' or senha_input.value == '':
                        ui.notify('Preencha todos os campos')
                        return

                    cursor.execute('SELECT * FROM usuarios WHERE nome = %s AND senha = %s',
                                   (email.value, senha_input.value))
                    usuario = cursor.fetchone()
                    # Verifica se o usuário foi encontrado      
                    if not usuario:
                        ui.notify('Usuário não encontrado')
                        return
                    if usuario:
                        # supondo que o campo 9 seja o tipo: 'cliente' / 'funcionario' / 'admin'
                        tipo = usuario[9].upper()  
                        user_session["usuario_id"] = usuario[0]
                        user_session["tipo"] = tipo
                        
                        
                        if tipo == 'CLIENTE':
                            ui.notify('Login como cliente')
                            ui.navigate.to('/consulta')
                        else:
                            ui.navigate.to('/dashboard')        
                    else:
                        ui.notify('Login inválido', type='negative')
                        email.value = ''
                        senha_input.value = ''
                except Error as e:
                    ui.notify(f'Erro no banco: {e}')
                finally:
                    if conn.is_connected():
                        cursor.close()
                        conn.close()

            ui.button('Entrar', on_click=login).classes('mt-4 w-full')
            ui.button('Cadastrar Usuario', on_click=lambda: ui.navigate.to('/cadastro_usuario')).classes('mt-2 w-full')
