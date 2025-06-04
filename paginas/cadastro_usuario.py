from nicegui import ui

@ui.page('/cadastro_usuario')
def cadastro_usuario():
    ui.label('Cadastro de Usuário')
    ui.input('Nome')
    ui.input('Email')
    ui.button('Salvar', on_click=lambda: ui.notify('Usuário salvo'))
    ui.button('Voltar', on_click=lambda: ui.navigate.to('/dashboard')).props('color=secondary unelevated')
