import speech_recognition as sr
import time
import sys
import threading

def receive_stop_signal(signal):
    if (signal == True):
        return True
    else:
        return False

def send_sentence(string):
    #Здесь должна быть реализована функция отправки сообщения на сервер к другим сообщениям
    print("send_sentence sends: " + string)

def recognize_audio(recognizer, stop_signal, queue):
    while not stop_signal.is_set():
        #Если есть необработанные аудиофайлы
        if(len(queue) != 0):
            try:
                #Отправляем информацию в гугл для обработки
                text = recognizer.recognize_google(queue.pop(0), language="ru-RU").lower()
                send_sentence(text)
            except:
                pass
        time.sleep(1)

def main():
    recog_func = sr.Recognizer()
    mic = sr.Microphone()

    condition_from_heavens = True

    queue_of_audio_data = []

    #В течении 5ти секунд программа распознает уровень фонового шума
    with mic as source:
        recog_func.adjust_for_ambient_noise(source, duration = 5)

    #Создаем сигнал для остановки служебного потока
    stop_signal = threading.Event()
    #Создали служебный поток для обработки звуковых данных
    thread_for_recognizer = threading.Thread(target=recognize_audio,
        args=(recog_func, stop_signal, queue_of_audio_data),
        daemon=True)
    #Запускаем служебный поток
    thread_for_recognizer.start()

    #Основное тело программы, которое считывает информацию с микрофона до тех пор пока не придет сигнал остановки
    while True:
        with mic as source:
            print("Пожалуйста говорите")
            audio = recog_func.listen(source, timeout = 2)
        queue_of_audio_data.append(audio)
        print("Началась обработка сообщения...")
        if receive_stop_signal(condition_from_heavens): break
    #Поднимаем стоп сигнал для служебного потока, чтобы он закончил свое выполнение
    stop_signal.set()
    #Мерджим потоки
    thread_for_recognizer.join()

if __name__ == "__main__":
    main()
