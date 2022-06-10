# _*_coding: UTF-8_*_
# 开发作者 ：TXH
# 开发时间 ：2020/9/14 1:44
# 文件名称 ：pyqtbar.py
# 开发工具 ：Python 3.7+ Pycharm IDE


from PyQt5 import QtWidgets, QtCore
import sys
from PyQt5.QtCore import *
import time


class Runthread(QThread):
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(int, int, int)

    def __init__(self):
        super(Runthread, self).__init__()

    def run(self):
        task_number = 0
        total_task_number = 9
        for i in range(100):
            ##########################
            #                        #
            # 将需要计算的代码块放在此处#
            #                        #
            ##########################

            time.sleep(0.1)
            self._signal.emit(i + 1, task_number, total_task_number)  # 发送实时任务进度和总任务进度


class ProcessBar(QtWidgets.QWidget):

    def __init__(self, work):
        super().__init__()
        self.work = work
        self.run_work()

    def run_work(self):
        # 创建线程
        # 连接信号
        self.work._signal.connect(self.call_backlog)  # 进程连接回传到GUI的事件
        # 开始线程
        self.work.start()

        # 进度条设置
        self.pbar = QtWidgets.QProgressBar(self)
        self.pbar.setMinimum(0)  # 设置进度条最小值
        self.pbar.setMaximum(100)  # 设置进度条最大值
        self.pbar.setValue(0)  # 进度条初始值为0
        self.pbar.setGeometry(QRect(1, 3, 499, 28))  # 设置进度条在 QDialog 中的位置 [左，上，右，下]

        # 窗口初始化
        self.setGeometry(300, 300, 500, 32)
        self.setWindowTitle('正在处理中')
        self.show()
        # self.work = None  # 初始化线程

    def call_backlog(self, msg, task_number, total_task_number):
        if task_number == 0 and total_task_number == 0:
            self.setWindowTitle(self.tr('正在处理中'))
        else:
            label = "正在处理：" + "第" + str(task_number) + "/" + str(total_task_number) + '个任务'
            self.setWindowTitle(self.tr(label))  # 顶部的标题
        self.pbar.setValue(int(msg))  # 将线程的参数传入进度条


class pyqtbar():
    def __init__(self, work):
        self.app = QtWidgets.QApplication(sys.argv)
        self.myshow = ProcessBar(work)
        self.myshow.show()
        sys.exit(self.app.exec_())



if __name__ == "__main__":
    # 继承QThread
    work = Runthread()
    bar = pyqtbar(work)
