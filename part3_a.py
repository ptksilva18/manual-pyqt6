# -*- coding: utf-8 -*-
"""Parte III — Capítulos 20 a 22 (Step 4)."""
from blocks import ST_AVA, bl, ch, flat, h2, h3, img, lst, nl, note, out, p, snip, tab

CAP20 = flat(
    ch("Concorrência e programação assíncrona", ST_AVA, [
        "Manter a interface responsiva durante tarefas longas.",
        "Aplicar QThread, QThreadPool e primitivas de sincronização.",
        "Combinar o event loop do Qt com threading, multiprocessing e asyncio.",
    ]),
    h2("Por que nunca bloquear o event loop"),
    p("Toda a interface — pintura, teclado, mouse, temporizadores, sinais enfileirados — é processada pelo event "
      "loop da thread principal (Capítulo 4). Enquanto um slot executa, nada mais acontece: a janela não "
      "redesenha, os botões não respondem e o sistema operacional pode marcá-la como \"não respondendo\". A "
      "Listagem 20.1 mede esse efeito com um `QTimer` de 20 ms: com o cálculo na thread da GUI, o loop fica "
      "parado por 600 ms; com o mesmo cálculo em um worker, os disparos continuam regulares."),
    lst("c20_bloqueio.py", "Responsividade do event loop: cálculo na thread da GUI versus em worker"),
    out("c20_bloqueio"),
    p("O worker também é código Python e disputa o **GIL** (*Global Interpreter Lock*) com a thread da GUI. O "
      "interpretador alterna entre threads a cada 5 ms (`sys.getswitchinterval()`), o que explica o pior "
      "intervalo de algumas dezenas de milissegundos na segunda fase: a interface continua fluida, mas não há ganho de paralelismo para "
      "cálculo puramente Python. Para paralelismo real de CPU, use processos (Seção 20.6) ou bibliotecas que "
      "liberam o GIL em código nativo, como NumPy e SciPy em operações vetorizadas."),
    note("ATENÇÃO", "Widgets só podem ser criados, lidos e alterados na thread da GUI. Uma thread secundária "
                    "nunca chama `label.setText()` diretamente: ela emite um sinal, e o slot da GUI faz a "
                    "atualização. Violar essa regra produz falhas intermitentes e travamentos difíceis de "
                    "reproduzir."),

    h2("QThread"),
    p("`QThread` não é a thread: é o objeto que **gerencia** uma thread do sistema operacional. Ao chamar "
      "`start()`, a nova thread executa `run()`, cuja implementação padrão roda um event loop próprio "
      "(`exec()`). É esse event loop que permite que objetos movidos para a thread recebam sinais "
      "enfileirados."),
    h3("Padrão worker com moveToThread()"),
    p("O padrão recomendado separa o trabalho em um `QObject` (o *worker*) e o move para a thread com "
      "`moveToThread()`. A Listagem 20.2 implementa o ciclo completo: o sinal `started` dispara `executar()`, "
      "o worker publica progresso, resultado, cancelamento ou erro por sinais, e `finalizado` encerra o event "
      "loop da thread (`quit`). Os `deleteLater()` conectados a `finalizado` e a `finished` liberam o worker "
      "e a `QThread` no momento certo, sem vazamentos."),
    lst("c20_worker.py", "Padrão worker com moveToThread(): progresso, resultado, erro e cancelamento"),
    out("c20_worker"),
    img("Padrão worker com QThread e sinais enfileirados", "f20_1_worker.png", 15.0),
    p("Repare na saída: `iniciar()` e os slots de progresso rodam na thread `GUI`; `executar()` roda em "
      "`integrador-1` e `integrador-2`. O cancelamento é **cooperativo**: `requestInterruption()` apenas marca "
      "um pedido, e o worker o verifica entre blocos com `isInterruptionRequested()`. A barra parou pouco acima "
      "de 40 %, porque um bloco já estava em processamento quando o pedido chegou — comportamento correto "
      "e esperado. Por isso o botão Cancelar é desabilitado no próprio clique, evitando pedidos repetidos."),
    note("DICA", "Exceções dentro do worker não chegam à thread da GUI. Capture-as no próprio worker e "
                 "converta-as em um sinal `erro(str)`, como na Listagem 20.2; sem isso, o erro some ou encerra o "
                 "processo (Capítulo 3)."),
    h3("Subclasse de QThread: quando (não) usar"),
    p("Reimplementar `run()` é adequado para laços autocontidos que não precisam receber sinais — aquisição "
      "contínua, por exemplo. A armadilha clássica aparece na Listagem 20.3: o objeto `QThread` pertence à "
      "thread que o criou, de modo que **slots declarados na subclasse executam na thread da GUI**, não em "
      "`run()`."),
    lst("c20_qthread_sub.py", "Subclasse de QThread: run() na nova thread, slots na thread de origem"),
    out("c20_qthread_sub"),
    h3("Encerramento seguro: requestInterruption(), quit() e wait()"),
    p("Uma thread em execução ao fim do programa causa a mensagem `QThread: Destroyed while thread is still "
      "running` e pode abortar o processo. A sequência segura é: pedir a parada (`requestInterruption()` para "
      "laços em `run()`, `quit()` para o event loop do worker), aguardar com `wait()` — opcionalmente com prazo, "
      "via `QDeadlineTimer` — e só então destruir os objetos. O `closeEvent()` da Listagem 20.2 aplica essa "
      "sequência quando o usuário fecha a janela com uma tarefa em andamento. Evite `terminate()`: ele "
      "interrompe a thread em ponto arbitrário, podendo deixar mutexes travados e dados corrompidos."),

    h2("QThreadPool e QRunnable"),
    p("Para muitas tarefas curtas e independentes, criar uma `QThread` por tarefa é desperdício. O "
      "`QThreadPool` mantém threads reutilizáveis e uma fila de `QRunnable`. O pool global "
      "(`QThreadPool.globalInstance()`) usa, por padrão, uma thread por núcleo lógico; pools próprios permitem "
      "limitar a concorrência com `setMaxThreadCount()`. Como `QRunnable` não herda de `QObject`, os sinais "
      "ficam em um objeto auxiliar. O PyQt6 também aceita um *callable* Python em `start()`."),
    lst("c20_pool.py", "QThreadPool com QRunnable, sinais auxiliares e callables"),
    out("c20_pool"),
    p("`waitForDone()` bloqueia até o pool esvaziar e só deve ser usado em scripts, testes ou no encerramento. "
      "Na interface, use os sinais de conclusão. A tarefa 5 mostra o tratamento de erro: a exceção é capturada "
      "em `run()` e informada pelo sinal `falhou`."),

    h2("Sincronização"),
    p("Quando threads compartilham dados mutáveis, o acesso precisa ser coordenado. O GIL protege apenas a "
      "integridade interna do interpretador, não a lógica do programa: uma operação como `self.valor += 1` "
      "envolve leitura, soma e escrita, e outra thread pode intervir entre elas."),
    lst("c20_sync.py", "Sincronização: QMutex, QReadWriteLock, QWaitCondition e QSemaphore"),
    out("c20_sync"),
    h3("QMutex, QMutexLocker e QRecursiveMutex"),
    p("`QMutex` garante exclusão mútua: `lock()` antes da seção crítica e `unlock()` em um bloco `finally`, "
      "para que o mutex seja liberado mesmo se ocorrer exceção. Em C++, o idioma usual é o `QMutexLocker`; no "
      "PyQt6 6.12, porém, ele falhou nos testes deste manual (ver o quadro a seguir). `QRecursiveMutex` "
      "permite que a mesma thread trave o mutex mais de uma vez, útil quando um método protegido chama outro; "
      "prefira, porém, reorganizar o código para não precisar dele."),
    note("ATENÇÃO", "Com 4 threads disputando o mesmo mutex, `with QMutexLocker(mutex):` encerrou o processo com "
                    "falha de segmentação ou *abort* em 5 de 15 execuções (PyQt6 6.12.0, Python 3.13); criar o "
                    "`QMutexLocker` sem `with` também falhou (3 de 12). Com `lock()`/`unlock()` em "
                    "`try/finally` e com `threading.Lock`, foram 0 falhas em 15 execuções; `QReadLocker` e "
                    "`QWriteLocker` usados com `with` também não falharam (0 de 12). Por isso, a Listagem 20.5 "
                    "usa `lock()`/`unlock()` explícitos."),
    h3("QReadWriteLock, QReadLocker e QWriteLocker"),
    p("Quando as leituras predominam, `QReadWriteLock` permite vários leitores simultâneos e um único escritor "
      "exclusivo. `QReadLocker` e `QWriteLocker` travam no modo correspondente e liberam ao sair do bloco "
      "`with`, como na Listagem 20.5."),
    h3("QSemaphore e QWaitCondition"),
    p("`QWaitCondition` permite que uma thread durma até que outra sinalize uma condição (`wakeOne()`, "
      "`wakeAll()`); a espera libera o mutex atomicamente e o readquire ao acordar. O laço `while` em torno de "
      "`wait()` é obrigatório, pois a condição deve ser reavaliada ao acordar. O buffer limitado da listagem "
      "nunca ultrapassou 8 itens e entregou os 10 000 valores, com soma conferida. `QSemaphore` controla um "
      "número de recursos (`acquire`, `tryAcquire`, `release`); `QSemaphoreReleaser` libera "
      "automaticamente ao sair do escopo."),
    note("NOTA", "O PyQt6 não expõe `QThread.create()` (função C++ que aceita um callable). A classe "
                 "`ThreadFuncao` da Listagem 20.5 cumpre esse papel em cinco linhas."),

    h2("Comunicação thread-safe por sinais"),
    p("A emissão de um sinal é segura em qualquer thread. O **tipo de conexão** define onde o slot executa "
      "(Tabela 5.1): com `AutoConnection` (padrão), se o receptor vive em outra thread, o Qt copia os "
      "argumentos para um evento e o slot roda no event loop da thread do receptor. A Listagem 20.6 confirma "
      "cada caso e mostra `QMetaObject.invokeMethod()`, que chama um slot de outro objeto pelo nome, na "
      "thread dele."),
    lst("c20_sinais_threads.py", "Tipos de conexão entre threads e QMetaObject.invokeMethod"),
    out("c20_sinais_threads"),
    bl("**DirectConnection** executou o slot na thread `worker`: se o slot tocasse em widgets, haveria uma "
       "violação da regra da Seção 20.1.",
       "**BlockingQueuedConnection** fez o emissor esperar o slot terminar — útil para obter confirmação "
       "síncrona, mas causa *deadlock* se emissor e receptor estiverem na mesma thread.",
       "A ordem das linhas mostra que os slots enfileirados executaram depois da chamada direta, na sequência "
       "das emissões."),

    h2("Python threading, concurrent.futures e multiprocessing com Qt"),
    p("As ferramentas da biblioteca padrão convivem com o Qt desde que a regra de ouro seja respeitada: o "
      "resultado volta para a GUI por sinal. Na Listagem 20.7, `add_done_callback()` é executado na thread que "
      "concluiu o futuro; o callback apenas emite um sinal de um `QObject` que vive na GUI, e a conexão "
      "enfileirada faz o resto. A tarefa com argumento inválido mostra que exceções de processos filhos são "
      "propagadas pelo `Future`."),
    lst("c20_futures.py", "concurrent.futures com processos e threads integrados ao Qt"),
    out("c20_futures"),
    bl("**ThreadPoolExecutor**: E/S (arquivos, rede, bancos) — o GIL é liberado durante a espera.",
       "**ProcessPoolExecutor**: cálculo Python intensivo — cada processo tem seu próprio interpretador e GIL. "
       "Argumentos e resultados são serializados com `pickle`; funções precisam ser importáveis no nível do "
       "módulo.",
       "O método de início `spawn` é o padrão no Windows e no macOS e o mais seguro com Qt em qualquer "
       "sistema, porque `fork` duplica um processo que já tem threads e estado do Qt. Com `spawn`, o guarda "
       "`if __name__ == \"__main__\":` é obrigatório.",
       "Processos filhos nunca devem criar widgets nem acessar objetos Qt do processo pai."),

    h2("asyncio e o event loop do Qt (bibliotecas de integração de terceiros)"),
    p("`asyncio` tem seu próprio event loop, incompatível com `app.exec()`: dois loops não podem rodar ao mesmo "
      "tempo na mesma thread. O PyQt6 não traz integração nativa (o PySide6 oferece o módulo `QtAsyncio`); a "
      "solução usual é a biblioteca **qasync** (licença BSD), que implementa o loop do `asyncio` sobre o loop "
      "do Qt. Corrotinas e sinais passam a compartilhar a mesma thread, sem bloqueio."),
    lst("c20_asyncio.py", "asyncio sobre o event loop do Qt com qasync"),
    out("c20_asyncio"),
    p("As três consultas concorrentes levaram cerca de 0,3 s, e não 0,60 s; `asyncio.to_thread()` delegou o cálculo "
      "bloqueante a uma thread e `wait_for()` impôs prazo à consulta lenta. Use `asyncio` quando a aplicação "
      "já depende de bibliotecas assíncronas (clientes HTTP, OPC UA, MQTT); para o resto, os recursos nativos "
      "do Qt (sinais, `QNetworkAccessManager`, `QThread`) são suficientes e não acrescentam dependência."),

    h2("Progresso e cancelamento de tarefas longas"),
    p("O padrão da Listagem 20.2 resume as boas práticas:"),
    bl("Publique progresso em **percentual inteiro** e só quando ele mudar; milhares de sinais por segundo "
       "congestionam a fila de eventos da GUI.",
       "Torne o cancelamento cooperativo, com verificações em pontos seguros (entre blocos, entre arquivos).",
       "Desabilite os controles que iniciam a tarefa enquanto ela roda, e o de cancelar após o clique.",
       "Para diálogos modais de progresso, `QProgressDialog` (Capítulo 9) com `canceled` conectado a "
       "`requestInterruption()` resolve a maior parte dos casos.",
       "Garanta o encerramento no `closeEvent()` da janela e no sinal `aboutToQuit` da aplicação."),

    h2("Exercícios do capítulo"),
    nl("Modifique a Listagem 20.1 para medir o pior intervalo com o cálculo feito por `numpy.linalg.solve` de "
       "uma matriz 2000 × 2000 no worker e compare com o laço Python. Explique a diferença com base no GIL.",
       "Acrescente à Listagem 20.2 um botão Pausar/Continuar usando `QMutex` e `QWaitCondition`.",
       "Use um `QThreadPool` com `setMaxThreadCount(2)` para processar 20 arquivos CSV, exibindo o progresso "
       "global em uma `QProgressBar`.",
       "Reescreva a Listagem 20.7 para cancelar os futuros pendentes quando a janela for fechada "
       "(`Future.cancel()` e `shutdown(cancel_futures=True)`).",
       "Explique por que a Listagem 20.3 imprimiu que `slot_da_subclasse()` executou na thread da GUI e "
       "proponha a correção com o padrão worker."),
)

