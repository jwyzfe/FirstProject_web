import pyautogui
import keyboard
import time

# PyAutoGUI 안전 설정
pyautogui.FAILSAFE = True  # 마우스를 화면 모서리로 이동하면 프로그램이 중지됨

def main():
    print("자동 클릭 프로그램 시작")
    print("마우스를 클릭할 위치에 놓으세요.")
    print("프로그램을 종료하려면 'q' 키를 누르세요.")

    # 3초 대기 (사용자가 마우스 위치를 조정할 시간 제공)
    for i in range(3, 0, -1):
        print(f"{i}초 후 클릭을 시작합니다...")
        time.sleep(1)

    click_count = 0  # 클릭 횟수 카운트

    try:
        while True:  # 무한 루프
            if keyboard.is_pressed('q'):  # 'q' 키로 종료
                print(f"\n프로그램 종료. 총 {click_count}번 클릭했습니다.")
                break

            pyautogui.click()  # 현재 마우스 위치에서 클릭
            click_count += 1
            print(f"클릭 횟수: {click_count}", end='\r')

            time.sleep(0.1)  # 클릭 간격 (0.1초, 필요 시 조정 가능)

    except Exception as e:
        print(f"\n오류 발생: {e}")
    finally:
        print("\n자동 클릭 프로그램이 종료되었습니다.")

if __name__ == "__main__":
    main()