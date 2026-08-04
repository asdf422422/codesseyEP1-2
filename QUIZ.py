import sys #KeyboardInterrupt와 EOFError 처리용 시스템 
import json #데이터 기록용

maxscore = 0 #최고 점수 기록용
data = {
        "quizzes": [],
        "maxscore": maxscore
    } #save files 
# 1. [check] 메뉴(로 복귀도 가능해야하고 메뉴에서 나갈수도있어야하고나너무배고프다그냥재미없지나갈까..상태가되)
def menu():
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 목록 보기")
    print("4. 점수 확인")
    print("5. 파일 저장/불러오기")
    print("0. exit")
    select = numinput(min=0, max=5)
    if select == 0:
        exit_program()
    elif select == 1:
        quizsolve()
    elif select ==2:
        quizappend()
    elif select ==3:
        quizlist()
    elif select == 4:
        quizscore()
    elif select ==5:
        save_quizzes()

def exit_program():
    a = numinput("will you really quit? 1: yes, 2: no", 1, 2)
    if a == 1:
        sys.exit()
    elif a == 2:
        menu()
# 2. 입력/예외처리 함수 
# 숫자 입력(앞뒤 공백 제거, 변환 실패 or 범위밖 or 빈입력 시 재입력)
def numinput(prompt= "선택할 번호를 입력해주세요: ",min=1, max=4): #default 범위가 1~4(답안 선택지)
    while True:
        try:
            num = input(prompt)
            num = num.strip()
            
            #공백 체크
            if num == "":            
                print("입력이 비어 있습니다. 다시 입력하세요.")
                continue
            value = int(num)

            # 범위 체크
            if value < 1:
                print(f"{min} 이상의 값을 입력해주세요.")
                continue
            if value > 4:
                print(f"{max} 이히의 값을 입력해주세요.")
                continue
            return value

        except ValueError:
            # 정수 체크
            print("정수를 입력해주세요.")
        except (KeyboardInterrupt, EOFError):
            # 에러 발생시 
            print("\n입력이 취소되었습니다. 프로그램을 종료합니다.")
            # [check] 필요한 저장 작업이 있다면 여기에서 수행
            sys.exit(0)
# [check] 데이터 파일이 없거나, 손상된 경우 -> 기본 퀴즈 데이터로 복구(혹은 초기화)

# 퀴즈 클래스
class QUIZ:
    def __init__(self, topic, question, choices, answer):
        if not isinstance(choices, (list, tuple)):
            raise TypeError("choices는 리스트 또는 튜플여야 합니다.")
        try: 
            answer = int(answer)
        except ValueError:
            raise ValueError("정답은 1~4 사이의 정수여야 합니다.")
        
        if len(choices) != 4:
            raise ValueError("choices는 4개로 구성되어야 합니다.")

        if not (1 <= answer <= 4):
            raise ValueError("정답은 1~4 사이의 정수여야 합니다.")

        self.topic = topic
        self.question = question
        self.choices = choices
        self.answer = answer

    def solve(self):
        print(self.question)
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")
        ans = numinput()
        return self.grading(ans)
    
    def grading(self, ans):
        if ans == self.answer:
            print("정답입니다! +10점")
            return True
        else:
            print("오답입니다. +0점")
            return False

# 기본 퀴즈 데이터
quiz1 = QUIZ("누오", "누오의 색깔은 무엇인가?", ["빨간색", "파란색", "노란색", "주황색"], 2)
quiz2 = QUIZ("누오", "누오의 타입은 무엇인가?", ["물, 땅", "물, 불", "불, 땅", "전기, 비행"], 1)
quiz3 = QUIZ("누오", "누오의 세대는 무엇인가?", ["1", "2", "3", "4"], 2)
quiz4 = QUIZ("누오", "누오의 분류는 무엇인가?", ["전설의 포켓몬", "프릴 포켓몬", "스타팅 포켓몬", "수어 포켓몬"], 4)
quiz5 = QUIZ("누오", "어떤 포켓몬이 진화하여 누오가 되는가?", ["누리레느", "발챙이", "우파", "수댕이"], 3)

quizzes = [
    quiz1, quiz2, quiz3, quiz4, quiz5
]

basedata = {
        "quizzes": [],
        "maxscore": maxscore
    }
for quiz in quizzes:
    basedata["quizzes"].append({
        "topic": quiz.topic,
        "question": quiz.question,
        "choices": quiz.choices,
        "answer": quiz.answer
    })

with open("state.json", "w", encoding="utf-8") as file:
    json.dump(basedata, file, ensure_ascii=False, indent=4)

#[check] 퀴즈 풀기
def quizsolve():
    global maxscore
    score = 0 
    if len(quizzes) == 0:
        print("저장된 퀴즈가 없습니다.") 
        return 0
    for quiz in quizzes: 
        result = quiz.solve()
        if result:
            score +=10
    print(score, "점 입니다.")

    #max score
    if maxscore < score: 
        maxscore = score
        data["maxscore"] = maxscore
        with open("state.json", "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        
#save the maxscore
#[check] 퀴즈 추가
def quizappend():
    global quizzes
    quiz_number = len(quizzes) + 1
    quiz_name = f"quiz{quiz_number}"
    topic = input("Write the topic: ") 
    question = input("Write the questioin: ")
    choices = []
    for i in range(1,5):
        choices.append(input(f"Write {i}th choice: "))     
    for i, choice in enumerate(choices, start=1):
                print(f"{i}. {choice}")
    answer = numinput("Write the number of the answer: ")
    # check if the given values are usable
    quiz_name = QUIZ(topic, question, choices, answer)
    quizzes.append(quiz_name) 
# save the quiz 

# 퀴즈 목록
def quizlist():
    if len(quizzes) == 0:
        print("저장된 퀴즈가 없습니다.") 
        return 0
    i = 0
    print("\033[34m퀴즈 목록\033[0m")   
    for quiz in quizzes: 
        print(i, ".", quiz.question)
        i+=1

#[check] 퀴즈 풀기
# 점수 확인
def quizscore():
    print(maxscore, "is the best score!")

#[check] 퀴즈게임 클래스

#[check] 파일 저장 및 불러오기


def save_quizzes(quizzes, maxscore):
    global data

    for quiz in quizzes:
        data["quizzes"].append({
            "topic": quiz.topic,
            "question": quiz.question,
            "choices": quiz.choices,
            "answer": quiz.answer
        })

    with open("state.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print("Quizzes saved!")

menu()