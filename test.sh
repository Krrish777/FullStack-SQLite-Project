#!/bin/bash

# Adjust this if main.py is located elsewhere
SCRIPT="main.py"

# Define an array of test SQL queries
declare -a TEST_CASES=(
  "SELECT * FROM users WHERE age > 30;"
  "INSERT INTO users (name, age) VALUES ('Alice', 25);"
  "UPDATE users SET age = 26 WHERE name = 'Alice';"
  "DELETE FROM users WHERE name = 'Alice';"
  "CREATE TABLE books (id INT, title TEXT);"
  "SELECT name FROM employees WHERE salary >= 50000;"
  "SELECT id, name FROM orders WHERE date = '2024-01-01';"
  "SELECT * FROM bad@table;"   # Should raise tokenization error
  "SELECT FROM missing_column" # Should raise tokenization error
)

# Run each test case
for sql in "${TEST_CASES[@]}"; do
  echo -e "\033[1;34mRunning test:\033[0m \"$sql\""
  
  # Run the Python script with the SQL query using python3
  output=$(python3 "$SCRIPT" "$sql" 2>&1)  # Using python3 instead of python
  
  # Check if the test passed or failed based on the output
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
