from nicegui import ui, app


# …



@ui.page('/dashboard')
def dashboard():
    

    

    # # se não tiver sessão válida, volta ao login
    # if not tipo:
    #     ui.notify(f'Você precisa fazer login antes.{tipo}', type='negative')
    #     #ui.navigate('/')      # ou ui.navigate.to('/')
    #     return           # interrompe a montagem da página

    # ui.notify(f'Login realizado como {tipo}', type='success')

    with ui.column().classes("w-full items-center pt-4"):
        ui.label("📚 Sistema da Biblioteca").classes("text-3xl font-bold")
       
    with ui.column().classes("w-full items-center pt-4"):
        with ui.card().style('width: 250px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'):
            ui.button('Cadastrar Usuário', on_click=lambda: ui.navigate.to('/cadastro_ay')).classes('w-full mb-2')
            ui.button('Cadastrar Livro', on_click=lambda: ui.navigate.to('/cad_livros')).classes('w-full mb-2')
            ui.button('Registrar Movimento', on_click=lambda: ui.navigate.to('/movimentacao')).classes('w-full mb-2')
            ui.button('Consulta', on_click=lambda: ui.navigate.to('/consulta')).classes('w-full')