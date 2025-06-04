from nicegui import ui
import pymysql
import pandas as pd
from datetime import datetime, timedelta
from dateutil.parser import parse  

def conectar():
    return pymysql.connect(
        host='metro.proxy.rlwy.net',
        port=25858,
        user='root',
        password='bojFqQXsCRiLKyzbmgsPidyeQLJAVlsE',
        database='railway'
    )

def buscar_livros(usuario_id, resultado_area):
    try:
        conexao = conectar()
        query = """
        SELECT
            m.livro_id,
            l.titulo AS Título,
            l.autor AS Autor,
            DATE_FORMAT(m.DT_mov, '%%d/%%m/%%Y %%H:%%i') AS 'Data do Empréstimo',
            DATE_FORMAT(DATE_ADD(m.DT_mov, INTERVAL 7 DAY), '%%d/%%m/%%Y') AS 'Data Devolução Prevista',
            CASE 
                WHEN CURDATE() > DATE_ADD(m.DT_mov, INTERVAL 7 DAY) THEN DATEDIFF(CURDATE(), DATE_ADD(m.DT_mov, INTERVAL 7 DAY))
                ELSE 0
            END AS 'Dias em Atraso',
            CASE 
                WHEN CURDATE() > DATE_ADD(m.DT_mov, INTERVAL 7 DAY) THEN ROUND(DATEDIFF(CURDATE(), DATE_ADD(m.DT_mov, INTERVAL 7 DAY)) * 1.90, 2)
                ELSE 0.00
            END AS 'Multa (R$)'
        FROM movimentos m
        JOIN livros l ON l.id = m.livro_id
        WHERE m.usuario_id = %s
          AND m.tipo_movimento = 'S'
          AND m.id = (
              SELECT MAX(m2.id)
              FROM movimentos m2
              WHERE m2.livro_id = m.livro_id
          )
        """
        df = pd.read_sql(query, conexao, params=(usuario_id,))
        conexao.close()

        resultado_area.clear()
        if df.empty:
            ui.label('✅ Nenhum livro locado no momento.').classes('text-green-600')
        else:
            df['Multa (R$)'] = df['Multa (R$)'].astype(float).round(2)
            multa_total = df['Multa (R$)'].sum()

            rows = []
            for _, row in df.iterrows():
                dias_atraso = int(row['Dias em Atraso'])
                multa = float(row['Multa (R$)'])

                rows.append({
                    'Título': row['Título'],
                    'Autor': row['Autor'],
                    'Data do Empréstimo': row['Data do Empréstimo'],
                    'Data Devolução Prevista': row['Data Devolução Prevista'],
                    'Dias em Atraso': dias_atraso,
                    'Multa (R$)': f"{multa:.2f}",
                })

            columns = [
                {'name': 'Título', 'label': 'Título', 'field': 'Título', 'align': 'left'},
                {'name': 'Autor', 'label': 'Autor', 'field': 'Autor', 'align': 'left'},
                {'name': 'Data do Empréstimo', 'label': 'Data do Empréstimo', 'field': 'Data do Empréstimo', 'align': 'center'},
                {'name': 'Data Devolução Prevista', 'label': 'Prev. Devolução', 'field': 'Data Devolução Prevista', 'align': 'center'},
                {'name': 'Dias em Atraso', 'label': 'Dias Atraso', 'field': 'Dias em Atraso', 'align': 'center'},
                {'name': 'Multa (R$)', 'label': 'Multa (R$)', 'field': 'Multa (R$)', 'align': 'right'},
            ]

            with resultado_area:
                ui.table(columns=columns, rows=rows).classes('w-full')
                ui.label(f"💰 Total de multas: R$ {multa_total:.2f}").classes('mt-4 text-lg text-red-600 font-bold')
    except Exception as e:
        resultado_area.clear()
        ui.label(f"Erro ao buscar livros: {str(e)}").classes('text-red-500')









