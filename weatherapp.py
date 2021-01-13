
import requests
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QComboBox


apikey = 'bf527f2c0ece63f0e185788e4ea21be3'
base = 'http://api.openweathermap.org/data/2.5'


app = QApplication([])
mainWindow = QWidget()
mainWindow.setWindowTitle('Weather App V1.0')
mainWindow.setWindowIcon(QIcon('calicon.jpg'))
Body = QVBoxLayout()
mainWindow.setLayout(Body)
labelwidget = QWidget()
inputwidget = QWidget()
labellayout = QHBoxLayout()
inputlayout = QHBoxLayout()
labelwidget.setLayout(labellayout)
inputwidget.setLayout(inputlayout)
Info = QLabel('Enter city name below:')
labellayout.addWidget(Info)
City = QTextEdit('City')
City.setMaximumHeight(40)
City.setMaximumWidth(120)
inputlayout.addWidget(City)
button = QPushButton('OK')
button.setStyleSheet('background-color: green; color: white')
button.setMaximumHeight(20)
button.setMaximumWidth(120)
result = QLabel('')
result1 = QLabel('')
result2 = QLabel('')
result3 = QLabel('')
Body.addWidget(labelwidget)
Body.addWidget(inputwidget)
Body.addWidget(button)
Body.addWidget(result)
Body.addWidget(result1)
Body.addWidget(result2)
Body.addWidget(result3)

def onpush():
    try:
        citydetails = City.toPlainText()
        url = f'{base}/weather?q={citydetails}&appid={apikey}'
        r = requests.get(url)
        name = r.json().get('name')
        weather = r.json().get('weather')
        coord = r.json().get('coord')
        main = r.json().get('main')
        result.setText(str(name))
        result1.setText(str(weather))
        result2.setText(str(coord))
        result3.setText(str(main))
        return True
    except Exception as e:
        result.setText("Oops, we coluldn't connect to the server at this time!")
        

button.clicked.connect(lambda: onpush())
mainWindow.show()
app.exec_()
