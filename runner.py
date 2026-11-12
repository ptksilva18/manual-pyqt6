# -*- coding: utf-8 -*-
"""
Executa TODAS as listagens Python de data/listings/ em modo headless e grava a
saida padrao real em data/outputs/<nome>.txt (fonte unica dos blocos "Saida").

- QT_QPA_PLATFORM=offscreen (sem tela).
- Um "watchdog" substitui QApplication: a cada 100 ms fecha diálogos modais
  (simulando o usuário) e, após WATCHDOG_TICKS, fecha as janelas e encerra o
  event loop. Assim, programas interativos rodam do início ao fim.
- Falha = código de saída != 0, exceção, timeout ou mensagem "Traceback".

Opcoes por listagem (1a linha, comentario "# runner: ..."):
  ticks=N      encerra apos N x 100 ms (padrao 15)
  timeout=N    tempo maximo em segundos (padrao 60)
  xcb          executa com QT_QPA_PLATFORM=xcb sob Xvfb (OpenGL/RHI por Mesa llvmpipe)
  dbus         executa dentro de "dbus-run-session" (barramento de sessao privado)
  serial       cria um par de portas virtuais com socat; PORTA_SERIAL aponta uma ponta
               e um simulador de instrumento escreve linhas na outra
  env=K:V      define a variavel de ambiente K=V (pode repetir)

Uso: python runner.py [filtro]
"""
import glob
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from i18n import DATA_DIR, LANG  # noqa: E402  (MANUAL_LANG=en -> en/data)

LST = os.path.join(DATA_DIR, "listings")
OUT = os.path.join(DATA_DIR, "outputs")

HARNESS = r'''
import os, runpy, sys
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PyQt6 import QtCore, QtWidgets
TICKS = int(os.environ.get("WATCHDOG_TICKS", "15"))
_Orig = QtWidgets.QApplication

class QApplication(_Orig):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.__wd = QtCore.QTimer()
        self.__wd.setInterval(100)
        self.__n = 0
        self.__wd.timeout.connect(self.__tick)
        self.__wd.start()

    def __tick(self):
        self.__n += 1
        modal = _Orig.activeModalWidget()
        if modal is not None:
            modal.close()
        if self.__n >= TICKS:
            self.__wd.stop()
            _Orig.closeAllWindows()
            self.quit()

QtWidgets.QApplication = QApplication
path = sys.argv[1]
sys.argv = [path]
sys.path.insert(0, os.path.dirname(os.path.abspath(path)))   # como em "python script.py"
runpy.run_path(path, run_name="__main__")
'''


SIM_INSTRUMENTO = r"""
import sys, time
porta = sys.argv[1]
time.sleep(0.6)  # espera a aplicacao abrir a outra ponta
with open(porta, "w", buffering=1) as f:
    for i in range(12):
        f.write(f"$PT,{i},{100.0 + 2.5 * i:.2f},{25.0 + 0.1 * i:.2f}\r\n")
        time.sleep(0.05)
    time.sleep(1.0)
"""


def _opts(path):
    first = open(path, encoding="utf-8").readline()
    if "runner:" not in first:
        return {}
    toks = first.split("runner:", 1)[1].split()
    o = {"env": {}}
    for t in toks:
        if t.startswith("env="):
            k, v = t[4:].split(":", 1)
            o["env"][k] = v
        elif "=" in t:
            k, v = t.split("=", 1)
            o[k] = v
        else:
            o[t] = True
    return o


def _xvfb_vivo() -> bool:
    import socket
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        s.connect("/tmp/.X11-unix/X99")  # soquete órfão (servidor morto) recusa a conexão
        return True
    except OSError:
        return False
    finally:
        s.close()


