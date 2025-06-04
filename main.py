# main.py
from nicegui import ui, app






# 2) Serve estáticos e CSS (opcionalmente pode ficar nas próprias páginas também)
app.add_static_files('/static', 'static')
ui.add_head_html('<link rel="stylesheet" href="/static/custom.css">')

# 3) Importa TODOS os módulos de rota; cada um deve usar request.session
import paginas.login
import paginas.dashboard
import paginas.cadastro_ay
import paginas.cad_livros
import paginas.movimentacao
import paginas.consulta

# 4) Sobe a aplicação
ui.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
