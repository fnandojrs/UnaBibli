from nicegui import ui
import pymysql

def verificar_status_livro(livro_id):
    try:
        conexao = pymysql.connect(
            host='metro.proxy.rlwy.net',
            port=25858,
            user='root',
            password='bojFqQXsCRiLKyzbmgsPidyeQLJAVlsE',
            database='railway',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conexao.cursor() as cursor:
            sql = "SELECT locado FROM livros WHERE id = %s"
            cursor.execute(sql, (livro_id,))
            resultado = cursor.fetchone()

            if resultado is None:
                return "Livro não encontrado."

            locado = resultado['locado']
            return "Emprestado" if locado == 1 else "Livre"

    except Exception as e:
        return f"Erro na consulta: {e}"

    finally:
        if conexao:
            conexao.close()


@ui.page('/consulta')
def consulta_livros():
    with ui.column().classes('w-full items-center'):

        ui.label('Consulta de Status de Livro').classes('text-2xl font-bold mb-4')

        id_input = ui.input('ID do Livro').props('outlined').classes('w-64')
        resultado_label = ui.label('').classes('text-lg mt-4')

        def consultar():
            try:
                livro_id = int(id_input.value)
                status = verificar_status_livro(livro_id)
                resultado_label.text = f'Status: {status}'
            except ValueError:
                resultado_label.text = 'ID inválido.'

        ui.button('Consultar', on_click=consultar).classes('mt-2')
