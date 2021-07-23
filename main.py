# -*- coding: utf-8 -*-

"""
py40 PyQt5 tutorial

This example shows an icon
in the titlebar of the window.

"""

import sys, os, re
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QVBoxLayout

import platform

HOSTS_CONF = {
    "127.0.0.1": ["aaa.com", "bb.com", "cc.com"],
    "127.0.0.2": ["aaaa.com", "cbb.com", "ccc.com"],
}


def HostFormat(row=""):
    row = re.sub(r"^\s+", "", row)
    row = re.sub(r"\s{2,}", " ", row)
    if row[0] == "#":
        return None
    confList = row.split(" ")
    return {confList[0]: confList[1:]}


OSTYPE_HOST_PATH = {
    "linux": "/etc/hosts",
    "darwin": "/etc/hosts",
    "windows": "C:\Windows\System32\drivers\etc\hosts",
}


class CopyHost:
    osType = None
    hostPATH = None

    def __init__(self):
        self.osType = platform.system().lower()
        assert self.osType in ["linux", "darwin", "windows"], f"不支持的{self.osType}系统"
        self.hostsPath = OSTYPE_HOST_PATH[self.osType]

    def _linux(self, clean=False):
        canSave = os.access(self.hostsPath, os.W_OK)
        assert canSave, f"{self.hostsPath} 没有写入权限 请切换root运行"
        oldConf = ""
        with open(self.hostsPath, "r") as f:
            oldConf = f.read()

        if clean:
            newConf = re.sub(r".+#WriteByItplus.cc\n", "", oldConf, re.S)
        else:
            newConf = oldConf
            for k, v in HOSTS_CONF.items():
                newConf += f"{k} {' '.join(v)} #WriteByItplus.cc\n"
        with open(self.hostsPath, "w") as f:
            f.write(newConf)

    def _darwin(self, clean=False):
        self._linux(clean)

    def _windows(self, clean=False):
        canSave = os.access("C:\Windows\System32\drivers\etc\hosts", os.W_OK)
        assert canSave, "没有写入权限 请关闭窗口右键管理员权限运行"
        oldConf = ""
        with open(self.hostsPath, "rt") as f:
            oldConf = f.read()

        newConf = re.sub(r".+#WriteByItplus.cc\n", "", oldConf, re.S)
        if not clean:
            newConf = newConf
            for k, v in HOSTS_CONF.items():
                newConf += f"{k} {' '.join(v)} #WriteByItplus.cc\n"
        with open(self.hostsPath, "wt") as f:
            f.write(newConf)

    def save(self, clean=False):
        do = getattr(self, f"_{self.osType}")
        do(clean)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()  # 界面绘制交给InitUi方法

    def initUI(self):
        # 设置窗口的位置和大小
        self.setGeometry(300, 300, 300, 220)
        # 设置窗口的标题
        # layout = QVBoxLayout()
        # layout.addWidget(QPushButton('Top'))
        # layout.addWidget(QPushButton('Bottom'))
        # self.setLayout(layout)

        btn1 = QPushButton("设置", self)
        btn1.move(30, 50)

        btn2 = QPushButton("还原", self)
        btn2.move(150, 50)

        btn1.clicked.connect(self.save)
        btn2.clicked.connect(self.clean)
        # 显示窗口
        self.statusBar()
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle("Host修改工具")
        self.show()

    def save(self):
        msg = ""
        try:
            CopyHost().save(False)
            msg = "操作成功！！！"
        except Exception as e:
            msg = str(e)
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + msg)

    def clean(self):
        msg = ""
        try:
            CopyHost().save(True)
            msg = "操作成功！！！"
        except Exception as e:
            msg = str(e)
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + msg)


if __name__ == "__main__":
    # 创建应用程序和对象
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
