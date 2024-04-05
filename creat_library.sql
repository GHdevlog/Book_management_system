
-- create database library;
-- use library;

-- 도서 정보를 저장하는 테이블
CREATE TABLE books (
book_id INT AUTO_INCREMENT PRIMARY KEY, -- 도서 고유 식별자
title VARCHAR(255) NOT NULL, -- 도서 제목
author VARCHAR(255) NOT NULL, -- 도서 저자
publisher VARCHAR(255) NOT NULL, -- 출판사
publication_year INT NOT NULL, -- 도서 번호
loan_status BOOLEAN DEFAULT FALSE -- 도서의 대출 가능 여부
);

-- 사용자 정보를 저장하는 테이블 (선택 사항)
CREATE TABLE users(
user_id INT AUTO_INCREMENT PRIMARY KEY, -- 사용자 고유 식별자
username VARCHAR(50) NOT NULL UNIQUE, -- 사용자 이름
phone_number VARCHAR(15) NOT NULL, -- 사용자 연락처
max_loan INT NOT NULL, -- 대출가능 도서 수
loaning INT NOT NULL, -- 대출중인 도서 수
);

-- 대출 이력을 저장하는 테이블
CREATE TABLE loans (
loan_id INT AUTO_INCREMENT PRIMARY KEY, -- 대출 이력 고유 식별자
user_id INT NOT NULL, -- 대출한 사용자의 ID
book_id INT NOT NULL, -- 대출한 도서의 ID
loan_date DATE NOT NULL, -- 대출 날짜
return_date DATE, -- 반납 날짜 (NULL인 경우 아직 반납되지 않음)
FOREIGN KEY (user_id) REFERENCES users(user_id),
FOREIGN KEY (book_id) REFERENCES books(book_id)
);

