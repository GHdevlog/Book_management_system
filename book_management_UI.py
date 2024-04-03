import sys
from PyQt5.QtWidgets  import QApplication, QWidget, QVBoxLayout, QTabWidget, QLabel, \
QLineEdit, QPushButton, QHBoxLayout, QTextEdit, QComboBox, QTableWidget, QTableWidgetItem,\
QHeaderView, QDialog, QAbstractItemView, QMessageBox

from PyQt5.QtCore import Qt

def generate_books():
    from random import randrange, choice
    books = []
    for i in range(1, 21):
        # 도서명, 저자, 출판사, 출판년도, 도서번호
        book = [
            i,
            f"도서 {i}",
            f"저자 {i}",
            f"출판사 {randrange(1,6)}",
            str(2000 + randrange(10,20)),
            choice(("대출중","대출가능"))
        ]
        books.append(book)
    return books

def generate_users():
    from random import randrange
    users = []
    for i in range(1, 11):
        max_loan = randrange(5,11)
        # 회원 ID, 이용자명, 연락처, 대출가능 도서 수, 대출중인 도서 수
        user = [
            f"{i}",
            f"이용자 {i}",
            f"010-{randrange(1000,10000)}-{randrange(1000,10000)}",
            max_loan,
            randrange(0,max_loan+1)
        ]
        users.append(user)
    return users

def generate_loans():
    from random import randrange
    users = []
    for i in range(1, 11):
        # 대출 번호 
        user = [
            f"이용자 {i}",
            f"{i}",
            f"010-{randrange(1000,10000)}-{randrange(1000,10000)}",
            randrange(5,11),
            randrange(0,6)
        ]
        users.append(user)
    return users

