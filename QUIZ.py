import sys #KeyboardInterrupt와 EOFError 처리용 시스템 
import json #데이터 기록용
import random #랜덤 출제용
from datetime import datetime #시간/날짜 기록용

# region 스타일
RESET = "\033[0m"
BOLD = "\033[1m"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# 밝은 색
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
# endregion


class Quiz:
    def __init__(self, question, choices, answer, hint):
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

        self.question = question
        self.choices = list(choices)
        self.answer = answer
        self.hint = hint

    def solve(self):
        hint = 0 
        print(f"{BOLD}{self.question}{RESET}")

        for i, choice in enumerate(self.choices, start=1):
            print(f"{CYAN}{i}.{RESET} {choice}")

        print("0을 입력하면 힌트를 받을 수 있습니다.")
        answer = numinput(f"{BRIGHT_YELLOW}{BOLD}답을 입력하세요 ▶ {RESET}", 0, 4)
        if answer == 0:
            print(f"{CYAN}HINT: {RESET} {self.hint}")
            hint = 1
            answer = numinput(f"{BRIGHT_YELLOW}{BOLD}답을 입력하세요 ▶ {RESET}", 1, 4)

        if answer == self.answer:
            if hint ==1: 
                print(f"{BRIGHT_GREEN}{BOLD}✅ 정답입니다! +5점{RESET}")
                return 5
            print(f"{BRIGHT_GREEN}{BOLD}✅ 정답입니다! +10점{RESET}")
            return 10
        print(f"{BRIGHT_RED}{BOLD}❌ 오답입니다. +0점{RESET}")
        return 0


class QuizGame:
    def __init__(self):
        # 1. 데이터 관리자 인스턴스 생성 (의존성 주입 준비)
        self.data_manager = GameData()

        # 2. 데이터 관리자로부터 초기 값 가져오기
        self.quizzes = self.data_manager.quizzes
        self.best_score = self.data_manager.best_score

    
    def menu(self):

        print(f"""
{BRIGHT_CYAN}{BOLD}
===================================
        🎮 퀴즈 게임
===================================
{RESET}
{BRIGHT_GREEN}1.{RESET} 퀴즈 풀기
{BRIGHT_GREEN}2.{RESET} 퀴즈 추가
{BRIGHT_GREEN}3.{RESET} 목록 보기
{BRIGHT_GREEN}4.{RESET} 퀴즈 삭제
{BRIGHT_GREEN}5.{RESET} 최고 점수
{BRIGHT_GREEN}6.{RESET} 저장 / 불러오기
{BRIGHT_RED}0.{RESET} 종료
""")

        select = numinput(f"{BRIGHT_GREEN}{BOLD}메뉴 선택 ▶ {RESET}", 0, 6)

        if select == 0:
            self.exit_program()
        elif select == 1:
            self.quizsolve()
        elif select == 2:
            self.quizappend()
        elif select == 3:
            self.quizlist()
        elif select ==4:
            self.quizdelete()
        elif select == 5:
            self.quizscore()
        elif select == 6:
            self.file_menu()


    def file_menu(self):
        print("1. 저장")
        print("2. 불러오기")

        choice = numinput("선택: ", 1, 2)

        if choice == 1:
            self.data_manager.save()
        else:
            self.data_manager.load()

    def exit_program(self):
        choice = numinput("저장 후 종료하시겠습니까? (1: 저장 후 종료, 2: 저장하지 않고 종료, 3: 취소): ", 1, 3)

        if choice == 1:
            self.data_manager.save()
            print(f"{BRIGHT_RED}{BOLD}프로그램을 종료합니다.{RESET}")
            sys.exit()

        elif choice == 2:
            print(f"{BRIGHT_RED}{BOLD}저장하지 않고 프로그램을 종료합니다.{RESET}")
            sys.exit()

        else:
            return

    def quizsolve(self):
        score = 0
        if len(self.quizzes) == 0:
            print("저장된 퀴즈가 없습니다.")
            return

        select = numinput("풀 문제 수를 선택하세요: ", 1, len(self.quizzes))
        newquizzes = random.sample(self.quizzes, select)
        startT = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for quiz in newquizzes:
            score += quiz.solve()

        print(f"\n{BRIGHT_YELLOW}{BOLD}현재 점수: {score}점{RESET}")

        # 최고 점수 갱신
        if score > self.best_score:
            self.best_score = score
            self.data_manager.save()

            print(f"{BRIGHT_MAGENTA}{BOLD}🏆 최고 점수가 갱신되었습니다!{RESET}")

        endT = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.data_manager.add_history(newquizzes, score, startT, endT)
        print(self.data_manager.history)


    def quizappend(self):

        # 질문 입력
        question = blankinput("퀴즈의 질문을 입력하세요: ")


        # 선택지 입력
        choices = []
        for i in range(1, 5):
            choice = blankinput(f"{i}번째 선택지를 입력하세요: ")

        print("\n입력한 선택지:")
        for i, choice in enumerate(choices, start=1):
            print(f"{i}. {choice}")

        # 정답 번호 입력
        answer = numinput("정답의 번호를 입력하세요: ")

        # 힌트 입력
        hint = blankinput("정답에 대한 힌트 입력하세요: ")

        # Quiz 객체 생성 후 목록에 추가
        quiz = Quiz(question, choices, answer, hint)
        self.quizzes.append(quiz)

        print("퀴즈가 추가되었습니다.")

    def quizdelete(self):
        self.quizlist()
        num = numinput("삭제할 퀴즈 번호를 선택하세요: ",1,len(self.quizzes))
        del self.quizzes[num-1]
        self.data_manager.save()
    
    def quizlist(self):
        if len(self.quizzes) == 0:
            print("저장된 퀴즈가 없습니다.")
            return

        print(f"""{BRIGHT_BLUE}{BOLD}📚 퀴즈 목록{RESET}""")
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"{BRIGHT_CYAN}{i:2}.{RESET} {quiz.question}")
    
    def quizscore(self):
        print(f"\n{BRIGHT_YELLOW}{BOLD}최고 점수: {self.best_score}점{RESET}")


