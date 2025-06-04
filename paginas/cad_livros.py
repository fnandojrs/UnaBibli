from nicegui import ui
from datetime import datetime

import pymysql

def conectar():
    return pymysql.connect(
        host='metro.proxy.rlwy.net',
        port=25858,
        user='root',
        password='bojFqQXsCRiLKyzbmgsPidyeQLJAVlsE',
        database='railway'
    )




ano_atual = datetime.now().year
anos = [str(ano) for ano in range(ano_atual, 1950, -1)]

categorias = [
    'Romance', 'Ficção Científica', 'Fantasia', 'Mistério', 'Suspense', 'Terror',
    'Aventura', 'Drama', 'Biografia', 'Autobiografia', 'História', 'Ciência',
    'Tecnologia', 'Autoajuda', 'Psicologia', 'Religião', 'Espiritualidade',
    'Filosofia', 'Educação', 'Didático', 'Infantil', 'Juvenil', 'HQ e Mangá',
    'Clássicos', 'Poesia', 'Economia', 'Administração', 'Negócios', 'Direito',
    'Política', 'Sociologia', 'Saúde e Bem-estar', 'Culinária', 'Viagem',
    'Esportes', 'Arte', 'Música', 'Fotografia'
]



@ui.page('/cad_livros')
def cad_livros():

    with ui.column().classes("w-full items-center pt-1"):
        ui.label('📚 Cadastro de Livros').classes("text-3xl font-bold")
        ui.label('Preencha os campos abaixo para cadastrar um novo livro').classes("text-lg")

    with ui.column().classes("w-full items-center pt-1"):
        with ui.card().classes('w-full max-w-screen-md shadow-lg p-4'):
            with ui.grid(columns=1).classes('gap-4 w-full'):
                titulo_input = ui.input(label='Título', placeholder='TÍTULO') \
                    .props('outlined dense') \
                    .classes('w-full').style('text-transform: uppercase;')

                autor_input = ui.input(label='Autor', placeholder='AUTOR') \
                    .props('outlined dense') \
                    .classes('w-full').style('text-transform: uppercase;')

                with ui.row().classes('gap-4 w-full'):
                    ano_input = ui.select(anos, label='Ano') \
                        .props('outlined dense') \
                        .classes('w-full max-w-[160px]')

                    categoria_input = ui.select(categorias, label='Categoria') \
                        .props('outlined dense') \
                        .classes('w-full')

                id_input = ui.input(label='Número de Identificação', placeholder='Digite um número') \
                    .props('type=number outlined dense') \
                    .classes('w-full max-w-[300px]') \
                    .style('text-transform: uppercase;')
                id_input.on('keypress', lambda e: e.preventDefault() if not e.key.isdigit() else None)

                def adicionar_livro():
                    if all([titulo_input.value, autor_input.value, ano_input.value, categoria_input.value, id_input.value]):
                        try:
                            conn = conectar()
                            cursor = conn.cursor()

                            sql = '''
                                INSERT INTO livros (titulo ,autor , categoria, ano, num_id)
                                VALUES (%s, %s, %s, %s, %s)
                            '''
                            valores = (
                                titulo_input.value,
                                autor_input.value,
                                categoria_input.value,
                                int(ano_input.value),
                                int(id_input.value)
                            )

                            cursor.execute(sql, valores)
                            conn.commit()
                            cursor.close()
                            conn.close()

                            ui.notify('📚 Livro cadastrado com sucesso!')

                            # Limpa os campos
                            titulo_input.value = ''
                            autor_input.value = ''
                            ano_input.value = ''
                            categoria_input.value = ''
                            id_input.value = ''

                        except Exception as e:
                            ui.notify(f'❌ Erro ao inserir no banco: {e}')

            with ui.row().classes("w-full justify-center gap-4 pt-4"):
                ui.button('Cadastrar Livro', on_click=adicionar_livro).props('color=primary unelevated')
                ui.button('Voltar', on_click=lambda: ui.navigate.to('/dashboard')).props('color=secondary unelevated')
                ui.button('Consultar Livros', on_click=lambda: ui.navigate.to('/consulta')).props('color=secondary unelevated')
