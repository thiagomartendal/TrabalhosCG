# Thiago Martendal e Paulo Almeida

from janela import *
from objeto.objeto3D import *

Objeto3D('', [])

root = QApplication(sys.argv)
app = Janela()
app.show()
sys.exit(root.exec_())
