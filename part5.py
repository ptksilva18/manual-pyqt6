# -*- coding: utf-8 -*-
"""Parte V — Projeto integrador (Capítulo 31), referências e glossário (Step 5, Rev. 0)."""
from blocks import ST_FIN, bl, ch, flat, h2, img, lst, nl, note, out, p, part, snip, tab

NOTA_APP = "✔ Executado pela Listagem 31.13 (testes, autoteste do código-fonte e do executável congelado)."

CAP31 = flat(
    ch("Projeto integrador: aplicação técnica de engenharia", ST_FIN, [
        "Aplicar, em um único projeto, os conceitos de todas as Partes.",
        "Documentar requisitos, arquitetura e decisões técnicas.",
        "Entregar a aplicação testada, empacotada e documentada.",
    ]),
    p("Este capítulo reúne o manual em uma aplicação completa: o **Monitor de Ensaios de Estanqueidade**, "
      "ferramenta para registrar, analisar e documentar testes de pressão de linhas, vasos e equipamentos. "
      "O código (cerca de 900 linhas, incluindo testes) está organizado como um pacote Python profissional e "
      "foi verificado de ponta a ponta: testes automatizados, execução roteirizada sem interação "
      "(*autoteste*), geração do relatório PDF, empacotamento com PyInstaller e reexecução do executável "
      "congelado (Listagem 31.13)."),

    h2("Requisitos e escopo"),
    tab("Requisitos do Monitor de Ensaios", ["ID", "Requisito", "Onde é atendido"],
        [["RF-01", "Cadastrar ensaios com código único, descrição e critério de aceitação",
          "repositorio.py, janela.py"],
         ["RF-02", "Importar leituras (tempo, pressão, temperatura) de CSV com ';' ou ',' e vírgula decimal",
          "importacao.py"],
         ["RF-03", "Calcular queda de pressão, queda percentual e taxa de queda por regressão linear",
          "dominio.py"],
         ["RF-04", "Compensar a variação térmica do fluido aprisionado (dp/dT informado no critério)",
          "dominio.py"],
         ["RF-05", "Aprovar ou reprovar o ensaio, listando todos os motivos de reprovação", "dominio.py"],
         ["RF-06", "Exibir leituras em tabela e gráfico, e o resultado em painel acoplável", "janela.py"],
         ["RF-07", "Emitir relatório PDF com resultado, critério, gráfico e leituras", "relatorio.py"],
         ["RNF-01", "A interface não pode congelar durante a análise", "servicos.py (QThreadPool)"],
         ["RNF-02", "Regras de cálculo testáveis sem interface e verificadas contra referência independente",
          "tests/test_dominio.py (NumPy)"],
         ["RNF-03", "Dados persistentes na pasta de dados do usuário; estado da janela restaurado",
          "app.py (QStandardPaths), QSettings"],
         ["RNF-04", "Executável independente de instalação do Python", "monitor_ensaios.spec"]],
        [1000, 5300, 2771], font=17),
    p("Fora do escopo desta versão: edição manual de leituras, múltiplos usuários simultâneos e aquisição "
      "direta do instrumento — esta última pode ser acrescentada com a `QSerialPort` do Capítulo 21, "
      "alimentando o mesmo modelo de leituras."),
    note("ATENÇÃO", "O critério de aceitação do exemplo (duração mínima, queda percentual e taxa máximas, "
                    "coeficiente dp/dT) é ilustrativo. Em uso real, os valores e o método de compensação "
                    "térmica devem vir do procedimento de teste e da norma aplicável ao equipamento."),

    h2("Arquitetura da solução"),
    p("A aplicação segue as camadas do Capítulo 27. O **domínio** (`dominio.py`) é Python puro; "
      "**infraestrutura** (`repositorio.py`, `importacao.py`) lida com SQLite e arquivos; **serviços** "
      "(`servicos.py`, `relatorio.py`) executam a análise em segundo plano e produzem o PDF; a "
      "**apresentação** (`modelos.py`, `janela.py`) usa Model/View, ações e sinais. O módulo `app.py` é a "
      "**raiz de composição**: cria a `QApplication`, escolhe o banco de dados, injeta repositório e serviço "
      "na janela e oferece o modo `--autoteste`."),
    img("Arquitetura do projeto integrador", "f31_1_integrador.png", 15.5),
    tab("Módulos do projeto integrador e capítulos de referência", ["Módulo", "Conteúdo", "Capítulos"],
        [["dominio.py", "dataclasses, regressão linear, compensação térmica, critério", "3, 27"],
         ["importacao.py", "csv.Sniffer, conversão de vírgula decimal, erros por linha", "16"],
         ["repositorio.py", "SQLite com transações e chave estrangeira", "15, 27"],
         ["modelos.py", "QAbstractTableModel, papéis e cabeçalhos", "14"],
         ["servicos.py", "QThreadPool, QRunnable e sinais entre threads", "20"],
         ["relatorio.py", "QTextDocument, QPdfWriter, Matplotlib", "17, 22"],
         ["janela.py", "QMainWindow, QAction, QSplitter, QDockWidget, pyqtgraph", "7, 8, 9, 22"],
         ["app.py", "composição, QStandardPaths, QSettings, autoteste", "4, 13, 27"],
         ["tests/", "pytest e pytest-qt", "28"],
         ["monitor_ensaios.spec", "PyInstaller (onedir)", "30"]],
        [2300, 4900, 1871], font=17),
    lst("c31_app/ensaios/app.py", "app.py — raiz de composição, pastas de dados e autoteste", nota=NOTA_APP),
    p("O pacote também tem `ensaios/__init__.py` (versão) e `ensaios/__main__.py`, que permite executar com "
      "`python -m ensaios`:"),
    snip(["import sys", "", "from .app import main", "", "sys.exit(main(sys.argv))"]),
    p("No modo `--autoteste`, o banco SQLite e o arquivo de configuração (`QSettings` em formato INI) vão "
      "para a pasta informada — o teste nunca toca nos dados reais do usuário."),

    h2("Interface principal"),
    p("A janela combina o que foi visto nas Partes I e II: ações com atalhos padrão "
      "(`QKeySequence.StandardKey.New`), menu e barra de ferramentas compartilhando as mesmas `QAction`s, "
      "`QSplitter` com a lista de ensaios e as abas de gráfico e leituras, e um `QDockWidget` com o "
      "resultado. A habilitação das ações acompanha o estado (`_atualizar_acoes`): não é possível analisar "
      "sem leituras nem emitir relatório sem resultado. Os diálogos (`QInputDialog`, `QFileDialog`, "
      "`QMessageBox`) só aparecem quando os argumentos não são fornecidos — o que permite testar as ações "
      "sem interação."),
    lst("c31_app/ensaios/janela.py", "janela.py — janela principal, ações e integração dos componentes",
        nota=NOTA_APP),
    img("Janela principal do Monitor de Ensaios após o autoteste", "f31_2_janela.png", 15.5),
    p("Repare em `_ao_concluir()`: se o usuário trocou de ensaio enquanto a análise rodava, o resultado que "
      "chega é descartado. Esse cuidado é indispensável sempre que uma tarefa assíncrona termina depois que "
      "o contexto que a pediu mudou."),

    h2("Modelo de dados e persistência"),
    p("As leituras chegam de registradores de pressão em CSV. O arquivo de exemplo traz 60 min de patamar a "
      "345 bar com aquecimento de 0,57 °C do fluido:"),
    lst("c31_app/dados/TH-01.csv", "dados/TH-01.csv — leituras de exemplo", lang="text",
        nota="✔ Lido pelo autoteste e pelos testes da Listagem 31.11."),
    p("O domínio define três objetos imutáveis (`Leitura`, `Criterio`, `Resultado`) e a função `analisar()`. "
      "A pressão final é corrigida para a temperatura inicial por p_corr = p − k·(T − T0), em que k é o "
      "coeficiente dp/dT do critério; a taxa de queda vem da inclinação da reta de mínimos quadrados sobre "
      "as pressões corrigidas, o que a torna menos sensível a uma única leitura ruidosa do que a diferença "
      "entre extremos. Todas as falhas do critério são acumuladas em `motivos`, para que o relatório diga "
      "**por que** o ensaio foi reprovado."),
    lst("c31_app/ensaios/dominio.py", "dominio.py — regras de análise em Python puro", nota=NOTA_APP),
    lst("c31_app/ensaios/importacao.py", "importacao.py — leitura de CSV com detecção de separador",
        nota=NOTA_APP),
    p("A persistência usa o `sqlite3` da biblioteca padrão, com transações (`with self.con`) e exclusão "
      "em cascata das leituras. O critério é gravado como JSON a partir da *dataclass* — acrescentar um "
      "campo ao critério não exige migração de esquema. Para telas centradas em tabelas editáveis, os "
      "modelos SQL do Qt (Capítulo 15) seriam uma alternativa igualmente válida."),
    lst("c31_app/ensaios/repositorio.py", "repositorio.py — persistência em SQLite", nota=NOTA_APP),
    lst("c31_app/ensaios/modelos.py", "modelos.py — modelos de tabela para ensaios e leituras",
        nota=NOTA_APP),

    h2("Cálculos em segundo plano e gráficos"),
    p("A análise de um ensaio é rápida, mas o padrão precisa valer para cálculos longos (milhares de "
      "leituras, ajustes não lineares). O serviço entrega a tarefa a um `QThreadPool` e devolve o resultado "
      "por sinal: o objeto de sinais vive na thread da GUI, de modo que as emissões feitas na thread do pool "
      "chegam enfileiradas e os slots podem atualizar widgets com segurança (Capítulo 20). A lista de "
      "leituras é copiada antes de ir para o pool, para que a thread não compartilhe estado mutável com a "
      "interface."),
    lst("c31_app/ensaios/servicos.py", "servicos.py — análise em QThreadPool com resultado por sinal",
        nota=NOTA_APP),
    p("O gráfico da janela é um `PlotWidget` do pyqtgraph, atualizado com `setData()` a cada troca de "
      "ensaio; no relatório, a mesma série é desenhada com Matplotlib, que produz imagem com qualidade de "
      "impressão (Capítulo 22)."),

    h2("Relatórios em PDF"),
    p("O relatório é montado em HTML — tabelas, cores e listas — e convertido em PDF pelo `QTextDocument`, "
      "que pagina o conteúdo automaticamente no tamanho útil da folha A4 definido no `QPdfWriter`. O "
      "gráfico Matplotlib é gerado em memória (PNG) e registrado no documento com `addResource()` sob a URL "
      "`grafico://pressao`, referenciada pela tag `<img>`. Nenhum arquivo temporário é necessário."),
    lst("c31_app/ensaios/relatorio.py", "relatorio.py — HTML + Matplotlib → QTextDocument → PDF",
        nota=NOTA_APP),
    img("Primeira página do relatório PDF gerado pelo autoteste", "f31_3_relatorio.png", 12.0),

    h2("Testes, empacotamento e entrega"),
    p("Os testes do domínio verificam valores calculados à mão e comparam a regressão linear com a do "
      "NumPy (`numpy.polyfit`) — uma verificação cruzada independente. Os testes de interface exercitam o "
      "fluxo completo com pytest-qt, inclusive a espera pelo sinal da thread do pool, e os caminhos de erro, "
      "substituindo as caixas de mensagem por funções que registram o texto (`monkeypatch`)."),
    lst("c31_app/tests/test_dominio.py", "tests/test_dominio.py — testes do domínio e da importação",
        nota=NOTA_APP),
    lst("c31_app/tests/test_janela.py", "tests/test_janela.py — testes de interface com pytest-qt",
        nota=NOTA_APP),
    p("Um `conftest.py` de três linhas acrescenta a raiz do projeto ao `sys.path`, permitindo `import "
      "ensaios` sem instalar o pacote. O executável é gerado a partir do `.spec`:"),
    lst("c31_app/monitor_ensaios.spec", "monitor_ensaios.spec — empacotamento com PyInstaller",
        nota=NOTA_APP),
    p("A Listagem 31.13 é o roteiro de entrega, equivalente ao que um servidor de integração contínua "
      "executaria: testes com cobertura, autoteste a partir do código-fonte, empacotamento e autoteste do "
      "executável congelado. A entrega só é aprovada se as quatro etapas passarem."),
    lst("c31_entrega.py", "Roteiro de entrega: testes, autoteste, empacotamento e reteste do executável"),
    out("c31_entrega"),
    p("O resultado confere com o cálculo manual: a pressão final de 344,918 bar, corrigida de 0,57 °C de "
      "aquecimento com dp/dT = 0,25 bar/°C, vale 344,918 − 0,25 × 0,57 = 344,776 bar; a queda é de 0,224 bar "
      "(0,065 % de 345 bar), dentro do limite de 0,5 %. A cobertura de `app.py` aparece como 0 % porque o "
      "autoteste roda em outro processo, fora da medição do pytest-cov; ele é verificado pelas etapas 2 e 4."),

    h2("Lições aprendidas e próximos passos"),
    p("Os problemas encontrados durante o desenvolvimento do projeto integrador são típicos de aplicações "
      "reais e ilustram por que cada etapa de verificação existe:"),
    bl("**O executável congelado falhou na primeira tentativa** (\"The 'platformdirs' package is "
       "required\"): o hook de execução do `pkg_resources`, puxado indiretamente por dependências, quebrou o "
       "programa. Somente o autoteste do executável — e não os testes do código-fonte — revelou o "
       "problema. A correção (excluir `pkg_resources` e `setuptools` no `.spec`) também reduziu o pacote de "
       "515 MB para 364 MB.",
       "**Isolar o estado do teste**: o autoteste redireciona banco de dados e `QSettings` para uma pasta "
       "temporária; sem isso, executar a verificação alteraria os dados do usuário.",
       "**Resultados assíncronos podem chegar tarde**: conferir o identificador do ensaio em "
       "`_ao_concluir()` evita mostrar o resultado de um ensaio na tela de outro.",
       "**Separar o domínio pagou-se várias vezes**: as regras foram testadas em milissegundos, comparadas "
       "com o NumPy e reutilizadas sem alteração no relatório e no autoteste."),
    p("Evoluções naturais do projeto, cada uma apoiada em um capítulo do manual:"),
    nl("Aquisição direta do registrador por porta serial ou rede (Capítulo 21), com gráfico em tempo real "
       "(Capítulo 22).",
       "Edição de leituras com desfazer/refazer (`QUndoStack`, Capítulo 27).",
       "Interface traduzida (`QTranslator`, Capítulo 13) e tema escuro (Capítulo 12).",
       "Assinatura de código e instalador (Inno Setup, DMG ou AppImage, Capítulo 30).",
       "Integração contínua com a matriz de sistemas do Capítulo 28 e publicação automática dos "
       "executáveis."),
    note("DICA", "Use este projeto como modelo para as suas ferramentas: troque o domínio (por exemplo, "
                 "cálculos de dimensionamento ou de fadiga) e mantenha a estrutura de camadas, os testes e o "
                 "roteiro de entrega."),
)