class GameData:
    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.history = []
        self.load() # 시작 시 자동 로드

    def save(self):
        # 퀴즈 객체를 딕셔너리로 변환하여 저장
        data = {
            "best_score": self.best_score,
            "quizzes": [q.__dict__ for q in self.quizzes],
            "history": self.history
        }
        with open("state.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"{GREEN}데이터가 저장되었습니다.{RESET}")

    def load(self):
        try:
            with open("state.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.best_score = data.get("best_score", 0)
                self.quizzes = [Quiz(**q) for q in data.get("quizzes", [])]
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            print(f"{BRIGHT_RED}{BOLD}저장된 데이터가 없거나 손상되었습니다.{RESET}")
            print("기본 퀴즈 데이터로 복구합니다.")

            self.quizzes = self.create_basic_quizzes()
            self.best_score = 0
            self.data = {
                "quizzes": [],
                "best_score": self.best_score
            }

            self.save()

            print(f"{BRIGHT_CYAN}✔ 데이터 불러오기 완료!{RESET}")


    def add_history(self, quizzes, score, startT, endT):
        """새로운 게임 결과를 히스토리에 추가하고 최고 점수를 갱신합니다."""
        # 1. 최고 점수 갱신
        if score > self.best_score:
            self.best_score = score
            print(f"🎊 최고 점수 경신: {self.best_score}점!")

        # 2. 히스토리 데이터 생성
        record = {
            "quizlength": len(quizzes),
            "score": score,
            "start_time": startT,
            "end_time": endT
        }
        self.history.append(record)
        
        # 3. 변경된 내용 파일에 저장
        self.save()

    def reset_to_default(self):
        self.quizzes = self.create_basic_quizzes()
        self.best_score = 0
        self.history = []
        self.save()

    @staticmethod
    def create_basic_quizzes():
        # (기존 코드와 동일)
        return [
            Quiz("누오의 색깔은 무엇인가?", ["빨간색", "하늘색", "노란색", "주황색"], 2, "누오는 물에 산다."),
            Quiz("누오의 타입은 무엇인가?", ["물, 땅", "물, 불", "불, 땅", "전기, 비행"], 1, "누오는 물에 산다."),
            Quiz("누오의 세대는 무엇인가?", ["1", "2", "3", "4"], 2, "꽤 초반이다."),
            Quiz("누오의 분류는 무엇인가?", ["전설의 포켓몬", "프릴 포켓몬", "스타팅 포켓몬", "수어 포켓몬"], 4, "누오는 물에 산다."),
            Quiz("어떤 포켓몬이 진화하여 누오가 되는가?", ["누리레느", "발챙이", "우파", "수댕이"], 3, "작고 동그랗다.")
        ]


def numinput(prompt, min_val=1, max_val=4):
    while True:
        try:
            val = int(input(prompt))
            if val < min_val:
                print(f"{min_val} 이상의 숫자를 입력하세요.")
                continue
            if val > max_val:
                print(f"{max_val} 이하의 숫자를 입력하세요.")
                continue
            return val
        except ValueError:
            print(f"{RED}숫자만 입력 가능합니다. 다시 시도하세요.{RESET}")

def blankinput(prompt):
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("빈 입력입니다.")

if __name__ == "__main__":
    game = QuizGame()
    try:
        game.menu()
    except(KeyboardInterrupt, EOFError):
        print("종료")
        game.data_manager.save()
        sys.exit()
