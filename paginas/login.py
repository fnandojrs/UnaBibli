from nicegui import ui


import pymysql
import hashlib



def conectar():
    return pymysql.connect(
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
            ui.label('📖 Biblioteca - Login').classes('text-2xl mb-6 text-center')

            email = ui.input('Email').props('outlined').classes('w-full mb-4').props('placeholder=email@exemplo.com')
            senha_input = ui.input('Senha', password=True) \
                            .props('outlined') \
                            .classes('w-full mb-2') \
                            .props('placeholder=********')

            
            

            def login():
                if not email.value or not senha_input.value:
                    ui.notify('Preencha todos os campos', type='negative')
                    return
                try:
                    conn = conectar()
                    cursor = conn.cursor()
                    # busca usuário
                    cursor.execute('SELECT * FROM usuarios WHERE nome = %s AND senha = %s',
                                   (email.value, senha_input.value))
                    usuario = cursor.fetchone()
                    if not usuario or senha_input.value != usuario[3]:
                        email.value = ''
                        senha_input.value = ''
                        ui.notify('Login inválido', type='negative')
                        return
                    if usuario:
                        # supondo que o campo 9 seja o tipo: 'cliente' / 'funcionario' / 'admin'
                        tipo = usuario[9].upper()  
                        
                        
                        
                        if tipo == 'CLIENTE':
                            ui.notify('Login como cliente')
                            ui.navigate.to('/consulta')
                        else:
                            ui.run_javascript('window.location.href = "/dashboard";')        
                    


                    
                    


                except Exception as e:
                    ui.notify(f'Erro no banco: {e}', type='negative')
                finally:
                    if 'conn' in locals() :
                        cursor.close()
                        conn.close()

            ui.button('Entrar', on_click=login).classes('mt-2 w-full')
            





