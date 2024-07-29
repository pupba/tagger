import logging
import sys
# 로거 설정
logging.basicConfig(
    filename='./log/error.log',  # 로그 파일 이름
    level=logging.ERROR,  # 로그 레벨 설정
    format='%(asctime)s - %(levelname)s - %(message)s'  # 로그 포맷
)