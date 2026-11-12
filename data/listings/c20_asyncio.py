# runner: ticks=150
"""asyncio sobre o event loop do Qt com a biblioteca de terceiros qasync."""

import asyncio
import sys
import time

import qasync
from PyQt6.QtWidgets import QApplication, QLabel


async def consultar_sensor(nome: str, atraso: float) -> tuple[str, float]:
    await asyncio.sleep(atraso)  # simula E/S de rede sem bloquear a interface
    return nome, 100.0 + atraso * 10


def calculo_bloqueante(n: int) -> int:
    return sum(i * i for i in range(n))


async def principal(rotulo: QLabel) -> None:
    t0 = time.perf_counter()
    leituras = await asyncio.gather(
        consultar_sensor("PT-101", 0.30),
        consultar_sensor("PT-102", 0.20),
        consultar_sensor("TT-201", 0.10),
    )
    dt = time.perf_counter() - t0
    print(f"3 consultas concorrentes em {dt:.2f} s (sequencial levaria 0.60 s)")
    for nome, valor in leituras:
        print(f"  {nome}: {valor:.1f}")
    rotulo.setText(" | ".join(f"{n}={v:.1f}" for n, v in leituras))

    resultado = await asyncio.to_thread(calculo_bloqueante, 2_000_000)  # fora do loop
    print(f"to_thread: soma dos quadrados = {resultado}")

    try:
        await asyncio.wait_for(consultar_sensor("PT-999", 5.0), timeout=0.2)
    except TimeoutError:
        print("wait_for: consulta a PT-999 excedeu 0.2 s e foi cancelada")
    print(f"Rótulo da janela: {rotulo.text()!r}")


def main() -> int:
    app = QApplication(sys.argv)
    rotulo = QLabel("aguardando...")
    rotulo.show()
    loop = qasync.QEventLoop(app)  # um único loop: eventos Qt + corrotinas asyncio
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_until_complete(principal(rotulo))
    return 0


if __name__ == "__main__":
    sys.exit(main())
