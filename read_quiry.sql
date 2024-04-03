
SELECT count(*) FROM books;
SELECT * FROM books;
SELECT count(*) FROM users;
SELECT * FROM users;
SELECT count(*) FROM loans;
SELECT * FROM loans;


SET FOREIGN_KEY_CHECKS=0;
truncate table users;
SET FOREIGN_KEY_CHECKS=1;