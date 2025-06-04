#!/bin/bash

SCRIPT="main.py"

declare -a TEST_CASES=(
  # ✅ Valid basic commands
  "CREATE TABLE users (id INT, name TEXT);"
  "CREATE TABLE employees (id INT, name TEXT, salary INT);"
  "CREATE TABLE logs (timestamp TEXT, message TEXT);"
  "INSERT INTO users (id, name) VALUES (1, 'Alice');"
  "INSERT INTO users (id, name) VALUES (2, 'Bob');"
  "INSERT INTO employees (id, name, salary) VALUES (1, 'Eve', 60000);"
  "INSERT INTO employees (id, name, salary) VALUES (2, 'Mallory', 45000);"
  "SELECT * FROM users;"
  "SELECT name FROM users;"
  "SELECT id, name FROM employees;"
  "SELECT * FROM employees WHERE salary >= 50000;"
  "SELECT id FROM users WHERE name = 'Alice';"
  "UPDATE users SET name = 'Alicia' WHERE id = 1;"
  "UPDATE employees SET salary = 70000 WHERE name = 'Eve';"
  "DELETE FROM users WHERE id = 2;"
  "DELETE FROM employees WHERE name = 'Mallory';"
  "DROP TABLE users;"
  "DROP TABLE employees;"
  "CREATE TABLE products (id INT, price INT);"
  "INSERT INTO products (id, price) VALUES (1, 100);"
  "UPDATE products SET price = 120 WHERE id = 1;"
  "SELECT * FROM products WHERE price > 100;"
  "DELETE FROM products WHERE id = 1;"
  "CREATE TABLE a (x INT);"
  "INSERT INTO a (x) VALUES (1);"
  "INSERT INTO a (x) VALUES (2);"
  "SELECT x FROM a WHERE x = 2;"
  "DROP TABLE a;"
  "CREATE TABLE t (c INT);"
  "SELECT * FROM t WHERE c = 5;"

  # 🧪 Edge case queries
  "select * from users;"
  "Select name from USERS;"
  "SELECT    *    FROM    users;"
  "select id,name from users;"
  "INSERT INTO users(name,age)VALUES('Bob',30);"
  "Insert into users ( name , age ) values ( 'Carol' , 22 );"
  "   SELECT * FROM users WHERE age   <  40 ;"
  "UPDATE users SET name='Dave' WHERE id=1;"
  "update USERS set age = 33 where name = 'Bob';"
  "DELETE    FROM   users   WHERE name='Dave';"

  # ❌ Invalid queries
  "SELECT * FROM bad@table;"
  "SELECT FROM missing_column;"
  "INSERT INTO users name, age VALUES ('Alice', 25);"
  "UPDATE SET age = 30 WHERE name = 'Alice';"
  "DELETE FROM WHERE id = 1;"
  "CREATE TABLE missing_paren id INT, name TEXT;"
  "CREATE users (id INT);"
  "INSERT INTO users (name age) VALUES ('John', 22);"
  "DROP FROM users;"
  "SELECT * users WHERE age = 30;"
  "SELECT id name FROM users;"
  "UPDATE users SET = 5 WHERE id = 1;"
  "SELECT * FROM WHERE age > 30;"
  "INSERT users VALUES ('Jake', 28);"
  "INSERT INTO users ('Jake', 28);"
  "UPDATE users WHERE name = 'Bob';"
  "DELETE users WHERE id = 1;"
  "CREATE TABLE test id INT;"
  "INSERT INTO (name) VALUES ('Bob');"
  "SELECT WHERE id = 1;"

  # 🔁 Stress cases
  "CREATE TABLE bigtable (a INT, b INT, c INT);"
  "INSERT INTO bigtable (a, b, c) VALUES (1, 2, 3);"
  "INSERT INTO bigtable (a, b, c) VALUES (4, 5, 6);"
  "INSERT INTO bigtable (a, b, c) VALUES (7, 8, 9);"
  "UPDATE bigtable SET b = 20 WHERE a = 1;"
  "DELETE FROM bigtable WHERE c = 6;"
  "SELECT * FROM bigtable;"
  "DROP TABLE bigtable;"
  "CREATE TABLE test123 (id INT);"
  "INSERT INTO test123 (id) VALUES (999);"
  "SELECT id FROM test123 WHERE id != 1000;"
  "UPDATE test123 SET id = 1001 WHERE id = 999;"
  "DELETE FROM test123 WHERE id = 1001;"

  # ⏱ Value + empty string edge cases
  "SELECT * FROM logs WHERE message = '';"
  "SELECT * FROM logs WHERE timestamp = ' ';"
  "SELECT * FROM logs WHERE message = 'hello world';"
  "UPDATE logs SET message = '' WHERE timestamp = '2024-01-01';"
  "INSERT INTO logs (timestamp, message) VALUES ('2024-01-01', 'Started');"
  "INSERT INTO logs (timestamp, message) VALUES ('2024-01-02', 'Shutdown');"
  "SELECT * FROM logs;"
  "DELETE FROM logs WHERE message = 'Shutdown';"

  # 🧩 Invalid characters/keywords
  "SELECT * FROM SELECT;"
  "INSERT INTO DROP (id) VALUES (1);"
  "CREATE TABLE IF EXISTS users (id INT);"
  "SELECT * FROM users#;"
  "SELECT ! FROM users;"
  "INSERT INTO users (id) VALUES (NULL);"
  "SELECT id FROM users WHERE age === 30;"
  "INSERT INTO users (id, name VALUES (1, 'Bob');"
  "UPDATE users SET age WHERE name = 'Bob';"
  "DROP TABLE;"
)

# Run each test case
for sql in "${TEST_CASES[@]}"; do
  echo -e "\033[1;34mRunning test:\033[0m \"$sql\""
  output=$(python3 "$SCRIPT" "$sql" 2>&1)
  if [[ $? -eq 0 ]]; then
    echo -e "\033[1;32mTest passed:\033[0m $sql"
    echo "$output"
  else
    echo -e "\033[1;31mTest failed:\033[0m $sql"
    echo "$output"
  fi
  echo -e "\033[1;35m----------------------------------------\033[0m"
done

echo -e "\033[1;32mAll tests completed.\033[0m"
read -p "Press Enter to exit..."
