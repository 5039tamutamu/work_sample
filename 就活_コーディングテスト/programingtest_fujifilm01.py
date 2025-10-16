def is_valid_password(password):
    if len(password) != 4:
        return False
    
    if not password.isdigit():
        return False
    
    unique_chars = set(password)
    if len(unique_chars) < 2:
        return False
    
    return True

input_password = input("新しいパスワードを入力してください: ")
if is_valid_password(input_password):
    print("パスワードが必要条件を満たしています。")
else:
    print("パスワードが必要条件を満たしていません。")
