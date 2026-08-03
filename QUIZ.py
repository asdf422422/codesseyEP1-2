import sys #KeyboardInterrupt와 EOFError 처리용 시스템 

# 1. 메뉴(로 복귀도 가능해야하고 메뉴에서 나갈수도있어야하고나너무배고프다그냥재미없지나갈까..상태가되)

# 2. 입력/예외처리 함수 
# 숫자 입력(앞뒤 공백 제거, 변환 실패 or 범위밖 or 빈입력 시 재입력)
def numinput(min=1, max=4): #default 범위가 1~4(답안 선택지)
    while True:
        try:
            num = input("선택할 번호를 입력해주세요: ")
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
            # 필요한 저장 작업이 있다면 여기에서 수행
            sys.exit(0)
# 데이터 파일이 없거나, 손상된 경우 -> 기본 퀴즈 데이터로 복구(혹은 초기화)

#퀴즈 클래스
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

    def grading(self, ans):
        if ans == self.answer:
            print("정답입니다! +10점")
            return True
        else:
            print("오답입니다. +0점")
            return False

quiz1 = QUIZ("누오", "누오의 색깔은?", ["파란색", "빨간색", "노란색", "주황색"], 4)

#퀴즈 추가
#퀴즈 목록
#퀴즈 풀기
#점수 확인
#퀴즈게임 클래스
#파일 저장 및 불러오기
