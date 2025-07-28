-- 사용자 정보를 저장하는 테이블
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(50) NOT NULL COMMENT '사용자 이름',
    email VARCHAR(100) NOT NULL UNIQUE COMMENT '이메일 주소',
    signup_date DATE COMMENT '가입일'
);

-- 주문 정보를 저장하는 테이블
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '주문 번호',
    user_id INT COMMENT '사용자 ID',
    product_name VARCHAR(100) NOT NULL COMMENT '상품명',
    amount DECIMAL(10, 2) NOT NULL COMMENT '주문 금액',
    order_date DATE COMMENT '주문일',
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 샘플 사용자 데이터 삽입
INSERT INTO users (user_name, email, signup_date) VALUES
('홍길동', 'gildong@example.com', '2024-01-15'),
('이순신', 'sunsin@example.com', '2024-02-20'),
('세종대왕', 'sejong@example.com', '2024-03-10');

-- 샘플 주문 데이터 삽입
INSERT INTO orders (user_id, product_name, amount, order_date) VALUES
(1, '노트북', 1500000.00, '2024-07-01'),
(2, '기계식 키보드', 120000.00, '2024-07-03'),
(1, '무선 마우스', 35000.00, '2024-07-05'),
(3, '집현전 대형 책상', 250000.00, '2024-07-10'),
(2, '거북선 모양 USB', 25000.00, '2024-07-12');
