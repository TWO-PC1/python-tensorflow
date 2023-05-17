import random


game = True
value = random.randint(1, 101)
while game:
    
    input_value = input("숫자를 입력하세요: ")
    if input_value.isdigit():
        input_value = int(input_value)
        if input_value == value:
            print("정답입니다")
            game = False
        elif input_value > value:
            print("숫자가 큽니다")
        elif input_value < value:
            print("숫자가 작습니다")
    else:
        print("숫자를 입력하세요!!!!")
        continue
    

        

    