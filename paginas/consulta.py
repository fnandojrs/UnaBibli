from nicegui import ui
import pandas as pd
import pymysql
from datetime import datetime

def conectar():
    return pymysql.connect(
        host='metro.proxy.rlwy.net',
        port=25858,
        user='root',
        password='bojFqQXsCRiLKyzbmgsPidyeQLJAVlsE',
        database='railway'
    )

@ui.page('/consulta')
def pagina_consulta():
    dark = ui.dark_mode()
    with ui.row().classes("justify-end w-full pr-4 pt-2"):
        ui.button('🌙', on_click=dark.enable)
        ui.button('☀️', on_click=dark.disable)
        ui.button('Voltar', on_click=lambda: ui.navigate.to('/dashboard')).props('color=secondary unelevated')

    with ui.column().classes("w-full items-center pt-4"):
        ui.label("📚 Sistema da Biblioteca").classes("text-3xl font-bold")
        ui.label("Filtre os livros por título ou autor").classes("text-lg")

    with ui.column().classes("w-full items-center"):
        filtro_por = ui.select(['Título', 'Autor'], label='🔑 Buscar por').classes("w-64")
        filtro_por.value = 'Título'  # valor padrão

        campo_busca = ui.input("🔍 Digite aqui").classes("w-96")
        mensagem = ui.label().classes("text-md py-4")

        # Botões acima da tabela
        with ui.row().classes("gap-4 py-2 justify-center"):
            def consultar():
                try:
                    conexao = conectar()
                    cursor = conexao.cursor()

                    valor = campo_busca.value or ''
                    campo_sql = 'titulo' if filtro_por.value == 'Título' else 'autor'

                    query = f"""
                        SELECT
                            titulo AS 'Título',
                            Autor AS Autor,
                            CASE
                                WHEN locado = 1 THEN
                                    DATE_FORMAT(
                                        DATE_ADD(DATE(
                                            (SELECT movimentos.DT_mov
                                            FROM movimentos
                                            WHERE movimentos.livro_id = livros.id
                                            ORDER BY movimentos.DT_mov DESC
                                            LIMIT 1)
                                        ), INTERVAL 7 DAY),
                                        '%%d/%%m/%%Y'
                                    )
                                ELSE '--------'
                            END AS 'Data Devolucao',
                            CASE
                                WHEN locado = 1 THEN 'Emprestado'
                                ELSE 'Disponível'
                            END AS 'Status'
                        FROM
                            livros


                    WHERE {campo_sql} LIKE %s
                    """
                    df = pd.read_sql(query, conexao, params=(f"%{valor}%",))
                    cursor.close()
                    conexao.close()

                    if df.empty:
                        mensagem.text = "❌ Nenhum livro encontrado."
                        tabela_area.clear()
                    else:
                        mensagem.text = f"✅ {len(df)} livro(s) encontrado(s):"
                        tabela_area.clear()
                        columns = [
                            {'name': 'Título', 'label': 'Título', 'field': 'Título', 'align': 'left'},
                            {'name': 'Autor', 'label': 'Autor', 'field': 'Autor', 'align': 'left'},
                            {'name': 'Data Devolucao', 'label': 'Data Devolucao', 'field': 'Data Devolucao', 'align': 'center'},
                            {'name': 'Status', 'label': 'Status', 'field': 'Status', 'align': 'right'},
                        ]
                        rows = df.to_dict(orient='records')
                        with tabela_area:
                            ui.table(columns=columns, rows=rows).classes('w-3/4 mx-auto')
                except Exception as e:
                    mensagem.text = f"Erro ao consultar: {str(e)}"

            def limpar():
                campo_busca.set_value('')
                mensagem.set_text('')
                tabela_area.clear()

            ui.button("🔎 Consultar Empréstimos", on_click=consultar)
            ui.button("🧹 Limpar", on_click=limpar)

        tabela_area = ui.column().classes("w-full px-8")