REFERENCIAS = flat(
    dict(k="hu", t="Referências"),
    p("Documentação oficial e normas consultadas na elaboração deste manual (acesso em 11 nov. 2026). As "
      "versões de referência estão indicadas no Prefácio."),
    bl("BATCHELDER, N. *Coverage.py documentation*. Disponível em: https://coverage.readthedocs.io/.",
       "CX_FREEZE. *cx_Freeze documentation*. Disponível em: https://cx-freeze.readthedocs.io/.",
       "FOWLER, M. *Presentation Model*. 2004. Disponível em: "
       "https://martinfowler.com/eaaDev/PresentationModel.html.",
       "FREE SOFTWARE FOUNDATION. *GNU General Public License, version 3*. 2007. Disponível em: "
       "https://www.gnu.org/licenses/gpl-3.0.html.",
       "GAMMA, E.; HELM, R.; JOHNSON, R.; VLISSIDES, J. *Design Patterns: Elements of Reusable "
       "Object-Oriented Software*. Reading: Addison-Wesley, 1994.",
       "IETF. *RFC 6455 — The WebSocket Protocol*. 2011. Disponível em: https://www.rfc-editor.org/rfc/rfc6455.",
       "IETF. *RFC 6749 — The OAuth 2.0 Authorization Framework*. 2012. Disponível em: "
       "https://www.rfc-editor.org/rfc/rfc6749.",
       "IETF. *RFC 7636 — Proof Key for Code Exchange by OAuth Public Clients (PKCE)*. 2015. Disponível em: "
       "https://www.rfc-editor.org/rfc/rfc7636.",
       "JORDAN RUSSELL'S SOFTWARE. *Inno Setup Help*. Disponível em: https://jrsoftware.org/ishelp/.",
       "KHRONOS GROUP. *OpenGL and Vulkan Registry* (especificações). Disponível em: "
       "https://registry.khronos.org/.",
       "MATPLOTLIB DEVELOPMENT TEAM. *Matplotlib documentation*. Disponível em: https://matplotlib.org/stable/.",
       "NATIONAL MARINE ELECTRONICS ASSOCIATION. *NMEA 0183 — Standard for Interfacing Marine Electronic "
       "Devices*.",
       "NUITKA. *Nuitka User Manual*. Disponível em: https://nuitka.net/.",
       "NUMPY DEVELOPERS. *NumPy documentation*. Disponível em: https://numpy.org/doc/.",
       "PYINSTALLER DEVELOPMENT TEAM. *PyInstaller Manual*. Disponível em: https://pyinstaller.org/.",
       "PYQTGRAPH. *PyQtGraph documentation*. Disponível em: https://pyqtgraph.readthedocs.io/.",
       "PYTEST-DEV. *pytest documentation*. Disponível em: https://docs.pytest.org/.",
       "PYTEST-DEV. *pytest-qt documentation*. Disponível em: https://pytest-qt.readthedocs.io/.",
       "PYTHON PACKAGING AUTHORITY. *Python Packaging User Guide*. Disponível em: https://packaging.python.org/.",
       "PYTHON SOFTWARE FOUNDATION. *Python 3 documentation* (linguagem e biblioteca padrão). Disponível em: "
       "https://docs.python.org/3/.",
       "QASYNC. *qasync — Python library for using asyncio in Qt-based applications* (repositório). "
       "Disponível em: https://github.com/CabbageDevelopment/qasync.",
       "RIVERBANK COMPUTING. *PyQt6 Reference Guide*. Disponível em: "
       "https://www.riverbankcomputing.com/static/Docs/PyQt6/.",
       "RIVERBANK COMPUTING. *PyQt* (produto e licenciamento). Disponível em: "
       "https://www.riverbankcomputing.com/software/pyqt/.",
       "SUMMERFIELD, M. *Rapid GUI Programming with Python and Qt*. Upper Saddle River: Prentice Hall, 2007.",
       "THE QT COMPANY. *Qt 6 Documentation*. Disponível em: https://doc.qt.io/qt-6/.",
       "THE QT COMPANY. *Qt Licensing*. Disponível em: https://www.qt.io/licensing/.",
       "W3C. *Web Content Accessibility Guidelines (WCAG) 2.2*. 2023. Disponível em: "
       "https://www.w3.org/TR/WCAG22/."),
)