class LibraryWindow(QWidget):

    book_dummy_data = generate_books()
    user_dummy_data = generate_users()
    
    book_labels = ["도서번호","도서명", "저자", "출판사", "출판년도" ,"대출 상태"]
    user_labels = ["회원 ID", "이용자명", "연락처", "대출가능 도서 수", "대출중인 도서 수"]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("도서관 관리 시스템")
        self.setGeometry(600, 600, 1600, 1200)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        tab_widget = QTabWidget()

        book_tab = QWidget()
        user_tab = QWidget()
        loan_tab = QWidget()

        self.setup_book_tab(book_tab)
        self.setup_user_tab(user_tab)
        self.setup_loan_tab(loan_tab)

        tab_widget.addTab(book_tab, "도서 관리")
        tab_widget.addTab(user_tab, "회원 관리")
        tab_widget.addTab(loan_tab, "대출 관리")

        layout.addWidget(tab_widget)
        self.setLayout(layout)

    def setup_book_tab(self, tab):
        layout = QVBoxLayout()

        # 수평 레이아웃을 생성하여 검색할 항목, 검색어 및 검색 버튼을 같은 줄에 배치
        search_layout = QHBoxLayout()

        # 검색할 항목을 선택할 콤보 박스
        search_by_label = QLabel("검색할 항목:")
        self.search_by_combo = QComboBox()
        self.search_by_combo.addItems(["도서명", "저자", "출판사","출판년도"])

        # 입력 필드
        search_label = QLabel("검색어:")
        self.search_edit = QLineEdit()
        self.search_edit.returnPressed.connect(lambda : self.search_data(what_searching_for='book'))

        # 검색 버튼
        search_button = QPushButton("검색")
        search_button.clicked.connect(lambda : self.search_data(what_searching_for='book'))

        search_layout.addWidget(search_by_label)
        search_layout.addWidget(self.search_by_combo)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(search_button)

        # ---------------------------------------
        manage_layout = QHBoxLayout()

        add_book_button = QPushButton("도서 추가")
        add_book_button.clicked.connect(self.show_add_book_dialog)
        modify_book_button = QPushButton("도서 수정")  # 수정 버튼 추가
        modify_book_button.clicked.connect(self.modify_data)  # 수정 버튼에 대한 이벤트 핸들러 연결
        delete_book_button = QPushButton("도서 삭제")
        delete_book_button.clicked.connect(lambda : self.delete_data(what_deleting_for='book'))
        loan_book_button = QPushButton("도서 대출")
        loan_book_button.clicked.connect(self.loan_book)
        

        manage_layout.addWidget(add_book_button)
        manage_layout.addWidget(modify_book_button)
        manage_layout.addWidget(delete_book_button)
        manage_layout.addWidget(loan_book_button)

        #-----------------------------------------
        # 검색 결과를 표로 표시하기 위한 테이블 위젯
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(len(self.book_labels)+1)  # 도서명, 저자, 출판사, 출판년도, 도서번호 + 1
        self.result_table.setHorizontalHeaderLabels([""] + self.book_labels)
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_table.setSortingEnabled(True)  # 정렬 기능 활성화

        # 테이블 편집 비활성화
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout.addLayout(search_layout)
        layout.addLayout(manage_layout)
        layout.addWidget(self.result_table)

        tab.setLayout(layout)

    def add_checkbox_to_row(self, row_index, table):
        checkbox_item = QTableWidgetItem()
        checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)  # 사용자가 체크 가능하도록 설정
        checkbox_item.setCheckState(Qt.Unchecked)  # 기본적으로 체크 안된 상태로 설정
        table.setItem(row_index, 0, checkbox_item)  # 체크박스를 첫 번째 열에 추가

    def setup_user_tab(self, tab):
        layout = QVBoxLayout()

        # 수평 레이아웃을 생성하여 검색할 항목, 검색어 및 검색 버튼을 같은 줄에 배치
        user_layout = QHBoxLayout()

        # 검색할 항목을 선택할 콤보 박스
        search_by_label = QLabel("검색할 항목:")
        self.search_by_combo = QComboBox()
        self.search_by_combo.addItems(["이용자명", "회원 ID", "연락처"])
        # 입력 필드
        search_label = QLabel("검색어:")
        self.search_edit = QLineEdit()
        # self.search_edit.returnPressed.connect(self.search_user)
        self.search_edit.returnPressed.connect(lambda : self.search_data(what_searching_for='user'))

        # 검색 버튼
        search_button = QPushButton("검색")
        search_button.clicked.connect(lambda : self.search_data(what_searching_for='user'))

        user_layout.addWidget(search_by_label)
        user_layout.addWidget(self.search_by_combo)
        user_layout.addWidget(search_label)
        user_layout.addWidget(self.search_edit)
        user_layout.addWidget(search_button)

        # ---------------------------------------
        user_manage_layout = QHBoxLayout()

        add_book_button = QPushButton("회원 추가")
        add_book_button.clicked.connect(self.show_add_book_dialog)
        delete_book_button = QPushButton("회원 삭제")
        delete_book_button.clicked.connect(lambda : self.delete_data(what_deleting_for='user'))
        loan_book_button = QPushButton("대출 하기")
        loan_book_button.clicked.connect(self.loan_book)

        user_manage_layout.addWidget(add_book_button)
        user_manage_layout.addWidget(delete_book_button)
        user_manage_layout.addWidget(loan_book_button)

        #-----------------------------------------
        # 검색 결과를 표로 표시하기 위한 테이블 위젯
        self.user_result_table = QTableWidget()
        self.user_result_table.setColumnCount(len(self.user_labels)+1)  # 도서명, 저자, 출판사, 출판년도, 도서번호 + 1
        self.user_result_table.setHorizontalHeaderLabels([""] + self.user_labels)
        self.user_result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.user_result_table.setSortingEnabled(True)  # 정렬 기능 활성화

        # 테이블 편집 비활성화
        self.user_result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout.addLayout(user_layout)
        layout.addLayout(user_manage_layout)
        layout.addWidget(self.user_result_table)

        tab.setLayout(layout)

    def setup_loan_tab(self, tab):
        layout = QVBoxLayout()
        loan_label = QLabel("회원 이름:")
        self.loan_edit = QLineEdit()
        loan_button = QPushButton("대출 정보 검색")
        loan_button.clicked.connect(self.search_loan)
        self.loan_result = QTextEdit()

        layout.addWidget(loan_label)
        layout.addWidget(self.loan_edit)
        layout.addWidget(loan_button)
        layout.addWidget(self.loan_result)
        tab.setLayout(layout)

    def show_add_book_dialog(self):
        dialog = BookAddDialog()
        if dialog.exec_():
            book_info = dialog.get_book_info()
            self.book_dummy_data.append(book_info)
            # 여기서 도서 정보를 가져와서 도서 목록에 추가하는 작업을 수행합니다.
            # book_info 변수에는 ["도서명", "저자", "출판사", "출판년도", "도서번호"] 순서로 도서 정보가 들어 있습니다.
    def search_data(self, what_searching_for:str):
    # Determine whether it's a book search or user search
        if what_searching_for == 'book':
            result_table = self.result_table
            data = self.book_dummy_data
            labels = self.book_labels
        elif what_searching_for == 'user':
            result_table = self.user_result_table
            data = self.user_dummy_data
            labels = self.user_labels

        # Get the search criteria
        search_by = self.search_by_combo.currentText()
        search_keyword = self.search_edit.text()
        if search_by == "도서번호" or search_by == "대출가능 도서 수" or search_by == "대출중인 도서 수":
            search_keyword = int(search_keyword)

        # Clear the existing table content
        result_table.setRowCount(len(data))

        search_result_row = []

        # Iterate over the data to find matches
        for row_index, row_data in enumerate(data):
            self.add_checkbox_to_row(row_index, result_table)
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                if isinstance(col_data, int) and col_index in (3, 4):
                    item.setData(Qt.DisplayRole, int(col_data))
                result_table.setItem(row_index, col_index + 1, item) 

    def modify_data(self):
        selected_rows = []
        for row_index in range(self.result_table.rowCount()):
            checkbox_item = self.result_table.item(row_index, 0)
            if checkbox_item.checkState() == Qt.Checked:
                selected_rows.append(row_index)

        # 선택된 항목이 없을 경우 메시지 표시 후 종료
        if not selected_rows:
            QMessageBox.information(self, "알림", "수정할 항목을 선택하세요.")
            return

        # 선택된 행이 여러 개인 경우 메시지 표시 후 종료
        if len(selected_rows) > 1:
            QMessageBox.information(self, "알림", "한 번에 하나의 항목만 수정할 수 있습니다.")
            return

        # 선택된 행의 인덱스
        row_index = selected_rows[0]

        # 편집 모드로 변경하여 셀을 편집 가능하게 함
        for col_index in range(1, self.result_table.columnCount()):
            self.result_table.item(row_index, col_index).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)

        # 저장 버튼 생성 및 연결
        save_button = QPushButton("저장")
        save_button.clicked.connect(lambda: self.save_book_changes(row_index))
        self.result_table.setCellWidget(row_index, self.result_table.columnCount(), save_button)
        
        # 셀이 편집될 때마다 데이터를 업데이트하는 함수를 연결
        self.result_table.cellChanged.connect(self.update_book_info)

    def update_book_info(self, row, column):
        # 수정된 셀의 행과 열 인덱스를 가져옴
        edited_item = self.result_table.item(row, column)
        edited_text = edited_item.text()

        # 수정된 내용을 데이터에 반영
        if column == 1:
            self.book_dummy_data[row][0] = edited_text
        elif column == 2:
            self.book_dummy_data[row][1] = edited_text
        elif column == 3:
            self.book_dummy_data[row][2] = edited_text
        elif column == 4:
            self.book_dummy_data[row][3] = edited_text
        elif column == 5:
            self.book_dummy_data[row][4] = edited_text

    def save_book_changes(self, row_index):
        # 수정된 내용을 데이터에 반영
        for col_index in range(1, self.result_table.columnCount()):
            edited_text = self.result_table.item(row_index, col_index).text()
            self.book_dummy_data[row_index][col_index - 1] = edited_text  # 수정된 내용을 데이터에 반영

        # 편집 모드 해제
        for col_index in range(1, self.result_table.columnCount()):
            item = self.result_table.item(row_index, col_index)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # 편집 가능한 플래그 제거

        # 저장 버튼 삭제
        self.result_table.removeCellWidget(row_index, self.result_table.columnCount() - 1)

    def delete_data(self, what_deleting_for:str):
        # 선택된 행의 인덱스 추적
        if what_deleting_for == 'book':
            result_table = self.result_table
            data = self.book_dummy_data
        elif what_deleting_for == 'user':
            result_table = self.user_result_table
            data = self.user_dummy_data

        selected_rows = []
        for row_index in range(result_table.rowCount()):
            checkbox_item = result_table.item(row_index, 0)
            if checkbox_item.checkState() == Qt.Checked:
                selected_rows.append(row_index)

        # 선택된 항목이 없을 경우 메시지 표시 후 종료
        if not selected_rows:
            QMessageBox.information(self, "알림", "삭제할 항목을 선택하세요.")
            return
        # 삭제를 확인하는 메시지 박스 표시
        reply = QMessageBox.question(self, '확인', '선택된 항목을 삭제하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # 사용자가 "예"를 선택한 경우에만 삭제 진행
        if reply == QMessageBox.Yes:
            # 선택된 행을 역순으로 반복하여 삭제하여 인덱스 오류를 방지합니다.
            for row_index in reversed(selected_rows):
                result_table.removeRow(row_index)
                data.remove(data[row_index])

    
    def search_loan(self):
        user_name = self.loan_edit.text()
        # 대출 정보 검색 기능을 여기에 추가하세요
        # 예를 들어, 회원 이름을 사용하여 대출 정보를 데이터베이스에서 검색하고 결과를 self.loan_result에 표시할 수 있습니다.
        self.loan_result.setText("대출 정보를 검색합니다: " + user_name)

    def loan_book(self):
        pass

class BookAddDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("도서 추가")
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()

        self.book_name_edit = QLineEdit()
        self.author_edit = QLineEdit()
        self.publisher_edit = QLineEdit()
        self.publish_year_edit = QLineEdit()
        self.book_code_edit = QLineEdit()

        book_name_layout = QHBoxLayout()
        book_name_layout.addWidget(QLabel("도서명:"))
        book_name_layout.addWidget(self.book_name_edit)

        author_layout = QHBoxLayout()
        author_layout.addWidget(QLabel("저자:"))
        author_layout.addWidget(self.author_edit)

        publisher_layout = QHBoxLayout()
        publisher_layout.addWidget(QLabel("출판사:"))
        publisher_layout.addWidget(self.publisher_edit)

        publish_year_layout = QHBoxLayout()
        publish_year_layout.addWidget(QLabel("출판년도:"))
        publish_year_layout.addWidget(self.publish_year_edit)

        book_code_layout = QHBoxLayout()
        book_code_layout.addWidget(QLabel("도서 번호:"))
        book_code_layout.addWidget(self.book_code_edit)

        layout.addLayout(book_name_layout)
        layout.addLayout(author_layout)
        layout.addLayout(publisher_layout)
        layout.addLayout(publish_year_layout)
        layout.addLayout(book_code_layout)

        add_button = QPushButton("추가")
        add_button.clicked.connect(self.accept)

        layout.addWidget(add_button)

        self.setLayout(layout)

    def get_book_info(self):
        book_name = self.book_name_edit.text()
        author = self.author_edit.text()
        publisher = self.publisher_edit.text()
        publish_year = self.publish_year_edit.text()
        book_code = self.book_code_edit.text()

        # 올바르지 않은 값 필터링

        return book_name, author, publisher, publish_year, book_code
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryWindow()
    window.show()
    sys.exit(app.exec_())
