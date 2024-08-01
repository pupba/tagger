# 수동 Tagger
## demo
<img src="./demo.webp" width="auto"><br>

## 실행
- python3 설치
- ``git clone https://github.com/pupba/tagger.git``
### Linux & mac
- ``chmod +x run.sh``
- ``./run.sh``
- Args
    ```
    Usage: ./run.sh -i inputs -o outputs [options]...

    -h                   show this help
    -i input-path        이미지 파일 디렉토리 경로 (기본값: ./inputs)
    -o output-path       저장 디렉토리 경로 (기본값: ./outputs)
    -d default-path      기본 태그 파일 디렉토리 경로 (기본값: ./default.xlsx)
    -sn server-name      Gradio 서버 호스트 이름 (기본값: 127.0.0.1)
    -sp server-port      Gradio 서버 포트 (기본값: 7861)
    -s                   Gradio 서버 공유 모드 활성화 (기본값: False)
    ```
### other
- ``pip install requirements.txt``
- ``python runner.py``
- Args
    ```
    Usage: runner.py -i inputs -o outputs [options]...

    -h                   show this help
    -i input-path        이미지 파일 디렉토리 경로 (기본값: ./inputs)
    -o output-path       저장 디렉토리 경로 (기본값: ./outputs)
    -d default-path      기본 태그 파일 디렉토리 경로 (기본값: ./default.xlsx)
    -sn server-name      Gradio 서버 호스트 이름 (기본값: 127.0.0.1)
    -sp server-port      Gradio 서버 포트 (기본값: 7861)
    -s                   Gradio 서버 공유 모드 활성화 (기본값: False)
    ```

### ✅ v0.1.2 Update
- 실행전에 라이브러리 수정
- `venv/lib/python3.11/site-packages/transformers/dynamic_module_utils.py`
- 여기서 다음과 같이 수정(`input` 부분 주석 후 `answer = "yes"`)

<img src="./fix.webp" width="auto"><br> 