GLOSSARIO_TERMOS = [
    ("Ação (QAction)", "Comando reutilizável com texto, ícone, atalho e estado, compartilhado por menus, "
     "barras de ferramentas e atalhos de teclado."),
    ("Antisserrilhamento (antialiasing)", "Suavização das bordas de linhas e textos por cores "
     "intermediárias nos pixels de fronteira."),
    ("Autoteste", "Execução roteirizada e não interativa da aplicação que confere as funções essenciais; "
     "usada após o empacotamento."),
    ("Backend", "Implementação específica por trás de uma API genérica, como o plugin de áudio, de banco de "
     "dados ou de renderização em uso."),
    ("Binding", "Camada que expõe uma biblioteca escrita em uma linguagem (C++) a outra (Python); o PyQt6 é "
     "gerado com o SIP."),
    ("Blitting", "Técnica de redesenho que copia uma região já renderizada e atualiza só o que mudou."),
    ("Buffer circular", "Estrutura de tamanho fixo em que os dados novos substituem os mais antigos."),
    ("Callback", "Função passada como argumento para ser chamada quando um evento ou operação termina."),
    ("Cobertura (coverage)", "Proporção de linhas ou ramos de código executados pelos testes."),
    ("Conexão enfileirada (queued connection)", "Conexão em que o slot é executado pelo event loop da "
     "thread do receptor, com os argumentos copiados em um evento."),
    ("Congelamento (freezing)", "Empacotamento do interpretador Python, do código e das dependências em um "
     "executável distribuível."),
    ("D-Bus", "Barramento de comunicação entre processos usado em sistemas Linux de desktop."),
    ("Deadlock", "Bloqueio permanente em que duas ou mais threads esperam umas pelas outras."),
    ("Delegado (delegate)", "Objeto que desenha e edita os itens de uma visão Model/View."),
    ("Downsampling", "Redução do número de pontos de um sinal para exibição, preservando sua forma."),
    ("Enquadramento (framing)", "Regra que delimita mensagens em um fluxo contínuo de bytes, como o TCP."),
    ("Entry point", "Registro, nos metadados de um pacote instalado, de um objeto que outras aplicações "
     "podem descobrir e carregar."),
    ("Event loop", "Laço que recebe eventos do sistema e de timers e os despacha aos objetos Qt; iniciado "
     "por exec()."),
    ("Fixture", "No pytest, recurso preparado para um teste e liberado ao fim dele (ex.: qtbot)."),
    ("Flag", "Enum cujos membros podem ser combinados com o operador | (ex.: Qt.AlignmentFlag)."),
    ("GIL", "Global Interpreter Lock: trava do CPython que permite que apenas uma thread execute bytecode "
     "Python por vez (no CPython padrão, sem a variante free-threaded)."),
    ("High-DPI", "Telas de alta densidade de pixels; o Qt escala a interface pelo devicePixelRatio."),
    ("Hook (PyInstaller)", "Script que informa ao PyInstaller arquivos, módulos e plugins adicionais de um "
     "pacote."),
    ("i18n / l10n", "Internacionalização (preparar o código para tradução) e localização (traduzir e "
     "adaptar a uma região)."),
    ("Injeção de dependências", "Técnica em que um objeto recebe prontas as dependências de que precisa, em "
     "vez de criá-las."),
    ("Introspecção", "Consulta, em tempo de execução, da estrutura de objetos, classes e módulos."),
    ("Layout", "Gerenciador que posiciona e dimensiona widgets automaticamente."),
    ("Metaobjeto", "Descrição em tempo de execução de uma classe QObject: sinais, slots, propriedades e "
     "enums."),
    ("Modal", "Janela que bloqueia a interação com outras janelas até ser fechada."),
    ("Model/View", "Arquitetura do Qt que separa os dados (modelo) da apresentação (visão) e da edição "
     "(delegado)."),
    ("MVP / MVVM", "Padrões de apresentação: Model-View-Presenter e Model-View-ViewModel."),
    ("Mutex", "Primitiva de exclusão mútua que garante que só uma thread execute uma seção crítica."),
    ("NMEA 0183", "Padrão de sentenças de texto para equipamentos de navegação, como receptores GNSS."),
    ("Notarização", "Verificação automatizada da Apple exigida para distribuir aplicações fora da App "
     "Store no macOS."),
    ("OAuth 2.0 / PKCE", "Protocolo de autorização delegada; o PKCE protege o fluxo de código de "
     "autorização em aplicações públicas."),
    ("Offscreen", "Plataforma do Qt que cria janelas apenas em memória, sem tela; usada em testes."),
    ("Onedir / onefile", "Modos do PyInstaller: pasta com executável e bibliotecas, ou executável único "
     "autoextraível."),
    ("Paleta (QPalette)", "Conjunto de cores por papel e estado usado pelos estilos para desenhar widgets."),
    ("Plugin (Qt)", "Biblioteca carregada em tempo de execução que estende o Qt (plataforma, imagens, SQL, "
     "multimídia)."),
    ("Propriedade (pyqtProperty)", "Atributo registrado no metaobjeto, acessível por QML, QSS, animações e "
     "introspecção."),
    ("Proxy (modelo)", "Modelo intermediário que ordena, filtra ou transforma outro modelo sem copiar os "
     "dados."),
    ("QML", "Linguagem declarativa do Qt Quick para descrever interfaces e cenas."),
    ("QSS", "Qt Style Sheets: folhas de estilo com sintaxe semelhante ao CSS aplicadas a widgets."),
    ("Raiz de composição", "Ponto único da aplicação que cria e conecta as implementações concretas."),
    ("Regressão visual", "Teste que compara a renderização atual com uma imagem de referência aprovada."),
    ("RHI", "Rendering Hardware Interface: abstração do Qt sobre Direct3D, Metal, Vulkan e OpenGL."),
    ("Sandbox", "Isolamento de um processo com privilégios reduzidos, como o do Chromium no WebEngine."),
    ("Sinal / slot", "Mecanismo de comunicação do Qt: um sinal emitido chama os slots conectados a ele."),
    ("SIP", "Ferramenta da Riverbank Computing que gera os bindings do PyQt6."),
    ("Thread", "Linha de execução independente dentro de um processo."),
    ("TLS", "Transport Layer Security: protocolo de cifragem e autenticação de conexões de rede."),
    ("Undo stack", "Pilha de comandos que permite desfazer e refazer alterações (QUndoStack)."),
    ("venv", "Ambiente virtual Python isolado, com seu próprio conjunto de pacotes."),
    ("Wheel", "Formato de pacote Python pré-compilado (.whl) instalado pelo pip."),
    ("Widget", "Elemento de interface do Qt Widgets; toda janela e controle é um QWidget."),
    ("Worker", "Objeto que executa trabalho fora da thread da GUI e comunica resultados por sinais."),
    ("Xvfb", "Servidor X11 virtual, sem tela física, usado para testes gráficos em servidores Linux."),
]

GLOSSARIO = flat(
    dict(k="hu", t="Glossário"),
    p("Termos técnicos usados no manual, em ordem alfabética. Termos em inglês consagrados na prática foram "
      "mantidos, com a tradução quando usual."),
    bl(*[f"**{t}** — {d}" for t, d in sorted(GLOSSARIO_TERMOS, key=lambda x: x[0].lower())]),
)

PART5 = flat(
    part("V", "PROJETO INTEGRADOR", "Aplicação técnica completa, do requisito ao instalador", ST_FIN,
         "Capítulo 31 · Consolidação"),
    CAP31,
    REFERENCIAS,
    GLOSSARIO,
)
