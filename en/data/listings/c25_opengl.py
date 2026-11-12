# runner: ticks=40 xcb
"""QOpenGLWidget with OpenGL 4.1 Core: shaders, VBO, VAO, uniform and framebuffer
capture."""

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

# PyQt6 does not export the OpenGL constants: values from the specification (glcorearb.h).
GL_COLOR_BUFFER_BIT, GL_TRIANGLES, GL_FLOAT = 0x4000, 0x0004, 0x1406
GL_VERSION, GL_RENDERER, GL_SHADING_LANGUAGE_VERSION = 0x1F02, 0x1F01, 0x8B8C

VERT = """#version 410 core
layout(location = 0) in vec2 position;
layout(location = 1) in vec3 color;
uniform mat4 mvp;
out vec3 v_color;
void main() { v_color = color; gl_Position = mvp * vec4(position, 0.0, 1.0); }"""
FRAG = """#version 410 core
in vec3 v_color;
out vec4 frag;
void main() { frag = vec4(v_color, 1.0); }"""


class Triangle(QOpenGLWidget):
    def __init__(self) -> None:
        super().__init__()
        self.angle = 0.0

    def initializeGL(self) -> None:
        # PyQt6 ships the 2.0, 2.1 and 4.1 Core function tables; request one of them
        # explicitly (the driver may deliver a newer, compatible context).
        profile = QOpenGLVersionProfile()
        profile.setVersion(4, 1)
        profile.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
        self.gl = QOpenGLVersionFunctionsFactory.get(profile, self.context())
        print(f"OpenGL {self.gl.glGetString(GL_VERSION)}")
        print(
            f"Renderer: {self.gl.glGetString(GL_RENDERER)}; GLSL "
            f"{self.gl.glGetString(GL_SHADING_LANGUAGE_VERSION)}"
        )
        self.prog = QOpenGLShaderProgram(self)
        for kind, source in (
            (QOpenGLShader.ShaderTypeBit.Vertex, VERT),
            (QOpenGLShader.ShaderTypeBit.Fragment, FRAG),
        ):
            if not self.prog.addShaderFromSourceCode(kind, source):
                raise RuntimeError(self.prog.log())
        if not self.prog.link():
            raise RuntimeError(self.prog.log())
        # x, y, r, g, b — interleaved in a single buffer
        data = array.array(
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
        self.vao.bind()  # the VAO remembers the VBO and the attribute layout
        self.vbo = QOpenGLBuffer(QOpenGLBuffer.Type.VertexBuffer)
        self.vbo.create()
        self.vbo.bind()
        self.vbo.allocate(data.tobytes(), len(data) * data.itemsize)
        stride = 5 * data.itemsize
        self.prog.bind()
        self.prog.enableAttributeArray(0)
        self.prog.setAttributeBuffer(0, GL_FLOAT, 0, 2, stride)
        self.prog.enableAttributeArray(1)
        self.prog.setAttributeBuffer(1, GL_FLOAT, 2 * data.itemsize, 3, stride)
        self.vao.release()
        self.gl.glClearColor(0.12, 0.18, 0.25, 1.0)

    def resizeGL(self, width: int, height: int) -> None:
        self.aspect = width / max(height, 1)

    def paintGL(self) -> None:
        self.gl.glClear(GL_COLOR_BUFFER_BIT)
        mvp = QMatrix4x4()
        mvp.ortho(-self.aspect, self.aspect, -1.0, 1.0, -1.0, 1.0)
        mvp.rotate(self.angle, 0.0, 0.0, 1.0)
        self.prog.bind()
        self.prog.setUniformValue("mvp", mvp)
        self.vao.bind()
        self.gl.glDrawArrays(GL_TRIANGLES, 0, 3)
        self.vao.release()

    def rotate(self) -> None:
        self.angle = (self.angle + 15.0) % 360.0
        self.update()  # schedules paintGL(); never call paintGL() directly


def main() -> int:
    fmt = QSurfaceFormat()
    fmt.setVersion(4, 1)
    fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    fmt.setSamples(4)  # antialiasing (MSAA)
    QSurfaceFormat.setDefaultFormat(fmt)  # before creating the QApplication
    app = QApplication(sys.argv)
    w = Triangle()
    w.resize(480, 360)
    w.show()
    timer = QTimer()
    timer.timeout.connect(w.rotate)
    timer.start(50)

    def finish() -> None:
        timer.stop()
        img = w.grabFramebuffer()  # renders and reads the framebuffer as a QImage
        f = w.format()
        print(
            f"Context: {f.majorVersion()}.{f.minorVersion()} {f.profile().name}, "
            f"samples={f.samples()}; final angle = {w.angle:.0f}°"
        )
        background, center = (
            img.pixelColor(5, 5).name(),
            img.pixelColor(img.width() // 2, img.height() // 2).name(),
        )
        print(
            f"Framebuffer {img.width()}x{img.height()}: background {background}, "
            f"center {center}"
        )
        if os.environ.get("CAPTURE"):
            img.save(os.environ["CAPTURE"])
        app.quit()

    QTimer.singleShot(1000, finish)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
