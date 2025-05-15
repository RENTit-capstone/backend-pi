from gpiozero import Servo, DigitalInputDevice
import time

# 사용할 GPIO 핀 번호 설정 (예: 17번 핀)
SERVO_PIN = 17
REED_PIN = 27

# Servo 객체 생성 (GPIOZero는 -1.0 ~ 1.0 사이 값 사용)
servo = Servo(SERVO_PIN)

# 중앙(0도) 위치로 이동
print("서보모터를 0도(중앙) 위치로 이동합니다.")
servo.value = 0.0

# 모터 위치 설정 후 잠깐 대기
time.sleep(0.5)

# 서보모터 해제 (선택 사항, 전력 소모 줄이기 위해)
servo.detach()
print("초기화 완료. 서보모터 연결 해제됨.")


reed = DigitalInputDevice(REED_PIN, pull_up=False)
reed_val = reed.value

print("리드 스위치 상태: {reed_val}")