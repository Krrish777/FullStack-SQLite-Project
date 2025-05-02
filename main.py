from compiler.tokenizer import Tokenizer

if __name__ == "__main__":
    tokenizer = Tokenizer()
    sql = "SELECT * FROM users WHERE age > 30;"
    tokens = tokenizer.tokenize(sql)
    for token in tokens:
        print(token)