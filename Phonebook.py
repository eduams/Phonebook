from logging import root
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import json

class Node:
  def __init__(self,data):
    self.data = data
    self.left = None
    self.right = None
    self.height = 1

class Tree:
  def __init__(self):
    self.root = None

  def insert(self, data, node=None):
    if node == None:
      if self.root is None:
        self.root = Node(data)
        print("inseriu raiz", data)
        return
      #Esse código vai rodar uma função recursiva. Depois que essa função recursiva terminar de percorrer a árvore de baixo para cima, ela vai
      #receber o return da última "rodada" da recursividade dessa função e colocar no root da árvore
      else:
        node = self.root
        self.root = self.insert_recursive(data, node)

  def insert_recursive(self,data,node):
    if data < node.data:
        if node.left == None:
          #Não vai adicionar o elemento se já existir alguém com o mesmo nome
          if data[0] == node.data[0]:
            print("repetido")
          else:
            node.left = Node(data)
            print("inseriu ", data, " à esquerda de ", node.data)
        else:
          node_recursive = self.insert_recursive(data, node.left)
          node.left = node_recursive
    elif data > node.data:
        if node.right == None:
          #Não vai adicionar o elemento se já existir alguém com o mesmo nome
          if data[0] == node.data[0]:
            print("repetido")
          else:
            node.right = Node(data)
            print("inseriu ", data, " à direita de ", node.data)
        else:
          node_recursive = self.insert_recursive(data, node.right)
          node.right = node_recursive

    node.height = 1 + max(self.get_node_height(node.left), self.get_node_height(node.right))
    balance = self.get_balance(node)

    #Balanceamento: esse código vai ser responsável por checar o balanceamento da árvore de baixo para cima e fazer as rotações
    if balance > 1:
        print("Quem é a raiz da rotação: ",node.data)
        if self.get_balance(node.left) < 0:
          node.left = self.left_rotate(node.left)
        node = self.right_rotate(node)
        return node

    if balance < -1:
        print("Quem é a raiz da rotação: ",node.data)
        if self.get_balance(node.right) > 0:
          node.right = self.right_rotate(node.right)
        node = self.left_rotate(node)
        return node
    return node

  def delete(self, data, node=None):
    if node == None:
      if self.root is None:
        self.root = Node(data)
        print("inseriu raiz", data)
        return
      #Esse código vai rodar uma função recursiva. Depois que essa função recursiva terminar de percorrer a árvore de baixo para cima, ela vai
      #receber o return da última "rodada" da recursividade dessa função e colocar no root da árvore
      else:
        node = self.root
        self.root = self.delete_recursive(data, node)

  def delete_recursive(self,data,node):
    if not node:
        return node
    if data < node.data:
        node.left = self.delete_recursive(data, node.left)
    elif data > node.data:
        node.right = self.delete_recursive(data, node.right)
    else:
      if node.left is None:
        temp = node.right
        node = None
        return temp
      elif node.right is None:
        temp = node.left
        node = None
        return temp

        # Node with two children: Get the inorder successor (smallest
        # in the right subtree)
      temp = self.get_min_value_node(node.right)
      node.data = temp.data
      node.right = self.delete_recursive(temp.data, node.right)

        # If the tree had only one node then return
    if node is None:
      return node

    node.height = 1 + max(self.get_node_height(node.left), self.get_node_height(node.right))
    balance = self.get_balance(node)

    #Balanceamento: esse código vai ser responsável por checar o balanceamento da árvore de baixo para cima e fazer as rotações
    if balance > 1:
        print("Quem é a raiz da rotação: ",node.data)
        if self.get_balance(node.left) < 0:
          node.left = self.left_rotate(node.left)
        node = self.right_rotate(node)
        return node

    if balance < -1:
        print("Quem é a raiz da rotação: ",node.data)
        if self.get_balance(node.right) > 0:
          node.right = self.right_rotate(node.right)
        node = self.left_rotate(node)
        return node
    return node

  def print_tree(self, node=None):
        if node is None:
            node = self.root
        if node is not None:
            if node.left is not None:
                self.print_tree(node.left)
            balance = self.get_balance(node)
            left_value = 1 if node.left is not None else 0
            right_value = 1 if node.right is not None else 0
            print("Nó: ", node.data, "Altura do nó:", node.height, "Equlíbrio: ", balance)
            if node.right is not None:
                self.print_tree(node.right)

  def search(self, search_input, node=None):
    if node is None:
      node = self.root
    if node is None:
      return None
    if node.data[0] == search_input:
      return node
    elif search_input < node.data[0]:
      if node.left != None:
        return self.search(search_input, node.left)
      else:
        return None 
    else:
      if node.right != None:
        return self.search(search_input, node.right)
      else:
         return None

  def get_balance(self,node):
    if node is None:
      return 0
    return self.get_node_height(node.left) - self.get_node_height(node.right)

  def get_node_height(self,node):
    if node is None:
      return 0
    return node.height

  def left_rotate(self, A):
    B = A.right
    C = B.left
    B.left = A
    A.right = C

    A.height = 1 + max(self.get_node_height(A.left), self.get_node_height(A.right))
    B.height = 1 + max(self.get_node_height(B.left), self.get_node_height(B.right))

    return B


  def right_rotate(self, C):
    B = C.left
    A = B.right
    B.right = C
    C.left = A

    C.height = 1 + max(self.get_node_height(C.left), self.get_node_height(C.right))
    B.height = 1 + max(self.get_node_height(B.left), self.get_node_height(B.right))

    return B


  #converte a árvore em uma lista para poder ser colocada na tabela
  def return_tree_elements(self, node=None):
    elements = []
    if node is None:
        node = self.root
    if node is not None:
        elements.append(node.data)
        if node.left is not None:
            elements.extend(self.return_tree_elements(node.left))
        if node.right is not None:
            elements.extend(self.return_tree_elements(node.right))
    return elements

  #converte os inputs em uma lista para poder ser colocada em um json
  def list_json(self, node=None):
    tree = []
    if node is None:
        node = self.root
    if node is not None:
        tree.append(node.data)
        if node.left is not None:
            tree.extend(self.return_tree_elements(node.left))
        if node.right is not None:
            tree.extend(self.return_tree_elements(node.right))
    json_tree = json.dumps(tree)
    with open("data.json", "w") as outfile:
        outfile.write(json_tree)
    return tree


