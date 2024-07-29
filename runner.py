from gui import WebUI
import argparse

def main():
    # ArgumentParser 객체 생성
    parser = argparse.ArgumentParser(description='수동 Tagging 프로그램')

    # Args
    parser.add_argument('--inputs','-i', type=str,default="./inputs",help='이미지 파일 디렉토리 경로')
    parser.add_argument('--outputs','-o', type=str,default="./outputs",help='저장 디렉토리 경로')
    parser.add_argument('--default','-d', type=str,default="./default.xlsx" ,help='기본 태그 파일 디렉토리 경로')
    parser.add_argument('--server_name','-sn', type=str,default="127.0.0.1" ,help='gradio 서버 호스트 이름')
    parser.add_argument('--server_port','-sp', type=int,default=7861 ,help='gradio 서버 포트')
    parser.add_argument('--share','-s', type=bool,default=False ,help='gradio 서버 share')

    # 인자 파싱
    args = parser.parse_args()

    WebUI(
        img_path=args.inputs,
        save_path=args.outputs,
        default_tag_path=args.default
    ).run({
        "server_name":args.server_name,
        "server_port":args.server_port,
        "share":args.share
    })

if __name__ == "__main__":
    main()