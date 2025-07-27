# FastMCP 서버 배포 및 Cursor 등록 가이드

이 문서는 로컬 환경에서 `FastMCP` 서버를 실행하고, 이를 Cursor 에디터에 등록하여 자연어 DB 조회를 사용하는 전체 과정을 안내합니다.

---

## 🚀 1. FastMCP 서버 배포 (로컬 실행)

"배포"는 우리 컴퓨터에서 서버 프로그램을 실행시켜서 Cursor가 접속할 수 있도록 만드는 과정입니다.

1.  **터미널 열기**
    VS Code나 사용하시는 터미널을 엽니다.

2.  **프로젝트 폴더로 이동**
    `mcp-mysql-project` 폴더로 이동합니다.
    ```bash
    cd path/to/mcp-mysql-project
    ```

3.  **서버 실행**
    아래 명령어를 입력하여 `FastMCP` 서버를 시작합니다.
    ```bash
    uvicorn server.app.main:app --host 0.0.0.0 --port 8000
    ```
    -   서버가 정상적으로 실행되면 터미널에 아래와 같은 로그가 나타납니다.
    ```log
    INFO:     Uvicorn running on [http://0.0.0.0:8000](http://0.0.0.0:8000) (Press CTRL+C to quit)
    INFO:     Started server process [xxxx]
    INFO:     Waiting for application startup.
    FastMCP 서버가 시작되었습니다.
    데이터베이스 연결이 확인되었습니다.
    INFO:     Application startup complete.
    ```

4.  **서버 실행 상태 유지**
    **매우 중요합니다!** Cursor에서 사용하려면 **이 터미널 창을 끄지 않고 계속 실행된 상태로 두어야 합니다.** 이 터미널이 바로 우리의 MCP 서버 그 자체입니다.

---

## ⚙️ 2. Cursor에 MCP 등록하기

이제 실행된 서버를 Cursor가 인식하도록 `settings.json` 파일에 등록할 차례입니다.

1.  **`settings.json` 열기**
    Cursor에서 **명령 팔레트(Command Palette)**를 엽니다.
    -   Windows/Linux: `Ctrl + Shift + P`
    -   macOS: `Cmd + Shift + P`

2.  열린 입력창에 `settings`라고 검색한 후, **`기본 설정: 사용자 설정 열기 (JSON)` (Preferences: Open User Settings (JSON))**를 선택합니다.

3.  **MCP 정보 추가**
    `settings.json` 파일이 열리면, JSON의 최상위 레벨에 아래의 `cursor.contexts` 항목을 추가합니다. (만약 항목이 이미 있다면 배열 `[]` 안에 객체 `{}`를 추가합니다.)

    ```json
    {
      // ... 다른 설정들 ...

      "cursor.contexts": [
        {
          "name": "MySQL-QA",
          "command": "curl -s -X POST -H \"Content-Type: application/json\" -d '{\"query\": \"{{query}}\"}' [http://127.0.0.1:8000/query](http://127.0.0.1:8000/query)",
          "description": "로컬 MySQL DB에 자연어로 질문합니다."
        }
      ]

      // ... 다른 설정들 ...
    }
    ```
    -   **`name`**: `@`를 입력했을 때 표시될 이름입니다. (예: `@My-DB`, `@Local-MySQL`)
    -   **`command`**: Cursor가 우리 서버와 통신하는 방법입니다. `curl`을 이용해 우리가 만든 `http://127.0.0.1:8000/query` 엔드포인트로 사용자의 질문(`{{query}}`)을 보내는 명령어입니다.
    -   **`description`**: 해당 컨텍스트에 대한 간단한 설명입니다.

4.  **저장**
    `settings.json` 파일을 저장하면 **즉시 Cursor에 적용됩니다.**

---

## ✅ 3. 사용 방법 및 확인

모든 설정이 완료되었습니다. 이제 직접 사용해 보세요.

1.  **FastMCP 서버가 터미널에서 계속 실행 중인지 확인**합니다.

2.  Cursor의 채팅 패널이나 코드 에디터 내의 채팅창을 엽니다.

3.  채팅 입력창에 **`@`**를 입력하면, 방금 우리가 등록한 **`@MySQL-QA`**가 목록에 나타납니다.

4.  `@MySQL-QA`를 선택한 후, 한 칸 띄고 데이터베이스에 하고 싶은 질문을 자연어로 입력합니다.
    > `@MySQL-QA 30살 이상인 유저의 이름과 이메일은 뭐야?`

5.  엔터를 누르면 Cursor가 `settings.json`에 정의된 `command`를 실행하여 우리 `FastMCP` 서버에 요청을 보냅니다. 서버는 AI를 통해 받은 질문을 SQL로 변환하고, DB에서 결과를 가져와 Cursor에 최종 답변을 보여주게 됩니다.