def consultar_historico():
    with ui.dialog().classes('w-[90vw]') as dialog, ui.card().classes('w-full'):


        ui.label('🔍 Buscar Usuário').classes('text-xl font-bold mb-4')
        campo_busca = ui.input('Digite o nome do usuário').classes('w-full')
        resultado_area = ui.column().classes('w-full mt-4')

        def buscar_usuario():
            if not campo_busca.value:
                ui.notify('Por favor, digite o nome do usuário.', type='negative')
                return
            resultado_area.clear()
            
            try:
                nome = (campo_busca.value or '').strip()
                conexao = conectar()
                query = "SELECT id, nome FROM usuarios WHERE ativo = 1 AND nome LIKE %s ORDER BY nome"
                df = pd.read_sql(query, conexao, params=(f"%{nome}%",))
                conexao.close()

                resultado_area.clear()
                if df.empty:
                    ui.label('Nenhum usuário encontrado.').classes('text-red-500')
                else:
                    for _, row in df.iterrows():
                        with resultado_area:
                            ui.button(f"{row['nome']}", on_click=lambda r=row: buscar_livros(r['id'], resultado_area)).props('color=primary outline')
            except Exception as e:
                resultado_area.clear()
                ui.label(f"Erro: {str(e)}").classes('text-red-500')

        ui.button('Buscar', on_click=buscar_usuario).classes('bg-blue-500 text-white px-4 py-2 rounded-lg mt-2')
        ui.button('Fechar', on_click=dialog.close).classes('bg-gray-500 text-white px-4 py-2 rounded-lg mt-2')

    dialog.open()

def registrar_emprestimo():
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-2xl'):
        ui.label('📚 Registrar Empréstimo').classes('text-xl font-bold mb-4')
        campo_busca = ui.input('Digite o nome do usuário').classes('w-full')
        resultado_area = ui.column().classes('w-full mt-4')

        livros_para_emprestar = []
        tabela_area = ui.column().classes('w-full mt-4')

        def adicionar_livro(usuario_id, num_id):
            if any(livro['num_id'] == num_id for livro in livros_para_emprestar):
                ui.notify(f"⚠️ O livro com código {num_id} já está na lista.", type='warning')
                return

            try:
                conexao = conectar()
                cursor = conexao.cursor()
                cursor.execute("SELECT id, titulo, locado FROM livros WHERE num_id = %s", (num_id,))
                livro = cursor.fetchone()
                if not livro:
                    ui.notify(f"❌ Livro com num_id {num_id} não encontrado.", type='warning')
                    return

                livro_id, titulo, locado = livro
                if locado == '1':
                    ui.notify(f"❌ O livro '{titulo}' já está emprestado.", type='warning')
                    return

                livros_para_emprestar.append({
                    'livro_id': livro_id,
                    'titulo': titulo,
                    'num_id': num_id,
                    'usuario_id': usuario_id
                })

                atualizar_tabela()
                input_numid.set_value('')
                conexao.close()
            except Exception as e:
                ui.notify(f"Erro ao buscar livro: {str(e)}", type='negative')

        def atualizar_tabela():
            tabela_area.clear()
            if not livros_para_emprestar:
                return

            columns = [
                {'name': 'Título', 'label': 'Título', 'field': 'titulo', 'align': 'left'},
                {'name': 'num_id', 'label': 'Código', 'field': 'num_id', 'align': 'center'}
            ]

            rows = [
                {
                    'titulo': livro['titulo'],
                    'num_id': livro['num_id']
                }
                for livro in livros_para_emprestar
            ]

            with tabela_area:
                ui.label('📘 Livros para Empréstimo:').classes('font-bold')
                ui.table(columns=columns, rows=rows).classes('w-full')

        def concluir_emprestimos():
            try:
                conexao = conectar()
                cursor = conexao.cursor()

                for livro in livros_para_emprestar:
                    cursor.execute("""
                        INSERT INTO movimentos (livro_id, usuario_id, tipo_movimento, DT_mov)
                        VALUES (%s, %s, 'S', %s)
                    """, (livro['livro_id'], livro['usuario_id'], datetime.now()))
                    cursor.execute("UPDATE livros SET locado = '1' WHERE id = %s", (livro['livro_id'],))

                conexao.commit()
                conexao.close()
                ui.notify("✅ Empréstimos registrados com sucesso.", type='positive')
                livros_para_emprestar.clear()
                tabela_area.clear()
                dialog.close()
            except Exception as e:
                ui.notify(f"Erro ao concluir empréstimos: {str(e)}", type='negative')

        def buscar_usuario():
            try:
                nome = (campo_busca.value or '').strip()
                conexao = conectar()
                query = "SELECT id, nome FROM usuarios WHERE ativo = 1 AND nome LIKE %s ORDER BY nome"
                df = pd.read_sql(query, conexao, params=(f"%{nome}%",))
                conexao.close()

                resultado_area.clear()
                if df.empty:
                    ui.label('Nenhum usuário encontrado.').classes('text-red-500')
                else:
                    for _, row in df.iterrows():
                        with resultado_area:
                            ui.label(f"Usuário: {row['nome']}").classes('font-semibold')
                            nonlocal input_numid
                            input_numid = ui.input('Digite num_id do Livro e pressione ENTER').props('type=number').classes('w-64')
                            input_numid.on('keydown.enter', lambda e, r=row: adicionar_livro(r['id'], input_numid.value))
                            ui.button('Concluir Empréstimos', on_click=concluir_emprestimos).classes('bg-green-600 text-white mt-4')
                            tabela_area
            except Exception as e:
                resultado_area.clear()
                ui.label(f"Erro: {str(e)}").classes('text-red-500')

        input_numid = None

        ui.button('Buscar Usuário', on_click=buscar_usuario).classes('bg-blue-600 text-white px-4 py-2 rounded')
        ui.button('Fechar', on_click=dialog.close).classes('bg-gray-500 text-white px-4 py-2 rounded mt-2')

    dialog.open()


