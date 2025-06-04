#!/bin/bash

SCRIPT="main.py"

declare -a TEST_CASES=(
  # ✅ Valid DROP statements
  "DROP TABLE users;"
  "DROP TABLE employees;"
  "DROP TABLE IF EXISTS logs;"        # Should fail if IF EXISTS is not supported
  "DROP TABLE products;"
  "DROP TABLE temp_table;"

  # 🧪 Case insensitivity
  "drop table orders;"
  "DrOp TaBlE customers;"

  # ❌ Invalid DROP statements
  "DROP users;"                       # Missing 'TABLE' keyword
  "DROP TABLE;"                       # Missing table name
  "DROP TABLE 123abc;"                # Invalid table name
  "DROP TABLE users extra;"           # Extra tokens
  "DROP FROM users;"                  # Invalid keyword
  "DROP;"                             # Incomplete statement
  "DROP TABLE users WHERE id = 1;"    # DROP does not support WHERE
)

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

echo -e "\033[1;32mDROP TABLE tests completed.\033[0m"
read -p "Press Enter to exit..."
