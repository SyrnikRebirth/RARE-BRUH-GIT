from django.shortcuts import render
import speech_recognition as sr
import time
import sys
import threading



def index(request):
    return render(request, 'trash123/create_page.html')

def output(request):

    def receive_stop_signal(signal):
        if (signal == True):
            return True
        else:
            return False

    def punctuation_post_processing(string):
        output_string = string
        massive1 = ["здравствуйте ", " итак "]
        massive2 = [" что ", " как ", " когда",
                    " но ", " где ", " а ", " котор",
                    " потому что ", " так как ", " зато ",
                    " чей", " как будто ", " сколько", " зачем ", " если "]
        for matching_word in massive1:
            index = output_string.find(matching_word)
            while (index != -1):
                output_string = output_string[:index + len(matching_word) - 1] + "," + output_string[index + len(matching_word) - 1:]
                index = output_string.find(matching_word, index + len(matching_word))
        for matching_word in massive2:
            index = output_string.find(matching_word)
            while (index != -1):
                output_string = output_string[:index] + "," + output_string[index:]
                index = output_string.find(matching_word, index + 2)
        return output_string

    def send_sentence(string):
        #Здесь должна быть реализована функция отправки сообщения на сервер к другим сообщениям
        print("send_sentence sends: " + punctuation_post_processing(string))

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


    recog_func = sr.Recognizer()
    mic = sr.Microphone()

    condition_from_heavens = False

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
    return render(request, 'trash123/create_page.html')