# O restante do código permanece o mesmo...


def registrar_devolucao():
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-2xl'):
        ui.label('🔁 Registrar Devolução').classes('text-xl font-bold mb-4')
        campo_busca = ui.input('Digite o nome do usuário').classes('w-full')
        resultado_area = ui.column().classes('w-full mt-4')

        livros_para_devolver = []
        tabela_area = ui.column().classes('w-full mt-4')
        total_multa_label = ui.label('').classes('font-bold mt-2')

        def adicionar_livro(usuario_id, num_id):
            try:
                if any(l['num_id'] == num_id for l in livros_para_devolver):
                    ui.notify(f"⚠️ Livro com num_id {num_id} já está na lista.", type='warning')
                    return

                conexao = conectar()
                cursor = conexao.cursor()
                cursor.execute("SELECT id, titulo FROM livros WHERE num_id = %s", (num_id,))
                livro = cursor.fetchone()
                if not livro:
                    ui.notify(f"❌ Livro com num_id {num_id} não encontrado.", type='warning')
                    return

                livro_id = livro[0]
                titulo = livro[1]

                cursor.execute("""
                    SELECT
                        DT_mov,
                    CASE
                            
                            WHEN CURDATE() > DATE_ADD( m.DT_mov, INTERVAL 7 DAY ) THEN
                            ROUND( DATEDIFF( CURDATE(), DATE_ADD( m.DT_mov, INTERVAL 7 DAY )) * 1.90, 2 ) ELSE 0.00 
                        END AS 'Multa' 
                    FROM
                        movimentos m
                        JOIN livros l ON l.id = m.livro_id 
                    WHERE
                        m.usuario_id = %s 
                        AND m.tipo_movimento = 'S' 
                        AND m.id = ( SELECT MAX( m2.id ) FROM movimentos m2 WHERE m2.livro_id = m.livro_id ) 
                        AND l.id = %s
                """, (usuario_id,livro_id,))
                saida = cursor.fetchone()
                if not saida:
                    ui.notify(f"⚠️ Livro {titulo} não tem registro de saída.", type='warning')
                    return

                multa = saida[1]

                livros_para_devolver.append({
                    'livro_id': livro_id,
                    'titulo': titulo,
                    'num_id': num_id,
                    'multa': multa,
                    'usuario_id': usuario_id
                })

                atualizar_tabela()
                input_numid.set_value('')

                conexao.close()
            except Exception as e:
                ui.notify(f"Erro ao buscar livro: {str(e)}", type='negative')

        def atualizar_tabela():
            tabela_area.clear()
            if not livros_para_devolver:
                total_multa_label.text = ''
                return

            columns = [
                {'name': 'Título', 'label': 'Título', 'field': 'titulo', 'align': 'left'},
                {'name': 'num_id', 'label': 'Código', 'field': 'num_id', 'align': 'center'},
                {'name': 'Multa', 'label': 'Multa', 'field': 'multa', 'align': 'right'}
            ]

            rows = [
                {
                    'titulo': livro['titulo'],
                    'num_id': livro['num_id'],
                    'multa': f"{livro['multa']:.2f}"
                }
                for livro in livros_para_devolver
            ]

            total_multa = sum(l['multa'] for l in livros_para_devolver)
            with tabela_area:
                ui.label('📚 Livros para Devolução:').classes('font-bold')
                ui.table(columns=columns, rows=rows).classes('w-full')
                total_multa_label.text = f'Total de Multas: R$ {total_multa:.2f}'
                ui.element('div').classes('h-2')  # espaço inferior

        def concluir_devolucoes():
            try:
                conexao = conectar()
                cursor = conexao.cursor()

                for livro in livros_para_devolver:
                    cursor.execute("""
                        INSERT INTO movimentos (livro_id, usuario_id, tipo_movimento, DT_mov, Multa)
                        VALUES (%s, %s, 'E', %s, %s)
                    """, (livro['livro_id'], livro['usuario_id'], datetime.now(), livro['multa']))
                    cursor.execute("UPDATE livros SET locado = '0' WHERE id = %s", (livro['livro_id'],))

                conexao.commit()
                conexao.close()
                ui.notify("✅ Devoluções registradas com sucesso.", type='positive')
                livros_para_devolver.clear()
                tabela_area.clear()
                total_multa_label.text = ''
                dialog.close()
            except Exception as e:
                ui.notify(f"Erro ao concluir devoluções: {str(e)}", type='negative')

        def buscar_usuario():
            try:
                nome = (campo_busca.value or '').strip()
                conexao = conectar()
                query = "SELECT id, nome FROM usuarios WHERE ativo = 1 AND nome LIKE %s ORDER BY nome"
                df = pd.read_sql(query, conexao, params=(f"%{nome}%",))
                conexao.close()

                resultado_area.clear()
                if df.empty:
                    ui.label('Nenhum usuário encontrado.').classes('text-red-500')
                else:
                    for _, row in df.iterrows():
                        with resultado_area:
                            ui.label(f"Usuário: {row['nome']}").classes('font-semibold')
                            nonlocal input_numid
                            input_numid = ui.input('Digite num_id do Livro e pressione ENTER').props('type=number').classes('w-64')
                            input_numid.on('keydown.enter', lambda e, r=row: adicionar_livro(r['id'], input_numid.value))
                            ui.button('Concluir Devoluções', on_click=concluir_devolucoes).classes('bg-green-600 text-white mt-4')
                            tabela_area
            except Exception as e:
                resultado_area.clear()
                ui.label(f"Erro: {str(e)}").classes('text-red-500')

        input_numid = None

        ui.button('Buscar Usuário', on_click=buscar_usuario).classes('bg-blue-600 text-white px-4 py-2 rounded')
        ui.button('Fechar', on_click=dialog.close).classes('bg-gray-500 text-white px-4 py-2 rounded mt-2')

    dialog.open()



@ui.page('/movimentacao')
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
                ui.button('Pesquisar Usuário', on_click=consultar_historico).props('color=primary unelevated')
                ui.button('Registrar Empréstimo', on_click=registrar_emprestimo).props('color=primary unelevated')
                ui.button('Registrar Devolução', on_click=registrar_devolucao).props('color=primary unelevated')

    ui.run_javascript('document.title = "Movimentações - Biblioteca"')
