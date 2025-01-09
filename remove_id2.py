from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QListWidget, QLabel)
from PySide6.QtCore import Qt
import sys

class UserComparisonTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("사용자 목록 비교 도구")
        self.setMinimumSize(800, 600)
        
        # 메인 위젯과 레이아웃 설정
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # 상단 버튼 레이아웃
        button_layout = QHBoxLayout()
        self.load_button = QPushButton("파일 읽어오기")
        self.remove_button = QPushButton("중복 항목 제거")
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.remove_button)
        main_layout.addLayout(button_layout)
        
        # 리스트와 레이블을 담을 컨테이너 레이아웃
        lists_layout = QHBoxLayout()
        
        # 팔로워 컨테이너
        a_container = QVBoxLayout()
        self.a_label = QLabel("팔로워: 0개 항목")
        self.a_list = QListWidget()
        a_container.addWidget(self.a_label)
        a_container.addWidget(self.a_list)
        
        # 팔로잉 컨테이너
        b_container = QVBoxLayout()
        self.b_label = QLabel("팔로잉: 0개 항목")
        self.b_list = QListWidget()
        b_container.addWidget(self.b_label)
        b_container.addWidget(self.b_list)
        
        # 컨테이너들을 메인 레이아웃에 추가
        lists_layout.addLayout(a_container)
        lists_layout.addLayout(b_container)
        main_layout.addLayout(lists_layout)
        
        # 하단 버튼 레이아웃 추가
        bottom_button_layout = QHBoxLayout()
        self.save_b_list_button = QPushButton("뒷삭리스트 저장")
        self.save_b_list_button.setFixedHeight(40)  # 버튼 높이 설정
        bottom_button_layout.addWidget(self.save_b_list_button)
        main_layout.addLayout(bottom_button_layout)
        
        # 버튼 이벤트 연결
        self.load_button.clicked.connect(self.load_files)
        self.remove_button.clicked.connect(self.remove_duplicates)
        self.save_b_list_button.clicked.connect(self.save_b_list)
        
        # 데이터 저장용 변수
        self.a_data = []  # [(id, name), ...]
        self.b_data = []  # [(id, name), ...]
    
    def load_files(self):
        """파일에서 데이터를 읽어오는 함수"""
        try:
            # 팔로워 읽기
            with open('팔로워.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                self.a_data = []
                for i in range(0, len(lines), 2):
                    if i + 1 < len(lines):
                        user_id = lines[i].strip()
                        user_name = lines[i + 1].strip()
                        self.a_data.append((user_id, user_name))
            
            # B 파일 읽기
            with open('팔로잉.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                self.b_data = []
                for i in range(0, len(lines), 2):
                    if i + 1 < len(lines):
                        user_id = lines[i].strip()
                        user_name = lines[i + 1].strip()
                        self.b_data.append((user_id, user_name))
            
            # 리스트 위젯 업데이트
            self.update_list_widgets()
            
        except Exception as e:
            self.a_label.setText(f"팔로워 읽기 오류: {str(e)}")
            self.b_label.setText(f"팔로잉 읽기 오류: {str(e)}")
    
    def update_list_widgets(self):
        """리스트 위젯과 레이블 업데이트"""
        # A 리스트 업데이트
        self.a_list.clear()
        for user_id, user_name in self.a_data:
            self.a_list.addItem(f"{user_id} - {user_name}")
        self.a_label.setText(f"팔로워: {len(self.a_data)}개 항목")
        
        # B 리스트 업데이트
        self.b_list.clear()
        for user_id, user_name in self.b_data:
            self.b_list.addItem(f"{user_id} - {user_name}")
        self.b_label.setText(f"팔로잉: {len(self.b_data)}개 항목")
    
    def remove_duplicates(self):
        """양쪽 리스트에서 중복되는 항목 제거"""
        # 중복 항목 찾기
        a_set = set((user_id, user_name) for user_id, user_name in self.a_data)
        b_set = set((user_id, user_name) for user_id, user_name in self.b_data)
        
        # 중복되지 않는 항목만 남기기
        duplicates = a_set.intersection(b_set)
        self.a_data = list(a_set - duplicates)
        self.b_data = list(b_set - duplicates)
        
        # 리스트 위젯 업데이트
        self.update_list_widgets()
    
    def save_b_list(self):
        """B 리스트를 텍스트 파일로 저장"""
        try:
            with open('뒷삭리스트.txt', 'w', encoding='utf-8') as file:
                for user_id, user_name in self.b_data:
                    file.write(f"{user_id} : {user_name}\n")
            self.b_label.setText(f"팔로잉: {len(self.b_data)}개 항목 (저장 완료)")
        except Exception as e:
            self.b_label.setText(f"뒷삭리스트 저장 오류: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = UserComparisonTool()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()