def _ensure_xvfb():
    if _xvfb_vivo():
        return
    for resto in ("/tmp/.X11-unix/X99", "/tmp/.X99-lock"):
        if os.path.exists(resto):
            os.remove(resto)
    subprocess.Popen(["Xvfb", ":99", "-screen", "0", "1920x1200x24", "-nolisten", "tcp"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        if _xvfb_vivo():
            return
        time.sleep(0.1)
    raise RuntimeError("Xvfb nao iniciou")


TLS_DIR = os.path.join(LST, "resources", "tls")
TLS_NAME = "server" if LANG == "en" else "servidor"   # nome do certificado/chave por idioma
SERIAL_ENV = "SERIAL_PORT" if LANG == "en" else "PORTA_SERIAL"
TLS_ORG = "PyQt6 Manual (example)" if LANG == "en" else "Manual PyQt6 (exemplo)"


def _garantir_certificado_tls():
    """Gera o certificado autoassinado de TESTE da Listagem 21.4 (c21_tls.py), se faltar.

    A chave privada nao e versionada no repositorio; o comando e o mesmo mostrado no
    Capitulo 21. Nao use este certificado fora do exemplo.
    """
    crt = os.path.join(TLS_DIR, TLS_NAME + ".crt")
    key = os.path.join(TLS_DIR, TLS_NAME + ".key")
    if os.path.exists(crt) and os.path.exists(key):
        return
    os.makedirs(TLS_DIR, exist_ok=True)
    subprocess.run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "3650",
                    "-keyout", key, "-out", crt,
                    "-subj", f"/CN=localhost/O={TLS_ORG}",
                    "-addext", "subjectAltName=DNS:localhost,IP:127.0.0.1"],
                   check=True, capture_output=True)


def run_one(path):
    name = os.path.splitext(os.path.basename(path))[0]
    env = dict(os.environ, QT_QPA_PLATFORM="offscreen", PYTHONIOENCODING="utf-8",
               PYTHONHASHSEED="0", LANG="C.UTF-8")
    o = _opts(path)
    if "ticks" in o:
        env["WATCHDOG_TICKS"] = o["ticks"]
    env.update(o.get("env", {}))
    if o.get("xcb"):
        _ensure_xvfb()
        env.update(QT_QPA_PLATFORM="xcb", DISPLAY=":99")
    timeout = int(o.get("timeout", 60))
    procs = []
    with tempfile.TemporaryDirectory() as tmp:
        h = os.path.join(tmp, "_harness.py")
        open(h, "w", encoding="utf-8").write(HARNESS)
        if o.get("serial"):
            a, b = os.path.join(tmp, "ttyV0"), os.path.join(tmp, "ttyV1")
            procs.append(subprocess.Popen(["socat", f"pty,raw,echo=0,link={a}",
                                           f"pty,raw,echo=0,link={b}"]))
            for _ in range(50):
                if os.path.exists(a) and os.path.exists(b):
                    break
                time.sleep(0.1)
            env[SERIAL_ENV] = a
            sim = os.path.join(tmp, "_instrumento.py")
            open(sim, "w", encoding="utf-8").write(SIM_INSTRUMENTO)
            procs.append(subprocess.Popen([sys.executable, sim, b]))
        cmd = [sys.executable, h, path]
        if o.get("dbus"):
            cmd = ["dbus-run-session", "--"] + cmd
        try:
            p = subprocess.run(cmd, cwd=tmp, env=env, capture_output=True, text=True,
                               timeout=timeout)
        except subprocess.TimeoutExpired:
            return name, False, "TIMEOUT", ""
        finally:
            for pr in procs:
                pr.kill()
                pr.wait()
    ok = p.returncode == 0 and "Traceback" not in p.stderr and "Traceback" not in p.stdout
    open(os.path.join(OUT, name + ".txt"), "w", encoding="utf-8").write(p.stdout)
    return name, ok, f"rc={p.returncode}", p.stderr.strip()


def main():
    flt = sys.argv[1] if len(sys.argv) > 1 else ""
    files = sorted(f for f in glob.glob(os.path.join(LST, "*.py")) if flt in os.path.basename(f))
    if any(os.path.basename(f) == "c21_tls.py" for f in files):
        _garantir_certificado_tls()
    bad = 0
    for f in files:
        name, ok, rc, err = run_one(f)
        print(f"{'OK ' if ok else 'FALHA'} {name:40s} {rc}" + (f"\n    stderr: {err[:600]}" if (err and not ok) else ""))
        bad += not ok
    print(f"\n{len(files)} listagens, {bad} falhas")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
