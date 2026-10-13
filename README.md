# 📄 MarkToHTML (마크다운 웹 뷰어 & HTML 변환기)

PySide6 및 크로미움 웹엔진(`QWebEngineView`) 기반의 **마크다운(MD) to HTML 실시간 뷰어 및 변환 프로그램**입니다.

---

## 🌟 주요 기능

1. **좌측 파일 탐색기 (`FileExplorerWidget`)**
   - 원하는 폴더 선택 (`Ctrl+O`) 및 트리 구조 탐색
   - 마크다운(`.md`, `.markdown`, `.txt`) 파일 필터링 지원
   - 실시간 파일 검색창 지원
   - 외부 파일/폴더 드래그 앤 드롭 지원
   - 방향키(↑/↓) 또는 클릭 시 즉시 우측 화면에 변환 표시

2. **우측 웹 렌더러 & 원본 에디터 (`WebPreviewerWidget`)**
   - **QWebEngineView** 탑재: 실제 웹 브라우저와 동일한 렌더링 품질
   - **⚙️ 스타일 사용자 지정 (`style_config.json`)**: 상단 **[⚙️ 설정]** 버튼을 눌러 마크다운 문법별 글자 크기(H1~H6) 및 색상(제목, 볼드체, 인라인 코드 등)을 자유롭게 변경 가능
   - **✏️ 원본 마크다운 편집 & 저장**: 상단 **[편집]** 버튼(`Ctrl+E`)을 누르면 즉시 마크다운 소스 편집 모드로 전환되며, 버튼이 **[저장]**으로 변경되어 수정 후 파일에 바로 저장 가능
   - **모던 테마 8종**: `Modern Charcoal (모던 차콜)`, `Light Modern (라이트 모던)`, `Dracula (드라큘라)`, `Nord (노르드)`, `Solarized Light (솔라라이즈드)`, `GitHub Dark`, `GitHub Light`, `Notion Style`
   - **코드 신택스 하이라이트**: Python, JS, HTML, SQL 등 구문 강조 자동 적용
   - **테이블 & 체크리스트**: GFM 서식 완벽 지원

3. **출력 및 편의 기능**
   - **⚙️ 스타일 설정 열기**: `style_config.json`을 열어 글자 크기 및 색상 즉시 편집
   - **✏️ MD 편집 / 💾 저장 (`Ctrl+E` / `Ctrl+S`)**: 마크다운 파일 직접 수정 및 즉시 저장
   - **💾 HTML로 저장**: 스타일시트와 코드 테마가 내장된 단독 실행 HTML 파일로 내보내기
   - **🌐 브라우저에서 열기 (`Ctrl+B`)**: 기본 웹 브라우저(Edge, Chrome 등)로 1초 만에 확인
   - **📋 HTML 복사**: 클립보드에 HTML 소스 코드 즉시 복사
   - **🔄 새로고침 (`F5` / `Ctrl+R`)**: 수정된 원본 파일 및 변경된 스타일 설정 즉시 재렌더링

---

## 🚀 실행 및 배포 방법

### 1. 개발/일상 실행
가상환경 활성화 후 실행하거나 **`run.bat`** 파일을 실행합니다:
```bash
python main.py
```

### 2. 독립 실행 파일 (.exe) 빌드
**`build_exe.bat`** 파일을 실행하면 자동으로 PyInstaller를 통해 독립 실행 프로그램이 빌드됩니다.
* 빌드 완료 위치: `dist/MarkToHTML.exe` (단일 실행 파일)
* **배포 방법**: 소스 코드에는 포함되지 않으며, 빌드된 `MarkToHTML.exe` 파일을 GitHub Releases에 업로드하여 배포합니다.

---

## ⌨️ 단축키 안내
* **`Ctrl + E`**: 마크다운 원본 편집 / 미리보기 전환
* **`Ctrl + S`**: 편집 중일 때는 마크다운 원본 저장, 미리보기 중일 때는 HTML 내보내기
* **`Esc`**: 편집 취소 (미리보기 화면으로 복귀)
* **`Ctrl + O`**: 탐색할 폴더 열기
* **`Ctrl + B`**: 기본 웹 브라우저에서 열기
* **`F5` / `Ctrl + R`**: 파일 목록 및 문서 새로고침

---

## 📁 프로젝트 구조
```text
mark-to-html/
├── main.py              # 프로그램 진입점 (Entry Point)
├── main_window.py       # 메인 윈도우 (좌우 분할 스플리터)
├── explorer.py          # 좌측 파일 탐색창 (트리 뷰 + 검색 + 필터)
├── previewer.py         # 우측 웹 프리뷰어 (QWebEngineView + 툴바)
├── converter.py         # Markdown -> Standalone HTML 변환 코어
├── config_manager.py    # 사용자 스타일 설정 매니저
├── styles.py            # 앱 다크 테마 QSS 스타일시트
├── style_config.json    # 사용자 커스텀 스타일 설정
├── requirements.txt     # 프로젝트 의존성 라이브러리 목록
├── run.bat              # 파이썬 실행 배치 파일
└── build_exe.bat        # 독립형 .exe 빌드 자동화 스크립트
```
