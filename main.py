import sys
from PyQt5.QtWidgets import *
from CrawlingWorklist import crawlingworklist
from CrawlingCompguide import crawlingcompguide
import datetime
from PyQt5.QtCore import QThread, pyqtSignal

class Worker(QThread):
    update_progress = pyqtSignal(int, int)  # 진행 상태 신호 (현재 인덱스, 총 개수)
    finished = pyqtSignal()  # 작업 완료 신호

    def __init__(self, df):
        super().__init__()
        self.df = df

    def run(self):
        for index, row in self.df.iterrows():
            values = crawlingcompguide(row['GICODE'])
            self.df.at[index, ['시가총액', '유동자산', '총부채']] = values
            self.update_progress.emit(index + 1, len(self.df))  # 진행 상태 업데이트

        self.finished.emit()  # 작업 완료 신호

class myApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.pbar.setValue(0)
        self.label = QLabel('작업 준비 중 입니다..', self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.pbar)
        vbox.addStretch()
        self.setLayout(vbox)

        self.setWindowTitle('증권 데이터 수집')
        self.setGeometry(300, 300, 500, 300)
        self.show()

    def startcrawling(self):
        self.df = crawlingworklist()
        # self.df = self.df[0:10] # 테스트용 소스
        self.worker = Worker(self.df)  # Worker 스레드 생성
        self.worker.update_progress.connect(self.updateProgress)  # 진행 상태 업데이트 연결
        self.worker.finished.connect(self.crawlingFinished)  # 작업 완료 처리 연결
        self.worker.start()  # 스레드 시작

    def updateProgress(self, current, total):
        self.label.setText(f"총 {total}건의 작업 중 {current}번째 작업 중 입니다..")
        self.pbar.setValue(int(current / total * 100))

    def crawlingFinished(self):
        self.label.setText("작업 결과를 엑셀로 작성 중 입니다..")
        self.df = self.df[self.df['유동자산']!=0]

        self.df['유-총'] = self.df['유동자산']-self.df['총부채']
        self.df['시총x1.5배'] = self.df['시가총액']*1.5
        self.df['E-F>0'] = self.df['유-총'] - self.df['시총x1.5배']

        current_time = datetime.datetime.now().strftime('%Y.%m.%d_%H%M%S')

        filename = f'ncav_{current_time}.xlsx'
        self.df.to_excel(filename, columns=['기업명', '시가총액', '유동자산', '총부채', '유-총', '시총x1.5배', 'E-F>0'], index=False, engine='openpyxl')

        QMessageBox.information(self, '작업 완료', '작업이 완료되었습니다.')
        sys.exit()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = myApp()
    ex.startcrawling()
    sys.exit(app.exec_())