from nicegui import ui
import re
import datetime

import os

import pymysql

def conectar():
    return pymysql.connect(
        host='metro.proxy.rlwy.net',
        port=25858,
        user='root',
        password='bojFqQXsCRiLKyzbmgsPidyeQLJAVlsE',
        database='railway'
    )

# Validações
def validar_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def validar_senha(senha):
    return len(senha) == 6 and senha.isdigit()



# Formulário comum
def formulario_simples():
    with ui.card().classes('w-full max-w-lg mx-auto'):
        ui.icon('person').classes('text-primary text-4xl mx-auto')
        with ui.column().classes('items-center w-full'):
            ui.markdown("### Cadastro de Usuário")
        
        nome = ui.input('Nome').props('maxlength=50').classes('w-full').props('placeholder=Digite seu nome')
        email = ui.input('Email').classes('w-full').props('placeholder=email@exemplo.com')
        tipo_usuario = ui.select(
            ['ADMIN', 'CLIENTE', 'FUNCIONARIO'], 
            label='Tipo de Usuário'
        ).classes('w-60')
        with ui.column().classes('items-center w-full'):
            ui.markdown('#### Data de Nascimento')

        dias = [str(d).zfill(2) for d in range(1, 32)]
        meses = [str(m).zfill(2) for m in range(1, 13)]
        anos = [str(a) for a in range( datetime.datetime.now().year - 80, datetime.datetime.now().year - 8)] 

        with ui.column().classes('items-center w-full'):
            with ui.row().classes('items-center w-full justify-around'):
                
                dia = ui.select(dias, label='Dia').classes('w-20')
                mes = ui.select(meses, label='Mês').classes('w-20')
                ano = ui.select(anos[::-1], label='Ano').classes('w-40')  






        senha = ui.input('Senha (6 dígitos)', password=True, password_toggle_button=True).classes('w-60')

        with ui.row().classes('items-center w-full'):
            ui.button('Cadastrar', on_click=lambda: callback(
                nome.value, email.value, tipo_usuario.value,
                dia.value, mes.value, ano.value, senha.value
            )).classes('w-40').props('color=primary unelevated')

           
    

            ui.button('Voltar', on_click=lambda: ui.navigate.to('/dashboard')).props('color=secondary unelevated')




def callback(nome, email, tipo, dia, mes, ano, senha):
    if not nome or not email or not tipo or not dia or not mes or not ano or not senha:
        ui.notify('Preencha todos os campos.', type='negative')
        return

    if not validar_email(email):
        ui.notify('Email inválido.', type='negative')
        return

    if not validar_senha(senha):
        ui.notify('A senha deve conter exatamente 6 dígitos numéricos.', type='negative')
        return

    data_nascimento = f'{ano}-{mes}-{dia}'

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, tipo_usuario, data_nascimento, senha) VALUES (%s, %s, %s, %s, %s)",
            (nome, email, tipo, data_nascimento, senha)
        )
        conn.commit()
        dialog = ui.dialog()

        dialog = ui.dialog()

        with dialog:
            with ui.card().classes('items-center p-4'):
                ui.label('✅ Usuário cadastrado com sucesso!').classes('text-lg font-bold mb-2')
                with ui.column().classes('items-center w-full'):
                 ui.button('OK', on_click=lambda: (dialog.close() , ui.navigate.to('/cadastro_ay'))).props('color=primary')

        dialog.open()
        # ui.run_javascript('window.location.href = "/cadastro_ay";')

    except Exception as e:
        ui.notify(f'Erro ao cadastrar: {e}', type='negative')
    finally:
        cursor.close()
        conn.close()


# Página principal
@ui.page('/cadastro_ay')
def index():
    
    with ui.column().classes('items-center w-full'):
        ui.markdown("## Cadastro de Usuarios 📚")

        formulario_simples()


          
           
            
            
        

            
            


