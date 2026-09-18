/* dkYield99 교육과정 - 주차 데이터 단일 원본
 * 이 파일 하나를 고치면 curriculum/index.html · 주차 워크북 · docs/build_pptx.py 가 모두 따라갑니다.
 * 다른 곳에 주차 내용을 복사해 두지 마세요.
 */
window.DK_CURRICULUM =
{
 "project": "dkYield99",
 "labels": {
  "py": "Python",
  "dom": "화학공학",
  "lab": "dkYield99 실습",
  "stat": "데이터·통계"
 },
 "goals": [
  [
   "01",
   "Python 기초 활용",
   "변수·조건문·반복문·함수로 간단한 공정 계산 로직을 직접 작성한다."
  ],
  [
   "02",
   "공정을 데이터로 설계",
   "운전조건의 비용·효과·부작용·시너지를 구조화된 데이터로 표현한다."
  ],
  [
   "03",
   "시스템 사고",
   "수율·순도·안전·환경이 맞물린 공정 생태계의 인과를 추론한다."
  ],
  [
   "04",
   "공정 트레이드오프 판단",
   "생산량·품질·안전·원가 사이의 갈등을 균형 있게 의사결정한다."
  ],
  [
   "05",
   "데이터를 스스로 만든다",
   "시드·라벨·CSV로 <b>남이 다시 만들 수 있는</b> 운전 데이터를 직접 생산한다."
  ],
  [
   "06",
   "숫자를 직접 계산한다",
   "평균·표준편차·변동계수를 <b>엑셀로 한 번, 코드로 한 번</b> 구하고 두 값을 맞춰 본다."
  ],
  [
   "07",
   "AI의 답을 검증한다",
   "분포·관리도·공정능력으로 얻은 결론을, 그것이 틀릴 수 있는 이유와 <b>함께</b> 말할 수 있다."
  ]
 ],
 "assess": [
  [
   "25%",
   "주간 코드·공정 실습",
   "매주 실행되는 파일 + 3문장 노트"
  ],
  [
   "15%",
   "중간 공정팩 + 데이터셋 설명서",
   "공정 카드 5종 설계 · 내 데이터가 만들어진 방법 1쪽"
  ],
  [
   "20%",
   "데이터 분석 포트폴리오",
   "9~14주 반복실험 · 표 · 그림 모음"
  ],
  [
   "30%",
   "최종 검증 보고서",
   "공정 진단 · 근거 · 불확실성"
  ],
  [
   "10%",
   "발표·토론",
   "결과와 그 한계를 함께 말하기"
  ]
 ],
 "limitNote": "이 게임은 교육용으로 크게 단순화한 모형입니다. 여기서 나온 숫자는 <b>이 모형 안에서만</b> 참이며, 실제 현장의 값이나 인과를 그대로 말해 주지 않습니다.",
 "weeks": [
  {
   "w": 1,
   "track": "토대",
   "title": "오리엔테이션 · 설치 · 공정의 지표를 변수로",
   "goal": "게임을 설치해 한 판 돌려 보고, 화면의 숫자가 코드 속 <b>변수</b>라는 것을 그 자리에서 확인한다.",
   "py": {
    "h": "설치, 그리고 첫 변수",
    "b": "Python과 VS Code를 설치합니다. 변수는 값을 담는 상자입니다 - 정수(<code>1000</code>)·실수(<code>92.5</code>)·문자열(<code>\"공정\"</code>). <code>예산 = 1000</code> 처럼 이름에 값을 넣습니다."
   },
   "dom": {
    "h": "AI시대 공정 엔지니어링 · 운전의 기초",
    "b": "실제 플랜트는 조건 하나 바꾸는 데 큰 비용과 위험이 따릅니다. 시뮬레이션은 ‘실패해도 안전하게’ 결과를 미리 실험하는 도구입니다. 그 안의 숫자는 예산·생산량·수율·순도·안전입니다."
   },
   "lab": {
    "h": "12개월 운전 → 그 숫자를 코드에서 찾기",
    "b": "<code>_start.bat</code> 으로 게임을 켜고 12개월을 운전합니다. 그다음 <code>process_engine.py</code> 의 <code>new_plant()</code> 를 열면, 방금 화면에서 본 지표가 그대로 변수로 적혀 있습니다."
   },
   "code": {
    "cap": "new_plant() - 화면의 숫자가 여기 있습니다",
    "html": "<span class=\"k\">def</span> <span class=\"n\">new_plant</span>():\n    plant = {\n        <span class=\"s\">\"예산\"</span>: <span class=\"n\">1000</span>,      <span class=\"c\"># 지금 가진 돈(억)</span>\n        <span class=\"s\">\"생산량\"</span>: <span class=\"n\">100</span>,     <span class=\"c\"># 톤/월</span>\n        <span class=\"s\">\"수율\"</span>: <span class=\"n\">78</span>,      <span class=\"c\"># %</span>\n        <span class=\"s\">\"순도\"</span>: <span class=\"n\">92.5</span>,\n    }"
   },
   "practice": [
    "<b>lab/examples/week01/</b> 를 번호 순서로 열기 - 한 파일에 개념 하나입니다",
    "<b>VS Code</b> 설치 → 확장 <code>ms-python.python</code> 설치 (파이썬은 게임 폴더에 들어 있어 따로 설치하지 않습니다)",
    "<b>파일 → 폴더 열기</b> 로 게임 폴더를 통째로 열고, <code>Ctrl+Shift+P → Python: Select Interpreter</code> 에서 <code>.\\python\\python.exe</code> 고르기",
    "<b>_start.bat</b> 실행 → 게임 한 판 플레이 (12개월)",
    "<b>process_engine.py</b> 의 new_plant() 열어 화면에서 본 지표 찾기",
    "‘예산’ 값을 1000 → 1500 으로 바꾸고 새 게임으로 확인"
   ],
   "hw": "게임을 2번 플레이하고 ‘온도만 올렸을 때 무엇이 나빠졌는지’를 3줄로 적어 오세요. 핵심 지표의 의미도 표로 정리하세요.",
   "file": "INSTALL.md · docs/TOOLS.md · process_engine.py › new_plant()",
   "mno": "MODULE 01",
   "mtitle": "토대 - 공정·코드·화공의 첫 만남",
   "mspan": "1-3주",
   "l": "WEEK",
   "short": {
    "title": "오리엔테이션 · 설치 · 공정의 지표를 변수로",
    "py": "설치, 그리고 첫 변수",
    "dom": "AI시대 공정 엔지니어링 · 운전의 기초",
    "lab": "12개월 운전 → 그 숫자를 코드에서 찾기",
    "stat": "",
    "exam": ""
   },
   "explain": "_start.bat 으로 서버를 켜고, 화면의 지표가 처음 정의되는 함수를 같은 주에 함께 봅니다"
  },
  {
   "w": 2,
   "track": "토대",
   "title": "리스트·딕셔너리 = 공정 카드의 구조",
   "goal": "공정 카드가 데이터(딕셔너리)로 표현되는 방식을 이해한다.",
   "py": {
    "h": "리스트와 딕셔너리",
    "b": "리스트 <code>[a, b, c]</code> 는 값을 순서대로, 딕셔너리 <code>{\"키\": 값}</code> 는 이름표가 붙은 값을 담습니다. 카드 하나는 딕셔너리, 카드 목록은 리스트입니다."
   },
   "dom": {
    "h": "운전 조건과 단위조작",
    "b": "반응(반응기)·분리(증류탑) 같은 단위조작은 온도·압력·유량·환류비 같은 운전 변수로 조절합니다."
   },
   "lab": {
    "h": "공정 카드 읽기",
    "b": "<code>cards_data.py</code> 의 카드 20장은 각각 { 아이디·이름·분류·비용·즉시효과·부작용 } 딕셔너리입니다."
   },
   "code": {
    "cap": "운전 카드 한 장",
    "html": "{\n    <span class=\"s\">\"아이디\"</span>: <span class=\"s\">\"reactor_temp_up\"</span>,\n    <span class=\"s\">\"이름\"</span>: <span class=\"s\">\"반응기 온도 상승\"</span>,\n    <span class=\"s\">\"분류\"</span>: <span class=\"s\">\"운전\"</span>,\n    <span class=\"s\">\"비용\"</span>: <span class=\"n\">0</span>,\n    <span class=\"s\">\"즉시효과\"</span>: {<span class=\"s\">\"전환율\"</span>: <span class=\"n\">5</span>, <span class=\"s\">\"선택도\"</span>: -<span class=\"n\">3</span>},\n    <span class=\"s\">\"부작용\"</span>: {<span class=\"s\">\"안전지수\"</span>: -<span class=\"n\">5</span>},\n}"
   },
   "practice": [
    "<b>lab/examples/week02/</b> 를 번호 순서로 열기 - 한 파일에 개념 하나입니다",
    "cards_data.py 열기",
    "‘반응기 온도 상승’ 카드의 각 키 짚어보기",
    "즉시효과와 부작용이 어떻게 다른지 비교"
   ],
   "hw": "운전 카드와 연구(R&D) 카드의 구조 차이(즉시효과 vs 연구기간·성공효과)를 정리하세요.",
   "file": "server/app/cards/cards_data.py",
   "mno": "MODULE 01",
   "mtitle": "토대 - 공정·코드·화공의 첫 만남",
   "mspan": "1-3주",
   "l": "WEEK",
   "short": {
    "title": "리스트·딕셔너리 = 공정 카드의 구조",
    "py": "리스트, 딕셔너리(키-값)",
    "dom": "운전 조건과 단위조작(반응·분리)",
    "lab": "공정 카드가 데이터로 표현되는 방식 읽기",
    "stat": "",
    "exam": ""
   },
   "explain": "운전·설비·R&D 카드 20장이 { 비용·효과·부작용 } 딕셔너리 목록으로 정의된 파일"
  },
  {
   "w": 3,
   "track": "토대",
   "title": "첫 공정 카드 만들기",
   "goal": "딕셔너리를 직접 편집해 새 카드를 만들고 검사한다.",
   "py": {
    "h": "복사·수정·검사",
    "b": "기존 블록을 복사해 값만 바꾸면 새 카드가 됩니다. 오타·누락은 검사기가 한국어로 알려줍니다."
   },
   "dom": {
    "h": "운전 변수의 선택",
    "b": "온도·압력·유량·환류비 중 무엇을 건드릴지에 따라 수율·순도·안전·비용이 달라집니다."
   },
   "lab": {
    "h": "검사기로 확인",
    "b": "카드를 추가한 뒤 <code>python cards_data.py</code> 를 실행하면 <code>validate()</code> 가 오류·경고를 알려줍니다."
   },
   "code": {
    "cap": "새 카드 추가 + 검사",
    "html": "{\n    <span class=\"s\">\"아이디\"</span>: <span class=\"s\">\"catalyst_boost\"</span>,\n    <span class=\"s\">\"이름\"</span>: <span class=\"s\">\"촉매 추가 투입\"</span>,\n    <span class=\"s\">\"분류\"</span>: <span class=\"s\">\"운전\"</span>,\n    <span class=\"s\">\"비용\"</span>: <span class=\"n\">3</span>,\n    <span class=\"s\">\"즉시효과\"</span>: {<span class=\"s\">\"전환율\"</span>: <span class=\"n\">4</span>, <span class=\"s\">\"촉매비\"</span>: <span class=\"n\">2</span>},\n},\n<span class=\"c\"># 실행:  python cards_data.py  →  OK 완벽합니다!</span>"
   },
   "practice": [
    "<b>lab/examples/week03/</b> 를 번호 순서로 열기 - 한 파일에 개념 하나입니다",
    "카드 블록 하나를 통째로 복사",
    "아이디·이름·비용·효과를 새로 바꾸기",
    "검사 실행 → 오류가 나면 메시지대로 고치기",
    "서버 재실행 후 게임에서 새 카드 확인"
   ],
   "hw": "자기만의 운전 카드 1개를 설계(이름·비용·효과·부작용)해 검사를 통과시켜 오세요.",
   "file": "cards_data.py + card_schema.py",
   "mno": "MODULE 01",
   "mtitle": "토대 - 공정·코드·화공의 첫 만남",
   "mspan": "1-3주",
   "l": "WEEK",
   "short": {
    "title": "첫 공정 카드 만들기",
    "py": "딕셔너리 편집 · 검사기 실행",
    "dom": "공정 변수(온도·압력·유량·환류비)의 선택",
    "lab": "나의 첫 운전 카드 작성 후 검사기로 확인",
    "stat": "",
    "exam": ""
   },
   "explain": "블록을 복사해 카드를 추가하고 validate()로 오타·누락을 점검하는 흐름"
  },
  {
   "w": 4,
   "track": "로직",
   "title": "조건문 = 예산·설비 제약",
   "goal": "if/elif/else로 ‘조건에 따라 다르게 동작’하는 코드를 읽는다.",
   "py": {
    "h": "조건문 if / elif / else",
    "b": "<code>if 조건:</code> 은 조건이 참일 때만 실행합니다. 비교연산자 <code>&lt;, &gt;=, ==</code> 로 조건을 만듭니다."
   },
   "dom": {
    "h": "운전 한계·안전 제약",
    "b": "모든 공정에는 안전·설비·예산의 한계가 있습니다. 가능한 운전과 불가능한 운전을 가르는 규칙이 조건문입니다."
   },
   "lab": {
    "h": "카드 시행 조건",
    "b": "<code>enact_card()</code> 는 예산이 충분한지, 이미 설치한 일회성 설비인지 <code>if</code> 로 판단해 시행 여부를 정합니다."
   },
   "code": {
    "cap": "enact_card() 조건부",
    "html": "<span class=\"k\">if</span> card.get(<span class=\"s\">\"일회성\"</span>) <span class=\"k\">and</span> 이미_설치됨:\n    <span class=\"k\">return</span> <span class=\"n\">False</span>, <span class=\"s\">\"이미 설치됨\"</span>\n<span class=\"k\">if</span> plant[<span class=\"s\">\"예산\"</span>] &lt; card[<span class=\"s\">\"비용\"</span>]:\n    <span class=\"k\">return</span> <span class=\"n\">False</span>, <span class=\"s\">\"예산이 부족합니다\"</span>"
   },
   "practice": [
    "<b>lab/examples/week04/</b> 를 번호 순서로 열기 - 한 파일에 개념 하나입니다",
    "enact_card() 코드를 천천히 읽기",
    "어떤 조건일 때 카드가 막히는지 찾기",
    "게임에서 예산을 다 쓴 뒤 비싼 설비를 눌러 메시지 확인"
   ],
   "hw": "‘예산이 부족하면 어떻게 되는가’를 코드 흐름으로 3줄 설명하세요.",
   "file": "process_engine.py › enact_card()",
   "mno": "MODULE 02",
   "mtitle": "로직 - 제약 속의 의사결정",
   "mspan": "4-8주",
   "l": "WEEK",
   "short": {
    "title": "조건문 = 예산·설비 제약",
    "py": "if / elif / else, 비교연산",
    "dom": "운전 한계 · 안전 제약하 의사결정",
    "lab": "예산 부족·일회성 설비 조건 코드 분석",
    "stat": "",
    "exam": ""
   },
   "explain": "예산이 충분한지, 이미 설치한 설비인지 if로 판단해 시행 여부를 정하는 부분"
  },
  {
   "w": 5,
   "track": "로직",
   "title": "반복문 = 턴(월)의 흐름",
   "goal": "for 반복으로 ‘여러 개를 하나씩’ 처리하는 법을 배운다.",
   "py": {
    "h": "반복문 for",
    "b": "<code>for x in 목록:</code> 은 목록의 값을 하나씩 꺼내 같은 일을 반복합니다. 효과를 하나씩 적용하거나, 설치된 설비를 모두 순회할 때 씁니다."
   },
   "dom": {
    "h": "시계열 운전·누적효과",
    "b": "설비 유지비·장기효과는 매 턴 누적됩니다. 시간에 따른 변화(동특성)를 이해해야 장기 수율을 예측합니다."
   },
   "lab": {
    "h": "효과 적용과 턴 종료",
    "b": "<code>apply_effect()</code> 는 효과를 <code>for</code> 로 하나씩 더하고, <code>end_turn()</code> 은 설치된 모든 설비의 유지비·장기효과를 순회합니다."
   },
   "code": {
    "cap": "apply_effect() 의 for",
    "html": "<span class=\"k\">for</span> indicator, change <span class=\"k\">in</span> effect.items():\n    plant[indicator] = plant[indicator] + change\n    <span class=\"k\">if</span> indicator <span class=\"k\">in</span> PERCENT_INDICATORS:\n        <span class=\"c\"># 0~100 범위로 묶기</span>\n        plant[indicator] = min(<span class=\"n\">100</span>, max(<span class=\"n\">0</span>, plant[indicator]))"
   },
   "practice": [
    "<b>lab/examples/week05/</b> 를 번호 순서로 열기 - 한 파일에 개념 하나입니다",
    "apply_effect()와 end_turn() 읽기",
    "효과가 ‘하나씩’ 더해지는 부분 찾기",
    "<b>합계와 개수로 평균 구하기</b> - for 로 더한 뒤 개수로 나눠 보기"
   ],
   "hw": "지표 한 개를 12턴 동안 받아 적고, for 문으로 합계와 평균을 구해 오세요. (아직 ‘통계’라는 말은 쓰지 않습니다)",
   "file": "process_engine.py › apply_effect() · end_turn()",
   "mno": "MODULE 02",
   "mtitle": "로직 - 제약 속의 의사결정",
   "mspan": "4-8주",
   "l": "WEEK",
   "short": {
    "title": "반복문 = 턴(월)의 흐름",
    "py": "for 반복, 누적 합",
    "dom": "시계열 운전 · 누적 효과 · 동특성",
    "lab": "턴마다 효과·유지비가 쌓이는 과정 추적",
    "stat": "",
    "exam": ""
   },
   "explain": "효과를 하나씩 더하고(for), 설치된 설비·진행 중 R&D를 순회하는 부분"
  },
  {
   "w": 6,
   "track": "로직",
   "title": "함수 = 수율 계산기",
   "goal": "def로 기능을 묶고, 수율 공식의 의미를 체득한다.",
   "py": {
    "h": "함수 def",
    "b": "함수는 입력(인자)을 받아 일을 하고 결과(반환값)를 돌려줍니다. <code>calculate_yield(plant)</code> 는 한 번 만들면 매 턴 재사용됩니다."
   },
   "dom": {
    "h": "수율 = 전환율 × 선택도 × 분리회수율",
    "b": "수율은 생산량이 아니라 <b>세 요소의 곱</b>입니다. 하나만 낮아도 전체 수율이 무너집니다 - 이 수업의 핵심 개념입니다."
   },
   "lab": {
    "h": "수율 공식",
    "b": "<code>calculate_yield()</code> 는 전환율·선택도·분리회수율로 수율을 계산해 돌려줍니다. 매 턴 자동으로 다시 계산됩니다."
   },
   "code": {
    "cap": "calculate_yield()",
    "html": "<span class=\"k\">def</span> <span class=\"n\">calculate_yield</span>(plant):\n    y = (plant[<span class=\"s\">\"전환율\"</span>] * plant[<span class=\"s\">\"선택도\"</span>]\n         * plant[<span class=\"s\">\"분리회수율\"</span>]) / <span class=\"n\">10000</span>\n    <span class=\"k\">return</span> round(min(<span class=\"n\">100</span>, max(<span class=\"n\">0</span>, y)), <span class=\"n\">1</span>)"
   },
   "practice": [
    "<b>lab/examples/week06/</b> 를 번호 순서로 열기 - 한 파일에 개념 하나입니다",
    "calculate_yield() 읽기",
    "전환율 80·선택도 90·회수율 95 일 때 수율을 손으로 계산",
    "게임에서 환류비 증가(회수율↑)로 수율 상승 확인",
    "<b>def average(numbers):</b> 를 직접 작성해 보기 - 11주에 다시 씁니다"
   ],
   "hw": "calculate_yield() 를 3줄로 설명하고, <b>average() 함수를 직접 만들어</b> 제출하세요.",
   "file": "process_engine.py › calculate_yield()",
   "mno": "MODULE 02",
   "mtitle": "로직 - 제약 속의 의사결정",
   "mspan": "4-8주",
   "l": "WEEK",
   "short": {
    "title": "함수 = 수율 계산기",
    "py": "def 함수, 인자·반환값",
    "dom": "수율 = 전환율 × 선택도 × 분리회수율",
    "lab": "세 요소를 바꿔 수율이 어떻게 달라지는지 실험",
    "stat": "",
    "exam": ""
   },
   "explain": "전환율·선택도·분리회수율로 수율을 계산해 돌려주는 핵심 함수"
  },
  {
   "track": "시스템",
   "title": "엔진 전체 읽기 - 한 달은 어떻게 계산되는가",
   "goal": "변수·리스트·조건문·반복문·함수 다섯 가지가 <b>한 달 안에서 어떻게 맞물리는지</b> 호출 흐름으로 따라간다.",
   "py": {
    "h": "모듈과 호출 흐름",
    "b": "프로그램은 함수가 함수를 부르며 굴러갑니다. <code>import</code> 로 다른 파일을 가져오고, 한 함수가 끝나면 <b>어디로 돌아가는지</b>를 따라 읽는 것이 코드 읽기의 전부입니다."
   },
   "dom": {
    "h": "공정 계통과 피드백 루프",
    "b": "환류비를 올리면 순도가 오르지만 재비열이 늘고, 에너지비가 늘면 이익이 줄어 설비 투자가 밀립니다. 이렇게 돌아오는 <b>피드백 루프</b>를 못 보면 조건 변경은 늘 예상 밖으로 갑니다."
   },
   "lab": {
    "h": "end_turn() 한 줄씩 따라가기",
    "b": "<code>end_turn()</code> → <code>calculate_yield()</code> → <code>calculate_revenue()</code> → 안전·환경 점검. 생산 실행 버튼 하나가 부르는 함수들을 순서대로 짚습니다."
   },
   "code": {
    "cap": "end_turn() 의 호출 순서",
    "html": "<span class=\"k\">def</span> <span class=\"n\">end_turn</span>(plant):\n    <span class=\"c\"># ① 가동 중인 설비의 유지비·열화  (반복문)</span>\n    <span class=\"k\">for</span> u <span class=\"k\">in</span> plant[<span class=\"s\">\"설비\"</span>]: ...\n    <span class=\"c\"># ② 수율 = 전환율 × 선택도 × 회수율  (함수)</span>\n    plant[<span class=\"s\">\"수율\"</span>] = calculate_yield(plant)\n    <span class=\"c\"># ③ 매출·이익 정산  (함수)</span>\n    plant[<span class=\"s\">\"이익\"</span>] = calculate_revenue(plant)\n    <span class=\"c\"># ④ 안전·환경 한계 확인  (조건문)</span>\n    check_safety(plant)"
   },
   "practice": [
    "<b>lab/examples/week07/</b> 를 번호 순서로 열기 - 한 파일에 개념 하나입니다",
    "end_turn() 을 열고 호출되는 함수 이름을 <b>순서대로</b> 적기",
    "calculate_yield() 안으로 들어가 어떤 변수를 쓰는지 표시하기",
    "게임에서 생산 실행을 누르고, 방금 적은 순서대로 지표가 바뀌는지 확인",
    "‘환류비↑ → 순도↑ → 에너지비↑ → 이익↓’ 루프를 그림으로 그리기"
   ],
   "hw": "생산 실행 한 번에 벌어지는 일을 <b>호출 순서도 1장</b>으로 그려 제출하세요. 피드백 루프 1개를 화살표로 표시하세요.",
   "file": "server/app/engine/process_engine.py › end_turn()",
   "explain": "생산 실행 버튼 하나가 유지비·수율·이익·안전을 차례로 처리하는 흐름 - 앞의 5주가 모두 여기서 만납니다",
   "w": 7,
   "l": "WEEK",
   "short": {
    "title": "엔진 전체 읽기 - 한 달은 어떻게 계산되는가",
    "py": "모듈과 호출 흐름",
    "dom": "공정 계통과 피드백 루프",
    "lab": "end_turn() 한 줄씩 따라가기",
    "stat": "",
    "exam": ""
   },
   "mno": "MODULE 02",
   "mtitle": "로직 - 제약 속의 의사결정",
   "mspan": "4-8주"
  },
  {
   "w": 8,
   "track": "평가",
   "exam": "중간고사(개념) + 중간 프로젝트: 카드 5종 설계 후 시뮬레이션 결과 발표 + <b>내 데이터셋 설명서 1쪽</b>",
   "title": "중간 점검 · 공정팩 설계 발표",
   "goal": "1~7주를 종합해 자신만의 공정 카드 5종을 설계하고 발표한다.",
   "py": {
    "h": "복습 체크",
    "b": "변수·리스트/딕셔너리·조건문·반복문·함수 - 다섯 가지 기초를 모두 사용해 공정팩을 만듭니다."
   },
   "dom": {
    "h": "공정 패키지",
    "b": "낱개 카드가 아니라 ‘수율 목표를 향한 공정 전략’을 설계합니다. 수율·순도·안전·비용의 균형을 고려합니다."
   },
   "lab": {
    "h": "중간 프로젝트",
    "b": "카드 5종을 작성·검사한 뒤 게임으로 12개월을 돌려 결과를 발표합니다."
   },
   "code": {
    "cap": "중간고사 + 발표",
    "html": "<span class=\"c\"># 제출물</span>\n<span class=\"c\"># 1) 카드 5종이 담긴 cards_data.py (검사 통과)</span>\n<span class=\"c\"># 2) 게임 12개월 운영 결과 스크린샷</span>\n<span class=\"c\"># 3) 설계 의도 1쪽 발표자료</span>"
   },
   "practice": [
    "<b>lab/examples/week08/</b> 를 번호 순서로 열기 - 한 파일에 개념 하나입니다",
    "1~7주 핵심 개념 복습",
    "카드 5종 설계·검사 통과",
    "게임 12개월 운영 → 등급 기록",
    "설계 의도·트레이드오프 발표",
    "이번 주부터 <b>모든 판을 저장하고 성공/실패 라벨</b> 붙이기"
   ],
   "hw": "이번 주부터 모든 판을 <b>저장하고 성공/실패 라벨</b>을 붙이세요. 9주부터 그 데이터를 씁니다.",
   "file": "cards_data.py + card_schema.py",
   "mno": "MODULE 02",
   "mtitle": "로직 - 제약 속의 의사결정",
   "mspan": "4-8주",
   "l": "EXAM",
   "short": {
    "title": "중간 점검 · 공정팩 설계 발표",
    "py": "",
    "dom": "",
    "lab": "",
    "stat": "",
    "exam": "중간고사(개념) + 중간 프로젝트: 카드 5종 설계 후 시뮬레이션 결과 발표 + <b>내 데이터셋 설명서 1쪽</b>"
   },
   "explain": "학생이 직접 만든 공정 카드팩이 검사기를 통과하는지 확인 후 게임으로 검증"
  },
  {
   "w": 9,
   "track": "데이터",
   "title": "같은 선택, 다른 결과 - 시드와 반복",
   "goal": "똑같이 해도 결과가 매번 다르다는 것을 확인하고, 시드로 그 차이를 다시 만들어 낸다.",
   "py": {
    "h": "모듈 불러오기와 반복 호출",
    "b": "다른 파일의 기능을 <code>import</code> 로 가져다 씁니다. 같은 함수를 <b>여러 번</b> 부르고 결과를 리스트에 모으면, 한 번으로는 안 보이던 것이 보입니다."
   },
   "dom": {
    "h": "공정 변동과 재현성",
    "b": "같은 레시피도 원료 로트·주변온도·계측기에 따라 결과가 달라집니다. <b>한 배치의 성공</b>으로 조건을 확정하는 것이 현장에서 가장 흔한 오류입니다."
   },
   "lab": {
    "h": "같은 전략, 시드 5개",
    "b": "<code>run_batch.py</code> 로 같은 운전 전략을 시드만 바꿔 5번 돌립니다. 최종 수율과 순도가 매번 다릅니다."
   },
   "code": {
    "cap": "시드를 바꿔 5번 돌리기",
    "html": "<span class=\"k\">from</span> run_batch <span class=\"k\">import</span> play\n\n결과 = []\n<span class=\"k\">for</span> seed <span class=\"k\">in</span> [<span class=\"n\">1</span>, <span class=\"n\">2</span>, <span class=\"n\">3</span>, <span class=\"n\">4</span>, <span class=\"n\">5</span>]:\n    결과.append(play(seed=seed))\n    <span class=\"c\"># 같은 전략인데 값이 매번 다릅니다</span>\n\n<span class=\"k\">print</span>(결과)"
   },
   "hw": "같은 전략을 시드 10개로 돌린 표(시드·결과)와 3문장 노트를 제출하세요.",
   "file": "server/app/engine/noise.py + lab/run_batch.py",
   "mno": "MODULE 03",
   "mtitle": "데이터 - 만들고 · 남기고 · 읽는다",
   "mspan": "9-12주",
   "l": "WEEK",
   "short": {
    "title": "같은 선택, 다른 결과 - 시드와 반복",
    "py": "모듈 불러오기와 반복 호출",
    "dom": "공정 변동과 재현성",
    "lab": "같은 전략, 시드 5개",
    "stat": "한 번은 아무것도 증명하지 않는다",
    "exam": ""
   },
   "explain": "시드에서 난수를 만들어 매 턴 값을 조금씩 흔드는 부분 - 저장·불러오기를 해도 같은 시드면 같은 결과가 나옵니다",
   "stat": {
    "h": "한 번은 아무것도 증명하지 않는다",
    "b": "같은 조건인데 결과가 흩어집니다. 이 <b>흩어짐</b>이 이번 학기 후반부의 주제입니다. 아직 계산은 하지 않고, 눈으로만 봅니다."
   },
   "steps": {
    "edit": "lab/examples/week09/ - 02_five_seeds.py 의 시드 목록을 바꿔 보기",
    "run": "VS Code 에서 <code>lab/examples/week09/</code> 의 파일을 번호 순서로 열고, <code># %%</code> 아래에서 <b>Shift+Enter</b><br>또는 터미널에서  <code>cd lab\\examples\\week09</code> → <code>python 01_….py</code><br>여러 판을 한꺼번에: <code>cd lab → python run_batch.py --strategy 균형형 --n 5</code>",
    "expect": "5줄이 나오는데 값이 모두 다릅니다. 표로 옮겨 적으세요.",
    "ask": "가장 큰 값과 가장 작은 값의 차이는 얼마인가요? 그 차이만큼 ‘운’이었다면, 한 번만 돌려 본 친구의 결론은 믿을 수 있을까요?"
   }
  },
  {
   "w": 10,
   "track": "데이터",
   "title": "데이터를 남긴다 - 저장 · 라벨 · CSV",
   "goal": "판을 이름 붙여 저장하고 성공/실패 라벨을 달아, 나중에 비교할 수 있는 데이터로 만든다.",
   "py": {
    "h": "파일과 경로",
    "b": "프로그램이 만든 값은 끄면 사라집니다. <b>파일로 써야</b> 남습니다. 저장하면 같은 이름의 CSV가 <code>lab\\data\\</code> 에 함께 생깁니다."
   },
   "dom": {
    "h": "배치기록과 추적성",
    "b": "기록되지 않은 배치는 없던 배치입니다. 무엇을·언제·어떤 기준으로 측정했는지가 곧 그 공정의 신뢰도입니다."
   },
   "lab": {
    "h": "판을 이름 붙여 저장",
    "b": "판마다 이름·<b>성공/실패 라벨</b>·메모를 남깁니다. 라벨 기준은 여러분이 정하고, 그 기준을 글로 적어야 합니다."
   },
   "code": {
    "cap": "저장하면 CSV가 함께 생깁니다",
    "html": "<span class=\"c\"># 게임 화면:  💾 저장 · 불러오기  →  이름 \"환경우선_1\" · 라벨 \"성공\"</span>\n\nlab/data/환경우선_1.csv   <span class=\"c\">← 같은 이름으로 자동 생성</span>\n\n<span class=\"c\"># 이름을 알아볼 수 있게 지으세요. 나중에 이 이름으로 찾습니다.</span>"
   },
   "hw": "성공 3판·실패 3판을 저장하고, 라벨 기준을 한 문장으로 정의해 제출하세요.",
   "file": "server/app/persistence.py + export_csv.py",
   "mno": "MODULE 03",
   "mtitle": "데이터 - 만들고 · 남기고 · 읽는다",
   "mspan": "9-12주",
   "l": "WEEK",
   "short": {
    "title": "데이터를 남긴다 - 저장 · 라벨 · CSV",
    "py": "파일과 경로",
    "dom": "배치기록과 추적성",
    "lab": "판을 이름 붙여 저장",
    "stat": "표본 하나 = 판 하나",
    "exam": ""
   },
   "explain": "판을 이름·라벨·메모와 함께 저장하고, 같은 이름의 CSV를 lab/data 에 함께 기록하는 부분",
   "stat": {
    "h": "표본 하나 = 판 하나",
    "b": "판을 20번 저장하면 표본이 20개입니다. 표본이 적으면 어떤 통계도 소용없습니다. <b>모으는 일이 먼저입니다.</b>"
   },
   "steps": {
    "edit": "lab/examples/week10/ - 01_write_csv.py · 02_read_csv.py",
    "run": "게임 → 💾 저장 · 불러오기 → 이름·라벨·메모 입력 → 저장 (서로 다른 판 6개 이상)<br>VS Code 에서 <code>lab/examples/week10/</code> 의 파일을 번호 순서로 열고, <code># %%</code> 아래에서 <b>Shift+Enter</b><br>또는 터미널에서  <code>cd lab\\examples\\week10</code> → <code>python 01_….py</code>",
    "expect": "lab\\data\\ 폴더에 내가 지은 이름 그대로 CSV가 쌓입니다.",
    "ask": "라벨을 ‘성공’으로 정한 기준은 무엇이었나요? 그 기준을 남이 읽고 똑같이 나눌 수 있나요?"
   }
  },
  {
   "w": 11,
   "track": "데이터",
   "title": "엑셀로 읽는 숫자",
   "goal": "내가 만든 CSV를 엑셀로 열어 평균·표준편차를 구하고, 라벨별로 집계한다.",
   "py": {
    "h": "CSV는 그냥 글자입니다 · VS Code 셀 실행",
    "b": "CSV를 <b>메모장</b>으로 열어 보세요. 쉼표로 나뉜 글자일 뿐입니다. 엑셀도 파이썬도 이 글자를 읽는 도구입니다.<br>이번 주부터 <code># %%</code> 를 씁니다 - 그 줄 아래가 한 덩어리가 되고 <b>Shift+Enter</b> 로 그 덩어리만 실행됩니다. <b>파일은 그대로 평범한 .py 입니다.</b>"
   },
   "dom": {
    "h": "운전일지와 집계",
    "b": "현장 일지도 결국 표 하나입니다. 평균만 보면 놓치는 것 - 흩어짐과 이상치를 함께 봅니다."
   },
   "lab": {
    "h": "판별 요약 CSV",
    "b": "한 줄이 한 판인 CSV를 엑셀로 열어, 라벨별 최종 수율·순도·안전지수를 집계합니다."
   },
   "code": {
    "cap": "엑셀 수식 (파이썬 아님)",
    "html": "<span class=\"c\"># 판별 요약 CSV 를 엑셀로 열고</span>\n=AVERAGE(B2:B21)     <span class=\"c\">← 평균</span>\n=STDEV.S(B2:B21)     <span class=\"c\">← 표준편차 (n-1로 나눔)</span>\n=MAX(B2:B21)-MIN(B2:B21)\n\n<span class=\"c\"># 삽입 → 피벗테이블 → 행: 라벨 / 값: 평균</span>"
   },
   "hw": "라벨별 평균·표준편차 표와 차트 1장을 엑셀 파일로 제출하세요.",
   "file": "lab/data/*.csv",
   "mno": "MODULE 03",
   "mtitle": "데이터 - 만들고 · 남기고 · 읽는다",
   "mspan": "9-12주",
   "l": "WEEK",
   "short": {
    "title": "엑셀로 읽는 숫자",
    "py": "CSV는 그냥 글자입니다 · VS Code 셀 실행",
    "dom": "운전일지와 집계",
    "lab": "판별 요약 CSV",
    "stat": "직접 만드는 다섯 값",
    "exam": ""
   },
   "explain": "게임이 내보낸 CSV - 한글이 깨지지 않도록 BOM(utf-8-sig)을 붙여 저장합니다",
   "stat": {
    "h": "직접 만드는 다섯 값",
    "b": "<code>AVERAGE</code>(평균) · <code>MEDIAN</code>(중앙값) · <code>STDEV.S</code>(표준편차) · <code>MAX</code> · <code>MIN</code>. 이 다섯은 <b>학생이 직접 구합니다.</b> 피벗으로 라벨별 평균도 냅니다."
   },
   "steps": {
    "edit": "고칠 파일 없음 - 엑셀에서 진행 (코드로 확인하려면 lab/examples/week11/)",
    "run": "게임 → 💾 저장·불러오기 → 📥 판별 요약 CSV → 엑셀에서 더블클릭",
    "expect": "한 줄이 한 판입니다. 한글 헤더가 깨지지 않습니다.",
    "ask": "성공 판과 실패 판의 평균 차이는 얼마인가요? 그 차이가 9주에 본 ‘흩어짐’보다 큰가요, 작은가요?"
   }
  },
  {
   "w": 12,
   "track": "데이터",
   "title": "파이썬으로 같은 값 만들기",
   "goal": "엑셀이 준 값을 코드로 다시 구해 <b>두 값이 같은지</b> 확인한다. 이 대조가 이번 학기의 핵심 장면이다.",
   "py": {
    "h": "csv 읽기 · for 합계 · 함수 채우기",
    "b": "<code>csv</code> 모듈로 파일을 읽고, <code>for</code> 로 합계를 구하고, 7주에 만든 <code>average()</code> 를 다시 씁니다. 빈 함수 3개를 채우면 끝입니다."
   },
   "dom": {
    "h": "물질수지를 스스로 검산",
    "b": "공정 데이터는 대개 DCS가 계산해 준 숫자로 옵니다. 산식을 직접 돌려 보는 사람만이 그 숫자를 의심할 수 있습니다."
   },
   "lab": {
    "h": "엑셀 값과 코드 값 대조",
    "b": "11주에 엑셀로 구한 값과 12주에 코드로 구한 값이 같아야 합니다. 다르면 <b>둘 중 하나가 틀린 것</b>입니다."
   },
   "code": {
    "cap": "w12_basic.py - 채워야 할 곳",
    "html": "<span class=\"k\">def</span> <span class=\"n\">my_mean</span>(values):\n    <span class=\"c\"># TODO: 합계 ÷ 개수</span>\n    <span class=\"k\">return</span> sum(values) / len(values)\n\n<span class=\"k\">def</span> <span class=\"n\">my_stdev</span>(values):\n    <span class=\"c\"># TODO: 편차의 제곱 평균 → 제곱근.  n 이 아니라 n-1 로 나눕니다</span>\n    m = my_mean(values)\n    변동 = sum((v - m) ** <span class=\"n\">2</span> <span class=\"k\">for</span> v <span class=\"k\">in</span> values) / (len(values) - <span class=\"n\">1</span>)\n    <span class=\"k\">return</span> 변동 ** <span class=\"n\">0.5</span>"
   },
   "hw": "엑셀 값과 코드 값을 나란히 놓은 표 + 그림 1장(<code>w12_chart.py</code>)을 제출하세요.",
   "file": "lab/w12_basic.py · lab/check.py · lab/w12_chart.py",
   "mno": "MODULE 03",
   "mtitle": "데이터 - 만들고 · 남기고 · 읽는다",
   "mspan": "9-12주",
   "l": "WEEK",
   "short": {
    "title": "파이썬으로 같은 값 만들기",
    "py": "csv 읽기 · for 합계 · 함수 채우기",
    "dom": "물질수지를 스스로 검산",
    "lab": "엑셀 값과 코드 값 대조",
    "stat": "평균 · 표준편차 · 변동계수",
    "exam": ""
   },
   "explain": "학생이 직접 채우는 실습 파일 - 채점기(check.py)가 무엇이 왜 틀렸는지 한국어로 알려 줍니다",
   "stat": {
    "h": "평균 · 표준편차 · 변동계수",
    "b": "표준편차는 <b>n이 아니라 n-1</b>로 나눕니다(자유도). 변동계수 = 표준편차 ÷ 평균 - 단위가 다른 두 지표 중 무엇이 더 불안정한지 비교할 때 씁니다."
   },
   "steps": {
    "edit": "lab/w12_basic.py - my_mean · my_stdev · my_cv 세 함수  (풀이 흐름은 lab/examples/week12/)",
    "run": "VS Code 터미널(Ctrl+`)에서  cd lab  →  python w12_basic.py  →  python check.py<br>값을 이리저리 바꿔 볼 때는 <code># %%</code> + Shift+Enter",
    "expect": "check.py 가 통과를 알려 주고, 틀리면 왜 틀렸는지 한국어로 말해 줍니다.",
    "ask": "엑셀의 STDEV.S 값과 내 코드의 값이 소수점까지 같나요? 다르다면 n으로 나눴는지 n-1로 나눴는지 확인하세요."
   }
  },
  {
   "w": 13,
   "track": "판단",
   "title": "분포를 읽는다 - 평균이 숨기는 것",
   "goal": "평균 하나로는 안 보이는 <b>치우침 · 퍼짐 · 튀는 값</b>을 도수분포표와 히스토그램으로 직접 만들어 본다.",
   "py": {
    "h": "구간을 나눠 세기",
    "b": "<code>for</code> 안에 <code>if</code> 를 넣어 값이 어느 구간에 드는지 세면 그것이 <b>도수분포표</b>입니다. 히스토그램은 그 표를 막대로 세운 것일 뿐입니다."
   },
   "dom": {
    "h": "평균이 규격을 보장하지 않는다",
    "b": "평균 순도가 98%여도 <b>퍼짐이 크면 규격 미달 배치가 나옵니다.</b> 현장에서 문제가 되는 것은 늘 평균이 아니라 <b>꼬리 쪽 몇 배치</b>입니다."
   },
   "lab": {
    "h": "내 공정 지표의 분포",
    "b": "12개월간의 수율·순도를 구간별로 세어 봅니다. 튄 배치가 있다면 그달에 무슨 조건을 바꿨는지 로그에서 찾습니다."
   },
   "code": {
    "cap": "도수분포표를 직접 만들기",
    "html": "구간 = {}\n<span class=\"k\">for</span> v <span class=\"k\">in</span> 값들:\n    칸 = <span class=\"k\">int</span>(v // <span class=\"n\">5</span>) * <span class=\"n\">5</span>      <span class=\"c\"># 5 단위로 묶기</span>\n    구간[칸] = 구간.get(칸, <span class=\"n\">0</span>) + <span class=\"n\">1</span>\n\n<span class=\"k\">for</span> 칸 <span class=\"k\">in</span> sorted(구간):\n    <span class=\"k\">print</span>(칸, <span class=\"s\">\"■\"</span> * 구간[칸], 구간[칸])"
   },
   "hw": "지표 하나의 도수분포표(내 코드) + 히스토그램 캡처(게임)를 나란히 놓고, 모양을 3문장으로 설명하세요.",
   "file": "lab/w12_basic.py · lab/w12_chart.py",
   "mno": "MODULE 04",
   "mtitle": "판단 - 분포를 읽고 두 무리를 견준다",
   "mspan": "13-15주",
   "l": "WEEK",
   "short": {
    "title": "분포를 읽는다 - 평균이 숨기는 것",
    "py": "구간을 나눠 세기",
    "dom": "평균이 규격을 보장하지 않는다",
    "lab": "내 공정 지표의 분포",
    "stat": "히스토그램 · 이상치 - 직접 만듭니다",
    "exam": ""
   },
   "explain": "구간을 나눠 세는 것이 도수분포표이고, 그것을 막대로 세운 것이 히스토그램입니다",
   "stat": {
    "h": "히스토그램 · 이상치 - 직접 만듭니다",
    "b": "평균이 같아도 모양은 전혀 다를 수 있습니다. <b>어디에 몰려 있는가</b>(봉우리), <b>한쪽으로 쏠렸는가</b>(치우침), <b>혼자 멀리 있는 값이 있는가</b>(이상치)를 봅니다. 이상치는 지우는 게 아니라 <b>왜 생겼는지 찾는 것</b>입니다."
   },
   "steps": {
    "edit": "lab/examples/week13/ - 01_histogram.py 의 histogram( )",
    "run": "VS Code 에서 <code>lab/examples/week13/</code> 의 파일을 번호 순서로 열고, <code># %%</code> 아래에서 <b>Shift+Enter</b><br>또는 터미널에서  <code>cd lab\\examples\\week13</code> → <code>python 01_….py</code><br>그림까지: <code>cd lab → python w12_chart.py</code>",
    "expect": "구간별 개수가 막대(■)로 찍힙니다. 게임의 📊 통계 지표 보기 히스토그램과 모양이 같아야 합니다.",
    "ask": "가장 높은 봉우리는 어느 구간인가요? 평균은 그 봉우리 안에 있나요, 아니면 벗어나 있나요? 벗어났다면 왜 그런가요?"
   }
  },
  {
   "w": 14,
   "track": "판단",
   "title": "두 무리 비교 - 성공과 실패는 무엇이 달랐나",
   "goal": "라벨을 붙인 판들을 두 무리로 나눠 <b>평균과 퍼짐을 함께</b> 견주고, 그 차이를 어디까지 말할 수 있는지 정한다.",
   "py": {
    "h": "리스트 두 개를 나란히",
    "b": "라벨로 값을 두 리스트에 나눠 담고, 12주에 만든 <code>my_mean()</code>·<code>my_stdev()</code> 를 <b>각각 한 번씩</b> 부르면 끝입니다. 새로 배울 문법이 없습니다."
   },
   "dom": {
    "h": "품질 판정 - 관리도와 공정능력",
    "b": "평균이 규격 안이어도 흩어짐이 크면 불량이 납니다. 관리도는 ‘변했는가’를, Cp·Cpk는 ‘규격을 감당하는가’를 봅니다. 둘 다 <b>평균과 표준편차</b>만으로 만들어집니다 - 새 통계가 아닙니다."
   },
   "lab": {
    "h": "성공 vs 실패 · 품질 탭",
    "b": "두 무리 비교와 함께, 순도 관리도(X̄-R)와 Cp·Cpk를 눌러서 봅니다. 관리도의 선은 <b>평균 ± 3×표준편차</b>일 뿐입니다."
   },
   "code": {
    "cap": "두 무리를 견주는 법 - 이게 전부입니다",
    "html": "성공 = [r[<span class=\"s\">\"최종_수율\"</span>] <span class=\"k\">for</span> r <span class=\"k\">in</span> 행들 <span class=\"k\">if</span> r[<span class=\"s\">\"라벨\"</span>] == <span class=\"s\">\"성공\"</span>]\n실패 = [r[<span class=\"s\">\"최종_수율\"</span>] <span class=\"k\">for</span> r <span class=\"k\">in</span> 행들 <span class=\"k\">if</span> r[<span class=\"s\">\"라벨\"</span>] == <span class=\"s\">\"실패\"</span>]\n\n차이 = my_mean(성공) - my_mean(실패)\n퍼짐 = (my_stdev(성공) + my_stdev(실패)) / <span class=\"n\">2</span>\n\n<span class=\"k\">print</span>(<span class=\"s\">\"평균 차이\"</span>, 차이)\n<span class=\"k\">print</span>(<span class=\"s\">\"퍼짐 대비\"</span>, 차이 / 퍼짐)   <span class=\"c\"># 1보다 크면 눈에 띄는 차이</span>"
   },
   "hw": "성공/실패 비교표 + 3문장 노트(수치·판단·<b>한계</b>). 한계가 비면 감점입니다.",
   "file": "lab/w12_basic.py + server/app/statistics_lab.py › compare_groups()",
   "mno": "MODULE 04",
   "mtitle": "판단 - 분포를 읽고 두 무리를 견준다",
   "mspan": "13-15주",
   "l": "WEEK",
   "short": {
    "title": "두 무리 비교 - 성공과 실패는 무엇이 달랐나",
    "py": "리스트 두 개를 나란히",
    "dom": "품질 판정 - 관리도와 공정능력",
    "lab": "성공 vs 실패 · 품질 탭",
    "stat": "차이를 퍼짐과 견준다 (+ 관리도)",
    "exam": ""
   },
   "explain": "두 무리의 평균과 퍼짐을 나란히 계산해, 그 차이를 어디까지 말할 수 있는지 보여 주는 부분",
   "stat": {
    "h": "차이를 퍼짐과 견준다 (+ 관리도)",
    "b": "평균 차이만 보지 않고 <b>차이 ÷ 표준편차</b>를 봅니다. 관리도의 관리선도 <b>평균 ± 3×표준편차</b>이고, Cp 도 <b>규격폭 ÷ (6×표준편차)</b>입니다 - 전부 12주에 만든 그 표준편차 하나에서 나옵니다."
   },
   "steps": {
    "edit": "lab/examples/week14/ - 01_split_by_label.py · 03_diff_over_spread.py",
    "run": "게임 → ⚖ 성공 vs 실패 비교  ·  그다음 VS Code 에서 <code>lab/examples/week14/</code> 의 파일을 번호 순서로 열고, <code># %%</code> 아래에서 <b>Shift+Enter</b><br>또는 터미널에서  <code>cd lab\\examples\\week14</code> → <code>python 01_….py</code>",
    "expect": "게임 화면의 평균 차이와 내 코드의 평균 차이가 같아야 합니다.",
    "ask": "차이 ÷ 퍼짐 이 1보다 큰 지표는 무엇인가요? 그리고 그 차이가 정말 <b>내 정책 때문</b>일까요, 아니면 <b>다른 것이 함께 바뀐 것</b>일까요?"
   }
  },
  {
   "w": 15,
   "track": "평가",
   "exam": "최종 검증 보고서 + 발표. <b>필수 3요소</b> - ① 내 데이터는 어떻게 만들어졌는가(시드·판 수·라벨 기준) ② 분포 그림 1장 ③ 불확실성 문장 1개. 셋 중 하나라도 없으면 발표 상한 70%.",
   "title": "보고서와 발표 - 내 데이터로 말하기",
   "goal": "내가 만든 데이터로 결론을 말하고, 그 결론이 틀릴 수 있는 지점까지 함께 발표한다.",
   "py": {
    "h": "내 코드로 다시 확인",
    "b": "12주에 채운 <code>w12_basic.py</code> 를 최종 데이터에 그대로 돌립니다. 발표에 쓰는 숫자는 <b>내 코드가 낸 숫자</b>여야 합니다."
   },
   "dom": {
    "h": "근거를 밝히는 엔지니어링",
    "b": "기술보고서의 신뢰는 결론이 아니라 <b>근거를 어디까지 밝혔는가</b>에서 옵니다. 측정 방법·배치 수·한계를 적지 않은 보고서는 채택되지 않습니다."
   },
   "lab": {
    "h": "최종 평가와 검증",
    "b": "최종 수율·순도·안전지수로 결과를 보되, 등급보다 <b>그 등급을 어떻게 얻었는지</b>를 검증합니다."
   },
   "code": {
    "cap": "발표에 반드시 들어가야 하는 것",
    "html": "<span class=\"c\"># ① 내 데이터는 어떻게 만들어졌는가</span>\n시드 = [<span class=\"n\">1</span>, <span class=\"n\">2</span>, <span class=\"n\">3</span>, ...]   판 수 = <span class=\"n\">20</span>   라벨 기준 = \"...\"\n\n<span class=\"c\"># ② 분포 그림 1장  (w12_chart.py)</span>\n<span class=\"c\"># ③ 불확실성 문장 1개</span>\n<span class=\"c\">#    \"표본이 20개라 이 차이는 우연일 수도 있습니다.\"</span>"
   },
   "practice": [
    "최종 데이터셋 확정 - 시드·판 수·라벨 기준을 문서에 적기",
    "<b>w12_basic.py</b> 로 최종 수치를 내 코드로 다시 계산",
    "분포 그림 1장 생성 (<b>w12_chart.py</b>)",
    "발표(7분) - 수치·판단·<b>한계</b> 순서로",
    "동료 발표에 질문하기 - “그 숫자, 어떻게 만들었나요?”"
   ],
   "hw": "최종 검증 보고서 제출 - 데이터 생성 방법 · 분포 그림 · 불확실성 문장 포함.",
   "file": "lab/data/*.csv + process_engine.py",
   "mno": "MODULE 04",
   "mtitle": "판단 - 분포를 읽고 두 무리를 견준다",
   "mspan": "13-15주",
   "l": "EXAM",
   "short": {
    "title": "보고서와 발표 - 내 데이터로 말하기",
    "py": "",
    "dom": "",
    "lab": "",
    "stat": "",
    "exam": "최종 검증 보고서 + 발표. <b>필수 3요소</b> - ① 내 데이터는 어떻게 만들어졌는가(시드·판 수·라벨 기준) ② 분포 그림 1장 ③ 불확실성 문장 1개. 셋 중 하나라도 없으면 발표 상한 70%."
   },
   "explain": "최종 수율·순도·안전 등급으로 결과를 평가하되, 등급보다 그 등급을 어떻게 얻었는지를 검증합니다",
   "stat": {
    "h": "세 문장으로 끝내기",
    "b": "<b>수치</b>(내가 본 값과 단위) · <b>판단</b>(그래서 무엇이라 결론짓는가) · <b>한계</b>(이 결론이 틀릴 수 있는 이유). 한계가 비면 감점입니다."
   }
  }
 ]
}
;
