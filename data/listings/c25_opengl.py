# runner: ticks=40 xcb
"""QOpenGLWidget com OpenGL 4.1 Core: shaders, VBO, VAO, uniform e captura do
framebuffer."""

import array
import os
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QMatrix4x4, QSurfaceFormat
from PyQt6.QtOpenGL import (
    QOpenGLBuffer,
    QOpenGLShader,
    QOpenGLShaderProgram,
    QOpenGLVersionFunctionsFactory,
    QOpenGLVersionProfile,
    QOpenGLVertexArrayObject,
)
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QApplication

# O PyQt6 não exporta as constantes do OpenGL: valores da especificação (glcorearb.h).
GL_COLOR_BUFFER_BIT, GL_TRIANGLES, GL_FLOAT = 0x4000, 0x0004, 0x1406
GL_VERSION, GL_RENDERER, GL_SHADING_LANGUAGE_VERSION = 0x1F02, 0x1F01, 0x8B8C

VERT = """#version 410 core
layout(location = 0) in vec2 posicao;
layout(location = 1) in vec3 cor;
uniform mat4 mvp;
out vec3 v_cor;
void main() { v_cor = cor; gl_Position = mvp * vec4(posicao, 0.0, 1.0); }"""
FRAG = """#version 410 core
in vec3 v_cor;
out vec4 frag;
void main() { frag = vec4(v_cor, 1.0); }"""


class Triangulo(QOpenGLWidget):
    def __init__(self) -> None:
        super().__init__()
        self.angulo = 0.0

    def initializeGL(self) -> None:
        # O PyQt6 traz as tabelas de funções 2.0, 2.1 e 4.1 Core; peça uma delas
        # explicitamente (o driver pode entregar um contexto mais novo, compatível).
        perfil = QOpenGLVersionProfile()
        perfil.setVersion(4, 1)
        perfil.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
        self.gl = QOpenGLVersionFunctionsFactory.get(perfil, self.context())
        print(f"OpenGL {self.gl.glGetString(GL_VERSION)}")
        print(
            f"Renderer: {self.gl.glGetString(GL_RENDERER)}; GLSL "
            f"{self.gl.glGetString(GL_SHADING_LANGUAGE_VERSION)}"
        )
        self.prog = QOpenGLShaderProgram(self)
        for tipo, fonte in (
            (QOpenGLShader.ShaderTypeBit.Vertex, VERT),
            (QOpenGLShader.ShaderTypeBit.Fragment, FRAG),
        ):
            if not self.prog.addShaderFromSourceCode(tipo, fonte):
                raise RuntimeError(self.prog.log())
        if not self.prog.link():
            raise RuntimeError(self.prog.log())
        # x, y, r, g, b — intercalados em um único buffer
        dados = array.array(
            "f",
            [
                -0.8,
                -0.7,
                0.9,
                0.2,
                0.2,
                0.8,
                -0.7,
                0.2,
                0.7,
                0.2,
                0.0,
                0.8,
                0.2,
                0.4,
                0.9,
            ],
        )
        self.vao = QOpenGLVertexArrayObject(self)
        self.vao.create()
        self.vao.bind()  # o VAO memoriza o VBO e o layout dos atributos
        self.vbo = QOpenGLBuffer(QOpenGLBuffer.Type.VertexBuffer)
        self.vbo.create()
        self.vbo.bind()
        self.vbo.allocate(dados.tobytes(), len(dados) * dados.itemsize)
        passo = 5 * dados.itemsize
        self.prog.bind()
        self.prog.enableAttributeArray(0)
        self.prog.setAttributeBuffer(0, GL_FLOAT, 0, 2, passo)
        self.prog.enableAttributeArray(1)
        self.prog.setAttributeBuffer(1, GL_FLOAT, 2 * dados.itemsize, 3, passo)
        self.vao.release()
        self.gl.glClearColor(0.12, 0.18, 0.25, 1.0)

    def resizeGL(self, largura: int, altura: int) -> None:
        self.aspecto = largura / max(altura, 1)

    def paintGL(self) -> None:
        self.gl.glClear(GL_COLOR_BUFFER_BIT)
        mvp = QMatrix4x4()
        mvp.ortho(-self.aspecto, self.aspecto, -1.0, 1.0, -1.0, 1.0)
        mvp.rotate(self.angulo, 0.0, 0.0, 1.0)
        self.prog.bind()
        self.prog.setUniformValue("mvp", mvp)
        self.vao.bind()
        self.gl.glDrawArrays(GL_TRIANGLES, 0, 3)
        self.vao.release()

    def girar(self) -> None:
        self.angulo = (self.angulo + 15.0) % 360.0
        self.update()  # agenda paintGL(); nunca chame paintGL() diretamente


def main() -> int:
    fmt = QSurfaceFormat()
    fmt.setVersion(4, 1)
    fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    fmt.setSamples(4)  # antisserrilhamento (MSAA)
    QSurfaceFormat.setDefaultFormat(fmt)  # antes de criar a QApplication
    app = QApplication(sys.argv)
    w = Triangulo()
    w.resize(480, 360)
    w.show()
    timer = QTimer()
    timer.timeout.connect(w.girar)
    timer.start(50)

    def fim() -> None:
        timer.stop()
        img = w.grabFramebuffer()  # renderiza e lê o framebuffer como QImage
        f = w.format()
        print(
            f"Contexto obtido: {f.majorVersion()}.{f.minorVersion()} {f.profile().name}, "
            f"amostras={f.samples()}; ângulo final = {w.angulo:.0f}°"
        )
        fundo, centro = (
            img.pixelColor(5, 5).name(),
            img.pixelColor(img.width() // 2, img.height() // 2).name(),
        )
        print(
            f"Framebuffer {img.width()}x{img.height()}: fundo {fundo}, centro {centro}"
        )
        if os.environ.get("CAPTURA"):
            img.save(os.environ["CAPTURA"])
        app.quit()

    QTimer.singleShot(1000, fim)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