CAP21 = flat(
    ch("Redes, comunicação e dispositivos", ST_AVA, [
        "Consumir APIs HTTP/REST de forma assíncrona.",
        "Implementar clientes e servidores TCP, UDP e WebSocket.",
        "Comunicar-se com dispositivos seriais, Bluetooth e NFC.",
    ]),
    p("Todos os exemplos deste capítulo usam servidores locais (127.0.0.1) criados pelo próprio programa, de "
      "modo que executam sem acesso à internet e produzem saídas reproduzíveis. A API do Qt é assíncrona: "
      "nenhuma chamada bloqueia o event loop, e os resultados chegam por sinais."),
    h2("HTTP com QNetworkAccessManager"),
    h3("QNetworkRequest e QNetworkReply"),
    p("O `QNetworkAccessManager` (NAM) envia requisições e devolve imediatamente um `QNetworkReply`; o sinal "
      "`finished` indica a conclusão. Uma única instância por aplicação (ou por thread) é suficiente: ela "
      "reaproveita conexões, cookies e cache. Cada reply deve ser liberado com `deleteLater()` após o uso."),
    lst("c21_http.py", "HTTP com QNetworkAccessManager: GET/POST JSON, erros, timeout e progresso"),
    out("c21_http"),
    h3("JSON, cabeçalhos, timeouts e tratamento de erros"),
    bl("Cabeçalhos conhecidos usam `setHeader(QNetworkRequest.KnownHeaders...)`; os demais, "
       "`setRawHeader(b\"Nome\", b\"valor\")`. Na resposta, `header()` e `rawHeader()`.",
       "O código HTTP vem de `attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)`. Respostas 4xx/5xx "
       "também produzem um `error()` diferente de `NoError` (por exemplo, `ContentNotFoundError` para 404), "
       "mas o corpo de erro enviado pelo servidor continua disponível em `readAll()`.",
       "Por padrão **não há timeout de transferência** (`transferTimeout()` = 0, verificado no Qt 6.12). Defina "
       "um valor global com `QNetworkAccessManager.setTransferTimeout()` ou por requisição; ao expirar, o erro "
       "é `TimeoutError`, como na saída.",
       "No Qt 6, redirecionamentos são seguidos por padrão (`NoLessSafeRedirectPolicy`): de HTTPS para HTTP "
       "não, nos demais casos sim.",
       "Para JSON, `json.loads(bytes(reply.readAll()))` é a forma mais direta; `QJsonDocument` também serve "
       "(Capítulo 16)."),
    h3("Upload, download e progresso"),
    p("`downloadProgress(recebidos, total)` e `uploadProgress(enviados, total)` alimentam barras de progresso; "
      "`total` vale −1 quando o servidor não informa `Content-Length`. Para arquivos grandes, leia os dados "
      "incrementalmente em `readyRead` e grave-os em disco (de preferência com `QSaveFile`), em vez de "
      "acumular tudo em memória até `finished`. Envio de formulários *multipart* usa `QHttpMultiPart`; a "
      "partir do Qt 6.7, `QRestAccessManager` e `QNetworkRequestFactory` oferecem uma API de conveniência "
      "para serviços REST (ambas presentes no PyQt6 6.12; ver Anexo A)."),
    note("ATENÇÃO", "Não use `requests` ou `urllib` na thread da GUI: são bloqueantes. Se precisar dessas "
                    "bibliotecas, execute-as em um worker (Capítulo 20)."),

    h2("Sockets"),
    h3("TCP: QTcpSocket e QTcpServer"),
    p("TCP entrega um **fluxo** confiável e ordenado de bytes, mas não preserva fronteiras de mensagens: um "
      "`write()` pode chegar em vários `readyRead`, e vários `write()` podem chegar em um só. O protocolo da "
      "aplicação precisa definir o **enquadramento** — terminador de linha, prefixo de tamanho ou formato "
      "autodelimitado. A Listagem 21.2 enviou de propósito duas mensagens em um único `write()` e uma "
      "mensagem em dois pedaços; o enquadramento por linha remontou tudo corretamente."),
    lst("c21_tcp.py", "TCP com QTcpServer e QTcpSocket: protocolo de linhas e enquadramento"),
    out("c21_tcp"),
    h3("UDP: QUdpSocket"),
    p("UDP envia **datagramas** independentes, sem conexão, sem garantia de entrega nem de ordem, mas com "
      "fronteiras preservadas e baixa latência — adequado a telemetria periódica, descoberta na rede local e "
      "*broadcast*. O formato binário da listagem é definido com `struct` (tamanho fixo de 16 bytes)."),
    lst("c21_udp.py", "UDP com QUdpSocket e datagramas binários"),
    out("c21_udp"),
    h3("SSL/TLS: QSslSocket e QSslConfiguration"),
    p("`QSslSocket` acrescenta TLS a um socket TCP; `QSslServer` (Qt 6.4+) aceita conexões cifradas. O "
      "certificado do servidor e a chave privada entram na `QSslConfiguration`. No cliente, a verificação do "
      "par é obrigatória por padrão: um certificado autoassinado desconhecido gera `SelfSignedCertificate`, e "
      "um nome divergente do certificado gera `HostNameMismatch`. O certificado de exemplo foi gerado com:"),
    snip(["openssl req -x509 -newkey rsa:2048 -nodes -days 3650 \\",
          "    -keyout servidor.key -out servidor.crt \\",
          "    -subj \"/CN=localhost/O=Manual PyQt6 (exemplo)\" \\",
          "    -addext \"subjectAltName=DNS:localhost,IP:127.0.0.1\""], lang="text"),
    lst("c21_tls.py", "TLS com QSslServer e QSslSocket: verificação de certificado e de nome"),
    out("c21_tls"),
    note("ATENÇÃO", "Nunca chame `ignoreSslErrors()` sem argumentos em produção: isso desliga a proteção contra "
                    "ataques de intermediário. Para uma CA própria, adicione o certificado da CA com "
                    "`setCaCertificates()` — como na listagem — ou ignore apenas erros específicos e esperados."),

    h2("WebSockets: QWebSocket e QWebSocketServer"),
    p("WebSocket (RFC 6455) mantém um canal bidirecional sobre uma conexão HTTP, com mensagens de texto e "
      "binárias delimitadas — sem o problema de enquadramento do TCP. É o padrão para painéis de telemetria "
      "que recebem dados do servidor em tempo real. O modo `SecureMode` do servidor usa TLS (`wss://`)."),
    lst("c21_websocket.py", "WebSockets: servidor e cliente trocando JSON e dados binários"),
    out("c21_websocket"),

    h2("Autenticação OAuth com QtNetworkAuth"),
    p("O pacote **PyQt6-NetworkAuth** implementa OAuth 1.0 e 2.0. Para aplicações desktop, o fluxo indicado é "
      "o **Authorization Code com PKCE**: a aplicação abre o navegador na página de login do provedor, recebe "
      "o código de autorização em um endereço local (`QOAuthHttpServerReplyHandler`) e o troca por tokens. "
      "Na Listagem 21.6, um provedor mínimo local confere o PKCE e o \"navegador\" é simulado por uma "
      "requisição HTTP; em uma aplicação real, conecte `authorizeWithBrowser` a "
      "`QDesktopServices.openUrl`."),
    lst("c21_oauth.py", "OAuth 2.0 Authorization Code + PKCE com QOAuth2AuthorizationCodeFlow"),
    out("c21_oauth"),
    bl("O PKCE (S256) foi enviado automaticamente pelo fluxo, e o provedor validou o `code_verifier`.",
       "`setRequestedScopeTokens()` e `grantedScopeTokens()` são a API de escopos do Qt 6.9+; o `state` "
       "contra CSRF também é gerado e conferido pelo Qt.",
       "Guarde o *refresh token* em armazenamento seguro do sistema (por exemplo, com a biblioteca "
       "`keyring`), nunca em `QSettings` em texto puro.",
       "Para esquemas de URL próprios ou *app links*, o Qt 6.8+ oferece `QOAuthUriSchemeReplyHandler`."),

    h2("Objetos remotos: QtRemoteObjects"),
    p("O Qt Remote Objects publica um `QObject` (fonte) para outros processos ou máquinas, que o usam por meio "
      "de **réplicas**: propriedades sincronizadas, sinais repassados e slots invocados remotamente. O "
      "compilador `repc` gera código C++ a partir de arquivos `.rep`; em Python, usa-se a **réplica "
      "dinâmica** (`acquireDynamic`), cuja interface é descoberta em tempo de execução."),
    lst("c21_remoteobjects.py", "QtRemoteObjects: fonte e réplica dinâmica em processos distintos"),
    out("c21_remoteobjects"),
    p("A réplica só deve ser usada após `initialized`. A chamada de slot remoto é assíncrona: o efeito volta "
      "como mudança de propriedade (`pressaoChanged -> 0.0`). Endereços `local:` usam soquetes locais; "
      "`tcp://host:porta` atravessa a rede (sem cifragem: em redes não confiáveis, use um túnel TLS)."),

    h2("D-Bus: QtDBus"),
    p("D-Bus é o barramento de comunicação entre processos do Linux de desktop (serviços do sistema, "
      "notificações, gerenciadores de energia e rede). O módulo existe em todas as plataformas, mas só é útil "
      "onde há um daemon D-Bus em execução. A Listagem 21.8 exporta os slots de um objeto e os chama a partir "
      "de outro processo; o teste foi executado dentro de `dbus-run-session`."),
    lst("c21_dbus.py", "D-Bus: serviço exportado e cliente em outro processo"),
    out("c21_dbus"),

    h2("Portas seriais: QSerialPort e QSerialPortInfo"),
    p("Instrumentos de campo, CLPs, sensores e conversores RS-232/RS-485/USB continuam onipresentes na "
      "engenharia. `QSerialPort` é um `QIODevice` assíncrono: `readyRead` sinaliza dados, `canReadLine()`/"
      "`readLine()` resolvem protocolos de linha e `errorOccurred` informa desconexão do cabo ou falta de "
      "permissão. `QSerialPortInfo.availablePorts()` lista as portas físicas com descrição e identificadores "
      "USB (VID/PID)."),
    lst("c21_serial.py", "QSerialPort: aquisição de linhas ASCII de um instrumento"),
    out("c21_serial"),
    p("No teste, o instrumento foi simulado por um par de portas virtuais criado com `socat` "
      "(`PORTA_SERIAL` aponta uma das pontas); por isso a porta usada não aparece em `availablePorts()`, que "
      "lista apenas o hardware detectado (`ttyS0`). No Windows, use nomes como `COM3`; no Linux, o usuário "
      "precisa pertencer ao grupo `dialout` (ou equivalente) para abrir `/dev/ttyUSB0`."),
    note("ATENÇÃO", "No PyQt6 6.12, `setBaudRate()` recebe `int`: passar `QSerialPort.BaudRate.Baud115200` "
                    "gera `TypeError` (verificado). Use o número (`115200`) ou `.value` do enum."),
    img("Arquitetura de aquisição de dados via porta serial", "f21_1_serial.png", 15.5),

    h2("Bluetooth e NFC"),
    p("O **QtBluetooth** cobre Bluetooth clássico (RFCOMM) e **Low Energy** (BLE): descoberta "
      "(`QBluetoothDeviceDiscoveryAgent`), conexão a periféricos (`QLowEnergyController`), serviços e "
      "características GATT (`QLowEnergyService`, `QLowEnergyCharacteristic`) e, em algumas plataformas, papel "
      "de periférico. O **QtNfc** lê e grava etiquetas NFC (`QNearFieldManager`, `QNdefMessage`). Ambos "
      "dependem do sistema e do hardware — no Linux, o Bluetooth usa o BlueZ via D-Bus. O código deve tratar a "
      "ausência de adaptador, como na Listagem 21.10, executada em um ambiente sem Bluetooth e sem NFC."),
    lst("c21_bluetooth.py", "Bluetooth LE e NFC: descoberta com tratamento de ausência de hardware"),
    out("c21_bluetooth"),
    p("Com um periférico encontrado, o fluxo BLE típico é: `QLowEnergyController.createCentral(info)` → "
      "`connectToDevice()` → `discoverServices()` → `createServiceObject(uuid)` → `discoverDetails()` → "
      "leitura/escrita de características ou assinatura de notificações (`characteristicChanged`)."),
    snip("""controle = QLowEnergyController.createCentral(info)
controle.connected.connect(controle.discoverServices)
controle.discoveryFinished.connect(lambda: abrir_servico(controle))
controle.errorOccurred.connect(lambda e: print("BLE:", e.name))
controle.connectToDevice()"""),

    h2("Exercícios do capítulo"),
    nl("Acrescente à Listagem 21.1 um cliente com repetição automática (três tentativas com espera "
       "exponencial) para erros de timeout.",
       "Altere o protocolo da Listagem 21.2 para usar prefixo de tamanho (4 bytes, *big-endian*) em vez de "
       "terminador de linha.",
       "Implemente um painel que recebe telemetria por WebSocket e atualiza um gráfico (Capítulo 22).",
       "Na Listagem 21.9, mova a aquisição para uma `QThread` e entregue as amostras à GUI em lotes de 50.",
       "Escreva um cliente BLE que assine notificações de uma característica de temperatura e registre os "
       "valores em CSV."),
)

