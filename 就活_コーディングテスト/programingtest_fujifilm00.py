def greet_with_string(s):
    greeting = f"Hello {s}!"
    return greeting

input_string = input("文字列を入力してください: ")
result = greet_with_string(input_string)
print(result)
