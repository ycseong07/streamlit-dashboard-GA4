# streamlit-dashboard-GA4

데이터야 놀자 2023 'Streamlit으로 활용 가능한 대시보드 만들기' 자료 공유를 위한 저장소입니다.  

Visual Studio Code에서 Docker Container를 띄워 관리할 수 있도록 구성해두기는 했지만, 데이터와 ga4_dashboard.py 파일만 다운받아 본인의 파이썬 환경에서 실행하셔도 무방합니다.

![ga4-dashboard](https://github.com/ycseong07/streamlit-dashboard-GA4/assets/48194852/52abd8f8-f43b-428e-b73a-909a09a6876f)

## VSCode, Docker를 이용해 열기
- Visual Studio Code, Docker

1. Repository를 클론 받아주세요.
2. VSCode를 실행해 Extensions 중 Dev Containers를 설치합니다.
3. Cmd(Control) + Shift + p -> `Dev Containers: Open Folder in Container...` 를 선택합니다.
4. 클론받은 폴더를 선택해주세요
5. 컨테이너를 재시작하고 싶을 경우 `Dev Containers: Reopen in containers` 를 선택합니다.
6. `streamlit run ga4_dashboard.py` 명령어를 입력합니다.

## 참고
Mac, Linux에서 작업하실 경우 본 레포를 그대로 클론받아 쓰셔도 되지만, Windows의 경우 .streamlit 폴더를 `%userprofile%/.streamlit/` 처럼 위치시켜주셔야 합니다. ([관련링크](https://docs.streamlit.io/library/advanced-features/configuration#set-configuration-options))
