import sys
import pymysql
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton

class LibraryManagementApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Library Management System')

        # Add widgets
        self.lbl_title = QLabel('Title:', self)
        self.lbl_title.move(20, 20)
        self.txt_title = QLineEdit(self)
        self.txt_title.move(150, 20)

        self.lbl_author = QLabel('Author:', self)
        self.lbl_author.move(20, 50)
        self.txt_author = QLineEdit(self)
        self.txt_author.move(150, 50)

        self.lbl_publisher = QLabel('Publisher:', self)
        self.lbl_publisher.move(20, 80)
        self.txt_publisher = QLineEdit(self)
        self.txt_publisher.move(150, 80)

        self.lbl_publication_year = QLabel('Publication Year:', self)
        self.lbl_publication_year.move(20, 110)
        self.txt_publication_year = QLineEdit(self)
        self.txt_publication_year.move(150, 110)

        self.btn_add_book = QPushButton('Add Book', self)
        self.btn_add_book.move(150, 150)
        self.btn_add_book.clicked.connect(self.add_book)

        self.show()

    def add_book(self):
        title = self.txt_title.text()
        author = self.txt_author.text()
        publisher = self.txt_publisher.text()
        publication_year = int(self.txt_publication_year.text())

        # TODO: Add book to the database
        print(f'Adding book: {title}, {author}, {publisher}, {publication_year}')

    # MySQL 데이터베이스에 연결합니다.
  # 결과를 사전 형태로 반환하는 커서를 사용
    connection = pymysql.connect(host='localhost',  # 호스트 이름
                            user='root',    # 사용자 이름
                            password='0000',  # 비밀번호
                            database='library',  # 데이터베이스 이름
                            cursorclass=pymysql.cursors.DictCursor)
    def add_book(title, author, publisher, publication_year):
        try:
            # 커서를 사용하여 SQL 문을 실행합니다.
            with connection.cursor() as cursor:
                # 책을 추가하는 SQL 쿼리를 작성합니다.
                sql = "INSERT INTO books (title, author, publisher, publication_year) VALUES (%s, %s, %s, %s)"
                # SQL 쿼리를 실행하고 책 정보를 데이터베이스에 추가합니다.
                cursor.execute(sql, (title, author, publisher, publication_year))
            # 변경 사항을 커밋하여 데이터베이스에 반영합니다.
            connection.commit()
        except Exception as e:
            # 오류가 발생하면 오류 메시지를 출력하고 롤백합니다.
            print(f'Error adding book: {e}')
            connection.rollback()
        finally:
            # 연결을 닫습니다.
            if connection:
                connection.close()


# add_book 함수를 호출하여 책을 추가합니다.
# add_book('The Great Gatsby', 'F. Scott Fitzgerald', 'Scribner', 1925)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LibraryManagementApp()
    sys.exit(app.exec_())
