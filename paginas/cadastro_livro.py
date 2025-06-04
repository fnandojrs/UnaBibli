from nicegui import ui

@ui.page('/cadastro_livro')
def cadastro_livro():
    ui.label('Cadastro de Livro')
    ui.input('Título')
    ui.input('Autor')
    ui.button('Salvar', on_click=lambda: ui.notify('Livro salvo'))
    ui.button('Voltar', on_click=lambda: ui.open('/dashboard'))
