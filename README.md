## 프로젝트 개요
#### 나만의 퀴즈 게임 만들기
퀴즈를 풀고 점수를 기록할 수 있는 프로그램을 만들었다.

<br>

## checklist
- [ ] 동작하는 퀴즈 게임을 구현하였다. <br>
- [ ] 최소 2개 이상의 클래스를 정의해 기능별로 메서드를 분리한다. <br>
- [ ] 프로젝트 코드가 GitHub에 업로드되어 있다. <br>
- [ ] 최소 10개 이상의 의미 있는 커밋이 존재한다. <br>
- [ ] 최소 1회 이상의 브랜치 생성 및 병합(checkout, merge) 기록이 있다. <br>
- [ ] clone과 pull을 각각 1회 이상 사용한 기록이 있다. <br> <br>
<br>

## 퀴즈 주제 선정 이유
좋아하는 포켓몬인 누오에 대해 퀴즈를 구성하였다. 

<br>

## 실행 방법
1. 프로그램을 실행한다. <br> <br>
2. 메뉴를 확인하여 실행하고 싶은 기능의 숫자를 입력한다. (1. 퀴즈 출제, 2. 퀴즈 등록, 3. 퀴즈 목록 확인, 4. 점수 확인, 5. 저장 및 불러오기, 0. 종료) <br> <br>
3. 터미널 창의 안내에 따라 각 기능을 수행한다. <br>
4. 프로그램 종료를 원한다면 메뉴 창에서 0번 종료하기를 선택하고 종료한다.


<br>

## 기능 목록
- 프로그램 실행 시 메뉴에서 번호를 선택하면, 선택 결과에 따라 퀴즈 출제/등록/목록/삭제/점수 확인/종료 화면이 출력된다. <br>
- 퀴즈 풀기, 퀴즈 추가, 퀴즈 삭제, 퀴즈 목록, 점수 확인 기능이 동작한다. <br>
- 프로그램을 종료하고 다시 실행해도 추가한 퀴즈와 최고 점수가 유지된다. (파일 저장) 


<br>


## 파일 구조

#### Quiz class <br>
- 퀴즈 객체를 관리한다.
- 해당 퀴즈를 출력하고 정답을 입력받아 점수를 반환할 수 있다. 

#### QuizGame class <br>
- 퀴즈 게임을 관리한다.
- 메뉴 메서드를 통해 게임 기능들로 접근할 수 있다.
- 퀴즈를 풀거나, 더하거나, 삭제하거나, 목록을 확인할 수 있다.
- 최고 점수를 확인할 수 있다.
- 파일을 저장하거나 불러올 수 있다. 

#### GameData class <br>
- 게임의 데이터를 관리한다.
- 퀴즈 객체, 최고 점수, 게임 진행 히스토리를 속성으로 갖는다. 
- 위 데이터들을 JSON 파일로 저장하거나, 불러올 수 있다.
- state.JSON 파일이 손상되었거나 아예 없을 경우 초기 퀴즈 데이터를 불러올 수 있다.

<br>

## 데이터 파일 설명
- 경로: root/state.json
- 역할: 게임이 재실행되더라도 퀴즈와 점수 기록이 유지될 수 있도록 한다.

스키마
- best score을 점수로 기록하였다. 
- quiz 클래스의 규칙에 따라 생성된 퀴즈 객체들을 quizzes라는 리스트에 묶었다.
- 인스턴스를 딕셔너리 형태로 변환해 저장하였다.
- 퀴즈 개수와 점수, 시작 및 종료 시간을 확인 할 수 있는 게임 진행 히스토리를 기록하였다. 

파일 스키마
```py
data = {
    "best_score": self.best_score, #int
    "quizzes": [q.__dict__ for q in self.quizzes],
    "history": self.history #리스트
}
```
퀴즈 객체의 클래스 
```py
def __init__(self, question, choices, answer, hint):
    self.question = question #str
    self.choices = list(choices) #list
    self.answer = answer #int
    self.hint = hint #str
```


히스토리