CAP22 = flat(
    ch("Visualização de dados e gráficos científicos", ST_AVA, [
        "Escolher a biblioteca de gráficos adequada a cada caso.",
        "Construir gráficos 2D e 3D com QtGraphs e QtCharts.",
        "Integrar Matplotlib e pyqtgraph com atualização em tempo real.",
    ]),
    h2("Panorama das opções de visualização"),
    tab("Comparativo das bibliotecas de visualização para PyQt6", ["Biblioteca", "Tipo", "Situação", "Indicação"],
        [["QtGraphs (PyQt6-Graphs)", "2D (QML) e 3D", "Ativo — sucessor indicado pela Qt",
          "Novos projetos com visual moderno e 3D acelerado por GPU"],
         ["QtCharts (PyQt6-Charts)", "2D (Graphics View)", "Obsoleto desde Qt 6.10",
          "Manutenção de código existente; gráficos de negócio simples"],
         ["QtDataVisualization", "3D", "Obsoleto desde Qt 6.10", "Apenas legado; migrar para QtGraphs"],
         ["Matplotlib (backend QtAgg)", "2D/3D, qualidade de publicação", "Biblioteca externa",
          "Relatórios, figuras técnicas, ampla variedade de gráficos"],
         ["pyqtgraph", "2D/3D, alto desempenho", "Biblioteca externa",
          "Tempo real, grandes volumes, osciloscópios e monitoramento"]],
        [2300, 1900, 2200, 2671]),
    p("A escolha depende de três fatores: **volume e taxa de atualização** dos dados, **qualidade gráfica** "
      "exigida (tela ou publicação) e **dependências** aceitáveis. A Listagem 22.7, no fim do capítulo, mede "
      "o custo por atualização das três abordagens mais usadas."),

    h2("QtGraphs"),
    p("O QtGraphs (Qt 6.8+) unifica os gráficos 2D e 3D da Qt sobre o Qt Quick e a camada de renderização "
      "RHI (Capítulo 25). Os gráficos 2D são declarados em QML (`GraphsView`); os 3D têm classes para Widgets "
      "no módulo `QtGraphsWidgets`. Ambos exigem aceleração gráfica: no ambiente de teste, as listagens "
      "rodaram sob X11 virtual (Xvfb) com OpenGL por software (Mesa llvmpipe); na plataforma `offscreen`, "
      "sem OpenGL, o 3D não é exibido."),
    h3("Gráficos 2D com GraphsView em QML (QQuickWidget)"),
    p("O gráfico é descrito em QML (Listagem 22.1) e embutido em uma aplicação Widgets com `QQuickWidget` "
      "(Capítulo 26). O Python localiza séries e eixos pelo `objectName` com `findChild()` e os manipula pelas "
      "classes do módulo `QtGraphs` (`QLineSeries`, `QScatterSeries`, `QValueAxis`)."),
    lst("c22_graphs2d.qml", "GraphsView em QML: tema, eixos, série de linha e de dispersão", lang="qml",
        nota="✔ Arquivo carregado e renderizado pela Listagem 22.2 (executada e verificada)."),
    lst("c22_graphs2d.py", "QtGraphs 2D alimentado pelo Python em um QQuickWidget"),
    out("c22_graphs2d"),
    img("Gráfico 2D do QtGraphs (GraphsView) em um QQuickWidget", "f22_1_graphs2d.png", 13.0),
    p("Use `replace()` para trocar todos os pontos de uma vez: ele emite um único sinal de atualização, "
      "enquanto `append()` em laço provoca uma atualização por ponto."),
    h3("Gráficos 3D: Q3DBarsWidgetItem, Q3DScatterWidgetItem e Q3DSurfaceWidgetItem"),
    p("Os itens 3D para Widgets não são widgets: são objetos que controlam uma cena QML dentro de um "
      "`QQuickWidget` informado com `setWidget()`. Barras (`Q3DBarsWidgetItem`), dispersão "
      "(`Q3DScatterWidgetItem`) e superfície (`Q3DSurfaceWidgetItem`) compartilham eixos, tema, câmera e "
      "seleção."),
    lst("c22_graphs3d.py", "Superfície 3D com Q3DSurfaceWidgetItem, gradiente de cores e câmera"),
    out("c22_graphs3d"),
    img("Superfície 3D do QtGraphs (Q3DSurfaceWidgetItem) com gradiente por valor", "f22_2_graphs3d.png", 13.0),
    note("ATENÇÃO", "No PyQt6 6.12, criar a série com `QSurface3DSeries(proxy)` não associou o proxy à série: "
                    "a superfície ficou vazia e o Qt avisou \"series needs to be created to access data "
                    "members\" (verificado). Use o proxy padrão, `serie.dataProxy()`, como na Listagem 22.3, "
                    "ou `setDataProxy()`."),
    h3("Séries, eixos, proxies de dados e temas (QGraphsTheme)"),
    bl("**Séries 2D**: `QLineSeries`, `QSplineSeries`, `QScatterSeries`, `QAreaSeries`, `QBarSeries`, "
       "`QPieSeries`; **3D**: `QBar3DSeries`, `QScatter3DSeries`, `QSurface3DSeries`.",
       "**Eixos**: `QValueAxis`, `QLogValueAxis`, `QDateTimeAxis`, `QBarCategoryAxis` (2D); `QValue3DAxis`, "
       "`QCategory3DAxis` (3D).",
       "**Proxies 3D** separam a fonte dos dados da série: `QBarDataProxy`, `QScatterDataProxy`, "
       "`QSurfaceDataProxy`, `QHeightMapSurfaceDataProxy` (superfície a partir de imagem) e os `QItemModel*` "
       "que leem diretamente de um modelo Model/View (Capítulo 14).",
       "**Tema**: `QGraphsTheme` define esquema claro/escuro, paleta de séries, grade e fontes, com temas "
       "prontos (`QGraphsTheme.Theme`)."),

    h2("QtCharts (legado)"),
    p("O QtCharts foi por muitos anos a solução de gráficos 2D da Qt e ainda está presente no PyQt6 6.12, mas "
      "é **obsoleto desde o Qt 6.10**: continua funcionando, sem novos recursos. Por ser baseado em Graphics "
      "View (Capítulo 18), funciona em qualquer plataforma, inclusive sem aceleração gráfica."),
    h3("QChart e QChartView"),
    p("`QChart` contém séries, eixos, legenda e título; `QChartView` é o widget que o exibe. Ative "
      "antialiasing com `setRenderHint()`."),
    lst("c22_qtcharts.py", "QtCharts: linha, spline, dispersão, eixo logarítmico, barras e pizza"),
    out("c22_qtcharts"),
    img("Painel com quatro gráficos QtCharts", "f22_3_qtcharts.png", 15.5),
    h3("Séries: linha, spline, dispersão, área, barras e pizza"),
    p("A listagem cobre os casos mais comuns. Dois detalhes evitam erros frequentes: a série precisa estar no "
      "gráfico (`addSeries`) **antes** de `attachAxis()`; e o percentual de uma fatia (`QPieSlice.percentage()`) "
      "só é definitivo depois que todas as fatias foram adicionadas — calculado durante a inserção, a primeira "
      "fatia apareceria com 100 % (erro encontrado e corrigido na elaboração deste exemplo)."),
    h3("Eixos: QValueAxis, QLogValueAxis, QDateTimeAxis, QCategoryAxis"),
    p("`QValueAxis` é linear; `QLogValueAxis` exige valores positivos e base definida; `QDateTimeAxis` recebe "
      "milissegundos desde a época (`QDateTime.toMSecsSinceEpoch()`); `QBarCategoryAxis` e `QCategoryAxis` "
      "rotulam categorias e faixas. O formato dos rótulos usa a sintaxe de `printf` (`setLabelFormat(\"%.0f\")`)."),
    h3("Migração de QtCharts para QtGraphs"),
    tab("Correspondência entre QtCharts / QtDataVisualization e QtGraphs",
        ["Legado", "QtGraphs (Qt 6.12)", "Observação"],
        [["QChart + QChartView (Widgets)", "GraphsView (QML) em QQuickWidget", "2D do QtGraphs é declarado em QML"],
         ["QLineSeries, QSplineSeries, QScatterSeries", "QLineSeries, QSplineSeries, QScatterSeries",
          "Mesmos nomes, módulo QtGraphs"],
         ["QBarSeries, QBarSet, QPieSeries, QPieSlice", "QBarSeries, QBarSet, QPieSeries, QPieSlice",
          "API semelhante"],
         ["QValueAxis, QLogValueAxis, QDateTimeAxis, QBarCategoryAxis", "Mesmos nomes", "Ver Anexo A.3.1"],
         ["QChart.setTheme / QChart.ChartTheme", "QGraphsTheme", "Tema unificado 2D/3D"],
         ["Q3DBars, Q3DScatter, Q3DSurface (QtDataVisualization)",
          "Q3DBarsWidgetItem, Q3DScatterWidgetItem, Q3DSurfaceWidgetItem", "Exigem QQuickWidget"],
         ["Q3DTheme", "QGraphsTheme", "—"],
         ["QBarDataProxy, QScatterDataProxy, QSurfaceDataProxy", "Mesmos nomes", "Proxies preservados"]],
        [3100, 3300, 2671], font=16),
    p("A correspondência foi conferida contra o catálogo de classes do Anexo A. A migração costuma ser direta "
      "para as séries e eixos; o trabalho principal está em substituir `QChartView` por um `GraphsView` em QML."),

    h2("QtDataVisualization (legado) e migração para QtGraphs"),
    p("O QtDataVisualization (gráficos 3D de barras, dispersão e superfície) também é obsoleto desde o Qt "
      "6.10. Seus conceitos — séries, proxies, eixos, câmera, tema e seleção — foram preservados no QtGraphs, "
      "como mostra a tabela anterior. A principal mudança arquitetural é que os gráficos deixaram de ser "
      "janelas (`QWindow`) e passaram a ser itens de cena hospedados em `QQuickWidget`."),

    h2("Matplotlib embutido: FigureCanvasQTAgg e NavigationToolbar2QT"),
    p("O Matplotlib traz um backend Qt (`matplotlib.backends.backend_qtagg`) que funciona com PyQt6. "
      "`FigureCanvasQTAgg` é um `QWidget` que exibe uma `Figure`; `NavigationToolbar2QT` acrescenta zoom, "
      "deslocamento, configuração de subgráficos e exportação. Crie a figura com `matplotlib.figure.Figure` — "
      "e não com `pyplot` —, para que o Matplotlib não abra janelas próprias nem mantenha referências globais."),
    lst("c22_matplotlib.py", "Matplotlib embutido com barra de navegação e redesenho por parâmetros"),
    out("c22_matplotlib"),
    img("Gráfico Matplotlib embutido em uma janela PyQt6", "f22_4_matplotlib.png", 15.0),
    p("O sobressinal calculado (52,7 % para ζ = 0,20) coincide com o valor teórico "
      "exp(−πζ/√(1−ζ²)). Para atualizações interativas, altere os dados dos artistas existentes "
      "(`set_data`) e use `draw_idle()`, que agrupa vários pedidos em um único redesenho."),

    h2("pyqtgraph para dados em tempo real"),
    p("O **pyqtgraph** é construído sobre Graphics View e NumPy e foi projetado para atualização rápida de "
      "grandes volumes. Os recursos-chave para tempo real são: `setData()` sobre o item existente, "
      "`setClipToView(True)` (desenha apenas o trecho visível) e `setDownsampling(auto=True, method=\"peak\")` "
      "(reduz pontos preservando picos — essencial em sinais de vibração)."),
    lst("c22_pyqtgraph.py", "pyqtgraph: osciloscópio com buffer circular e QTimer"),
    out("c22_pyqtgraph"),

    h2("Desempenho em atualização contínua"),
    lst("c22_desempenho.py", "Custo por quadro (dados + pintura) de pyqtgraph, QtCharts e Matplotlib"),
    out("c22_desempenho"),
    p("Os números são da máquina de teste, com renderização por software; o que importa é a ordem de "
      "grandeza. Com 20 000 pontos por quadro, o pyqtgraph sustentou centenas de quadros por segundo; o "
      "QtCharts ficou limitado pela conversão de 20 000 `QPointF` criados em Python; o Matplotlib, pelo "
      "redesenho completo da figura. Recomendações:"),
    bl("Atualize a tela a no máximo 30–60 Hz, mesmo que a aquisição seja mais rápida: acumule amostras e "
       "desenhe em lote em um `QTimer`.",
       "Mantenha os dados em arrays NumPy e evite laços Python por ponto.",
       "Reduza os pontos ao que a tela consegue mostrar (*downsampling*) — 20 000 pontos em 800 pixels de "
       "largura não acrescentam informação visual.",
       "No Matplotlib, para animação, use *blitting* (`canvas.copy_from_bbox`/`restore_region`) ou "
       "`matplotlib.animation`; para relatórios, desenhe uma vez.",
       "Ao medir desempenho de widgets baseados em Graphics View, force a pintura do **viewport**: `repaint()` "
       "na moldura não desenha a cena (armadilha encontrada na elaboração da Listagem 22.7)."),

    h2("Exercícios do capítulo"),
    nl("Converta o painel QtCharts da Listagem 22.4 para QtGraphs (2D em QML), mantendo os quatro gráficos.",
       "Acrescente ao gráfico da Listagem 22.2 uma `LineSeries` com o gradiente de pressão de poros e "
       "um eixo secundário em psi.",
       "Use `QItemModelSurfaceDataProxy` para exibir em 3D os dados de um `QStandardItemModel`.",
       "Implemente *blitting* no exemplo Matplotlib e meça o ganho com a técnica da Listagem 22.7.",
       "Integre a aquisição serial da Listagem 21.9 ao osciloscópio da Listagem 22.6."),
)
