import random

def guess_the_number():
    # 1から10までのランダムな数を生成
    secret_number = random.randint(1, 10)
    
    attempts = 0

    print("Welcome to the Guess the Number game!")
    print("I have selected a number between 1 and 10. Can you guess it?")

    while True:
        try:
            # ユーザーに数を予想させる
            user_guess = int(input("Your guess: "))
            attempts += 1

            # 予想が正しいかどうかを判定
            if user_guess == secret_number:
                print(f"Congratulations! You guessed the number in {attempts} attempts.")
                break
            else:
                print("Incorrect! Try again.")

        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    guess_the_number()
