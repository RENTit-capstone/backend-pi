# About
*FastAPI*로 구성된 Python 서버입니다.

Raspberry PI에서 동작할 것을 염두로 개발하고 있고, 프론트엔드에서 신호를 받아와 *gpiozero*를 이용하여 GPIO를 제어합니다.

그리고 RabbitMQ 와 *asyncio-mqtt*를 이용해서 통신합니다.

# How to start?
아래의 스크립트를 실행하세요:
```sh
source ./run.sh
```
...그러면 자동으로...:
1. 가상 환경(venv)을 체크하고 생성합니다.
2. 시작하기 위해 필요한 모든 라이브러리를 다운합니다.
3. FastAPI 서버를 실행합니다.