class Phonebook:
  def __init__(self):
    self.tree = Tree()

#popup
class Ui_Popup(object):
    def setupUi(self, Dialog, search_input):
        Dialog.setObjectName("Dialog")
        Dialog.resize(642, 285)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(450, 250, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lineEdit = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 601, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 110, 601, 41))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(20, 180, 601, 41))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 54, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 54, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 160, 61, 17))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton.setGeometry(QtCore.QRect(20, 250, 80, 25))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        print(search_input)
        self.lineEdit.setText(search_input.data[0])
        self.lineEdit_2.setText(search_input.data[1])
        self.lineEdit_3.setText(search_input.data[2])

        self.pushButton.clicked.connect(lambda: delete_entry(search_input.data))
        self.buttonBox.accepted.connect(lambda: edit_entry(search_input.data))

        def edit_entry(data):
          delete_entry(data)

          list = []
          list.append(self.lineEdit.text())
          list.append(self.lineEdit_2.text())
          list.append(self.lineEdit_3.text())
          tree.insert(list)
          tree.print_tree

        def delete_entry(data):
          tree.delete(data)
          Dialog.close()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Editar"))
        self.label.setText(_translate("Dialog", "Nome"))
        self.label_2.setText(_translate("Dialog", "Telefone"))
        self.label_3.setText(_translate("Dialog", "Descrição"))
        self.pushButton.setText(_translate("Dialog", "Deletar"))

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(827, 665)
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 801, 621))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(parent=self.verticalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.lineEdit_4 = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout_4.addWidget(self.lineEdit_4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineEdit_3 = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_3.addWidget(self.lineEdit_3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.tableWidget = QtWidgets.QTableWidget(parent=self.verticalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton_2.clicked.connect(self.add_to_tree)
        self.pushButton.clicked.connect(self.search)
        self.fill_table()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "PhonebookQT"))
        self.pushButton.setText(_translate("Dialog", "Buscar nome"))
        self.label_3.setText(_translate("Dialog", "Nome"))
        self.label.setText(_translate("Dialog", "Telefone"))
        self.label_2.setText(_translate("Dialog", "Descrição"))
        self.pushButton_2.setText(_translate("Dialog", "Adicionar à lista"))

    
    def search(self):
      search_input = self.lineEdit.text()
      if not search_input:
        self.popup("Campo de pesquisa vazio.")
        return
      if not tree.search(search_input):
         self.popup("Nenhum resultado.")
         return
      Dialog = QtWidgets.QDialog()
      ui = Ui_Popup()
      ui.setupUi(Dialog,tree.search(search_input))
      Dialog.exec_()
      self.fill_table()


    def add_to_tree(self):
      nome = self.lineEdit_4.text()
      telefone = self.lineEdit_2.text()
      descricao = self.lineEdit_3.text()
      if not nome or not telefone or not descricao:
         self.popup("Todos os campos são obrigatórios. Tente novamente.")
         return
      list = []
      list.append(nome)
      list.append(telefone)
      list.append(descricao)
      tree.insert(list)
      tree.print_tree()
      self.fill_table()
      tree.list_json()
    
    def popup(self, mensagem_erro):
      msg = QMessageBox()
      msg.setWindowTitle("Erro")
      msg.setText(mensagem_erro)
      msg.setIcon(QMessageBox.Warning)
      msg.setStandardButtons(QMessageBox.Ok)
      msg.exec_()

    def fill_table(self):
      self.tableWidget.clear()

      num_rows = len(tree.return_tree_elements())
      self.tableWidget.setRowCount(num_rows)

      num_columns = 3 
      self.tableWidget.setColumnCount(num_columns)

      elements = tree.return_tree_elements()
      for row, item in enumerate(elements):
        for col, value in enumerate(item):
          self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))

tree = Tree()

#carrega o json
try:
  print("Lendo o JSON")
  caminho_arquivo = 'data.json'
  with open(caminho_arquivo, 'r') as arquivo:
    list = json.load(arquivo)
  for element in list:
    tree.insert(element)
  tree.print_tree()
except:
  print("JSON não existe")

app = QtWidgets.QApplication(sys.argv)
Dialog = QtWidgets.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()
sys.exit(app.exec())