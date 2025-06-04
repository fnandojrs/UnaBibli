from nicegui import ui

import pymysql
def conectar():
    return pymysql.connect(
        host='metro.proxy.rlwy.net',
        port=25858,
        user='root',
        password='bojFqQXsCRiLKyzbmgsPidyeQLJAVlsE',
        database='railway'
    )


def registrar_emprestimo():
        with ui.dialog() as dialog, ui.card().classes('shadow-xl rounded-lg p-50 text-center w-200'):
            ui.label('Registrar Empréstimo').classes('text-lg font-bold mb-4')
            nome_livro = ui.input('Nome do Livro').classes('mb-3')
            nome_usuario = ui.input('Nome do Usuário').classes('mb-3')
            with ui.row().classes('justify-end'):
                ui.button('Confirmar', on_click=dialog.close).classes('bg-green-500 text-white px-4 py-2 rounded-lg mr-2')
                ui.button('Cancelar', on_click=dialog.close).classes('bg-gray-500 text-white px-4 py-2 rounded-lg')

        dialog.open()

def registrar_devolucao():
        with ui.dialog() as dialog, ui.card():
            ui.label('Registrar Devolução').classes('text-lg font-bold mb-4')
            nome_livro = ui.input('Nome do Livro').classes('mb-3')
            nome_usuario = ui.input('Nome do Usuário').classes('mb-3')
            with ui.row().classes('justify-end'):
                ui.button('Confirmar', on_click=dialog.close).classes('bg-blue-500 text-white px-4 py-2 rounded-lg mr-2')
                ui.button('Cancelar', on_click=dialog.close).classes('bg-gray-500 text-white px-4 py-2 rounded-lg')

        dialog.open()

def consultar_historico():
        with ui.dialog() as dialog, ui.card():
            ui.label('Histórico de Movimentações').classes('text-lg font-bold mb-4')
            ui.label('Nenhuma movimentação registrada ainda.').classes('text-gray-500')
            ui.button('Fechar', on_click=dialog.close).classes('bg-gray-500 text-white px-4 py-2 rounded-lg mt-4')

        dialog.open()

@ui.page('/movimentacao')           # Interface principal ajustada para os botões no 
def movimentar_page():
    dark = ui.dark_mode()
    with ui.row().classes("justify-end w-full pr-4 pt-2"):
        
        ui.button('Voltar', on_click=lambda: ui.navigate.to('/dashboard')).props('color=secondary unelevated')
    with ui.column().classes('w-full items-center pt-1'):
        with ui.card().classes('shadow-xl rounded-lg p-50 text-center w-200'):
            with ui.column().classes('w-full items-center pt-1'):
                ui.label('Movimentações').classes('text-3xl font-bold mb-6 text-gray-800')
                ui.label('Escolha uma das opções abaixo:').classes('text-lg mb-6 text-gray-600')
            with ui.row().classes('w-full justify-center items-center py-1'):
                ui.button('Consultar Histórico', on_click=consultar_historico).props('color=primary unelevated')
                ui.button('Registrar Empréstimo', on_click=registrar_emprestimo).props('color=primary unelevated')
                ui.button('Registrar Devolução', on_click=registrar_devolucao).props('color=primary unelevated')
                
    
    ui.run_javascript('document.title = "Movimentações - Biblioteca"')
    ui.run_javascript('document.body.style.backgroundColor = "#f0f0f0"')
    ui.run_javascript('document.body.style.fontFamily = "Arial, sans-serif"')
    ui.run_javascript('document.body.style.color = "#333"')
    ui.run_javascript('document.body.style.padding = "20px"')
    ui.run_javascript('document.body.style.display = "flex"')
    ui.run_javascript('document.body.style.justifyContent = "center"')
    ui.run_javascript('document.body.style.alignItems = "center"')
    ui.run_javascript('document.body.style.height = "100vh"')
    ui.run_javascript('document.body.style.backgroundColor = "#f0f0f0"')
    ui.run_javascript('document.body.style.fontFamily = "Arial, sans-serif"')
    ui.run_javascript('document.body.style.color = "#333"')
    ui.run_javascript('document.body.style.padding = "20px"')
    ui.run_javascript('document.body.style.display = "flex"')
    ui.run_javascript('document.body.style.justifyContent = "center"')
    ui.run_javascript('document.body.style.alignItems = "center"')
    ui.run_javascript('document.body.style.height = "100vh"')
    ui.run_javascript('document.body.style.backgroundColor = "#f0f0f0"')
    ui.run_javascript('document.body.style.fontFamily = "Arial, sans-serif"')
    ui.run_javascript('document.body.style.color = "#333"')
    ui.run_javascript('document.body.style.padding = "20px"')
    ui.run_javascript('document.body.style.display = "flex"')
    ui.run_javascript('document.body.style.justifyContent = "center"')
    ui.run_javascript('document.body.style.alignItems = "center"')
    ui.run_javascript('document.body.style.height = "100vh"')
    ui.run_javascript('document.body.style.backgroundColor = "#f0f0f0"')
    ui.run_javascript('document.body.style.fontFamily = "Arial, sans-serif"')
    ui.run_javascript('document.body.style.color = "#333"')
    ui.run_javascript('document.body.style.padding = "20px"')       

