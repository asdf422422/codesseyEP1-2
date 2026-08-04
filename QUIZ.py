import sys #KeyboardInterrupt와 EOFError 처리용 시스템 
import json #데이터 기록용



class Quiz:
    def __init__(self, topic, question, choices, answer):
        if not isinstance(choices, (list, tuple)):
            raise TypeError("choices는 리스트 또는 튜플이어야 합니다.")

        try:
            answer = int(answer)
        except (ValueError, TypeError):
            raise ValueError("정답은 1~4 사이의 정수여야 합니다.")

        if len(choices) != 4:
            raise ValueError("choices는 4개로 구성되어야 합니다.")

        if not (1 <= answer <= 4):
            raise ValueError("정답은 1~4 사이의 정수여야 합니다.")

        self.topic = topic
        self.question = question
        self.choices = list(choices)
        self.answer = answer

    def solve(self):
        print(f"\n[{self.topic}]")
        print(self.question)

        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")

        answer = numinput("답을 입력하세요: ", 1, 4)

        return self.grading(answer)

    def grading(self, answer):
        if answer == self.answer:
            print("정답입니다! +10점")
            return True

        print("오답입니다. +0점")
        return False

class QuizGame:
    def __init__(self):
        best_score = 0
        basedata = create_basic_data(best_score)
    
    def menu(self):
        while True:
            print()
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 목록 보기")
            print("4. 점수 확인")
            print("5. 파일 저장/불러오기")
            print("0. 종료")

            select = numinput(min=0, max=5)

            if select == 0:
                self.exit_program()
            elif select == 1:
                self.quizsolve()
            elif select == 2:
                self.quizappend()
            elif select == 3:
                self.quizlist()
            elif select == 4:
                self.quizscore()
            elif select == 5:
                self.file_menu()

    def file_menu(self):
        print("1. 저장")
        print("2. 불러오기")

        choice = numinput("선택: ", 1, 2)

        if choice == 1:
            self.save()
        else:
            self.load()

    def exit_program(self):
        choice = numinput(
            "저장 후 종료하시겠습니까? (1: 저장 후 종료, 2: 저장하지 않고 종료, 3: 취소): ",
            1,
            3
        )

        if choice == 1:
            self.save()
            print("저장 후 종료합니다.")
            sys.exit()

        elif choice == 2:
            print("저장하지 않고 종료합니다.")
            sys.exit()

        else:
            return

    def quizsolve(self):
        score = 0

        if len(self.quizzes) == 0:
            print("저장된 퀴즈가 없습니다.")
            return

        for quiz in self.quizzes:
            if quiz.solve():
                score += 10

        print(f"{score}점 입니다.")

        # 최고 점수 갱신
        if score > self.best_score:
            self.best_score = score
            self.data["best_score"] = self.best_score

            with open("state.json", "w", encoding="utf-8") as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)

            print("최고 점수가 갱신되었습니다!")

    def quizappend(self):
        topic = input("퀴즈의 주제를 입력하세요: ")
        question = input("퀴즈의 질문을 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choices.append(input(f"{i}번째 선택지를 입력하세요: "))

        print("\n입력한 선택지:")
        for i, choice in enumerate(choices, start=1):
            print(f"{i}. {choice}")

        answer = numinput("정답의 번호를 입력하세요: ")

        # Quiz 객체 생성 후 목록에 추가
        quiz = Quiz(topic, question, choices, answer)
        self.quizzes.append(quiz)

        print("퀴즈가 추가되었습니다.")
    
    def quizlist(self):
        if len(self.quizzes) == 0:
            print("저장된 퀴즈가 없습니다.")
            return

        print("\033[34m퀴즈 목록\033[0m")

        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"{i}. {quiz.question}")
    
    def quizscore(self):
        print(f"최고 점수: {self.best_score}점")
    
    def save(self):
        self.data["quizzes"] = []

        for quiz in self.quizzes:
            self.data["quizzes"].append({
                "topic": quiz.topic,
                "question": quiz.question,
                "choices": quiz.choices,
                "answer": quiz.answer
            })

        self.data["best_score"] = self.best_score

        with open("state.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

        print("Quizzes saved!")

    def load(self):
        try:
            with open("state.json", "r", encoding="utf-8") as file:
                self.data = json.load(file)

            self.best_score = self.data.get("best_score", 0)

            self.quizzes = []

            for quiz in self.data.get("quizzes", []):
                self.quizzes.append(
                    Quiz(
                        quiz["topic"],
                        quiz["question"],
                        quiz["choices"],
                        quiz["answer"]
                    )
                )

            print("Quizzes loaded!")

        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            print("저장된 데이터가 없거나 손상되었습니다.")
            print("기본 퀴즈 데이터로 복구합니다.")

            self.quizzes = create_basic_quizzes()
            self.best_score = 0
            self.data = {
                "quizzes": [],
                "best_score": self.best_score
            }

            self.save()

            print("기본 데이터 복구 완료!")


def numinput(prompt="선택할 번호를 입력해주세요: ", min=1, max=4):
    while True:
        try:
            value = input(prompt).strip()

            # 빈 입력 체크
            if value == "":
                print("입력이 비어 있습니다. 다시 입력하세요.")
                continue

            value = int(value)

            # 범위 체크
            if value < min or value > max:
                print(f"{min}부터 {max} 사이의 값을 입력해주세요.")
                continue

            return value

        except ValueError:
            print("정수를 입력해주세요.")

        except (KeyboardInterrupt, EOFError):
            print("\n입력이 취소되었습니다. 프로그램을 종료합니다.")
            sys.exit(0)

def create_basic_quizzes():
    quiz1 = Quiz(
        "누오",
        "누오의 색깔은 무엇인가?",
        ["빨간색", "파란색", "노란색", "주황색"],
        2
    )

    quiz2 = Quiz(
        "누오",
        "누오의 타입은 무엇인가?",
        ["물, 땅", "물, 불", "불, 땅", "전기, 비행"],
        1
    )

    quiz3 = Quiz(
        "누오",
        "누오의 세대는 무엇인가?",
        ["1", "2", "3", "4"],
        2
    )

    quiz4 = Quiz(
        "누오",
        "누오의 분류는 무엇인가?",
        ["전설의 포켓몬", "프릴 포켓몬", "스타팅 포켓몬", "수어 포켓몬"],
        4
    )

    quiz5 = Quiz(
        "누오",
        "어떤 포켓몬이 진화하여 누오가 되는가?",
        ["누리레느", "발챙이", "우파", "수댕이"],
        3
    )

    return [quiz1, quiz2, quiz3, quiz4, quiz5]


def create_basic_data(best_score=0):
    quizzes = create_basic_quizzes()

    basedata = {
        "quizzes": [],
        "best_score": best_score
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

    return basedata


if __name__ == "__main__":
    game = QuizGame()
    game.menu()