```py
history = {
    "quizlength": len(quizzes), #int
    "score": score, #int
    "start_time": startT, #str('%Y-%m-%d %H:%M:%S')
    "end_time": endT, #str('%Y-%m-%d %H:%M:%S')
}
```

<br>

<details>
<summary> 파일 구조 예시 </summary>
    
```js
{
    "best_score": 20,
    "quizzes": [
        {
            "question": "누오의 색깔은 무엇인가?",
            "choices": [
                "빨간색",
                "하늘색",
                "노란색",
                "주황색"
            ],
            "answer": 2,
            "hint": "누오는 물에 산다."
        },
        {
            "question": "누오의 세대는 무엇인가?",
            "choices": [
                "1",
                "2",
                "3",
                "4"
            ],
            "answer": 2,
            "hint": "꽤 초반이다."
        },
        {
            "question": "누오의 분류는 무엇인가?",
            "choices": [
                "전설의 포켓몬",
                "프릴 포켓몬",
                "스타팅 포켓몬",
                "수어 포켓몬"
            ],
            "answer": 4,
            "hint": "누오는 물에 산다."
        },
        {
            "question": "어떤 포켓몬이 진화하여 누오가 되는가?",
            "choices": [
                "누리레느",
                "발챙이",
                "우파",
                "수댕이"
            ],
            "answer": 3,
            "hint": "작고 동그랗다."
        },
        {
            "question": "테스트",
            "choices": [
                "1번",
                "2번",
                "정답",
                "4번"
            ],
            "answer": 3,
            "hint": "힌트"
        },
        {
            "question": "1",
            "choices": [
                "3",
                "421",
                "42",
                "2"
            ],
            "answer": 2,
            "hint": "adf"
        }
    ],
    "history": [
        {
            "quizlength": 2,
            "score": 10,
            "start_time": "2026-08-11 13:18:26",
            "end_time": "2026-08-11 13:18:28"
        }
    ]
}
```

</details>

## 개발 환경
VS Code: 1.112.0 <br>
python: 3.12.13 <br>
git: 2.53.0 <br>

<img width="381" height="110" alt="스크린샷 2026-08-11 오후 1 34 16" src="https://github.com/user-attachments/assets/3250dbd3-d335-4bb6-8ca7-0a5d6d79c7e3" />

<details>
<summary> git config </summary>

```bash
credential.helper=osxkeychain
core.repositoryformatversion=0
core.filemode=true
core.bare=false
core.logallrefupdates=true
core.ignorecase=true
core.precomposeunicode=true
submodule.active=.
remote.origin.url=https://github.com/asdf422422/codesseyEP1-2.git
remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*
branch.main.remote=origin
branch.main.merge=refs/heads/main
branch.main.vscode-merge-base=origin/main
user.name=서현
user.email=00a0s0d0f00@gmail.com
```

<img width="466" height="204" alt="스크린샷 2026-08-11 오후 1 35 53" src="https://github.com/user-attachments/assets/d9912778-c92e-4b45-8f78-865a23c99a31" />

</details>

## 프로그램 실행 결과
### 퀴즈 추가
<img width="318" height="198" alt="스크린샷 2026-08-11 오후 1 39 32" src="https://github.com/user-attachments/assets/3491fd9d-8192-4dee-a66a-7a8b4d90ce82" />

### 퀴즈 목록
<img width="319" height="109" alt="스크린샷 2026-08-11 오후 1 38 49" src="https://github.com/user-attachments/assets/ad97a2a0-8f11-4141-8c94-e5053880ea55" />

### 퀴즈 플레이
<img width="357" height="495" alt="스크린샷 2026-08-11 오후 1 38 11" src="https://github.com/user-attachments/assets/fbb89ee6-364a-47b6-bf96-588670e16572" />

### 점수
<img width="137" height="29" alt="스크린샷 2026-08-11 오후 1 40 32" src="https://github.com/user-attachments/assets/f4180350-4758-428d-8fe9-0cc37de88152" />

## Git log 
<img width="866" height="406" alt="스크린샷 2026-08-11 오후 1 37 00" src="https://github.com/user-attachments/assets/6a9396e3-d169-4013-87b6-a0f80de599f1" />
