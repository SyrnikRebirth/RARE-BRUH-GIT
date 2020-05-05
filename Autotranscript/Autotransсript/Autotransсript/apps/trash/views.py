from django.shortcuts import render
import speech_recognition as sr
import time
import sys
import threading
import pyperclip as pc
import pyautogui as pag
from time import gmtime, strftime
from django.contrib.auth.models import User
from . import docx_writer


def sample_view(request):
    current_user = request.user
    return current_user.username
def index(request):
    return render(request, 'trash123/create_page.html')

def output(request):
    condition_from_heavens = [False]
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
        f = open('srenogramma.txt', 'a')
        assert(f.closed==False)
        #Здесь должна быть реализована функция отправки сообщения на сервер к другим сообщениям
        print("send_sentence sends: " + punctuation_post_processing(string))
        text =str(strftime("%H:%M", gmtime()))+" "+punctuation_post_processing(string)
        print(str(request.user.username))
        f.write(str(request.user.username)+'\n')
        f.write(text+'\n')
        pc.copy(text)
        # pag.move(0,15, duration = 1)
        # pag.click()
        if text != "v":
            pag.hotkey('ctrl','v')
            pag.press('enter')

        # pag.move(0,-15, duration = 1)

    def recognize_audio(recognizer, stop_signal, queue):
        while not stop_signal.is_set():
            #Если есть необработанные аудиофайлы
            if(len(queue) != 0):
                try:
                    #Отправляем информацию в гугл для обработки
                    text = recognizer.recognize_google(queue.pop(0), language="ru-RU").lower()
                    if (text == "стоп земля"):
                        condition_from_heavens[0] = True
                    send_sentence(text)
                except:
                    pass
            time.sleep(1)


    recog_func = sr.Recognizer()
    mic = sr.Microphone()

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
        if condition_from_heavens[0]: break
        with mic as source:
            print("Пожалуйста говорите")
            audio = recog_func.listen(source, timeout = 10)
        queue_of_audio_data.append(audio)
        print("Началась обработка сообщения...")
    #Поднимаем стоп сигнал для служебного потока, чтобы он закончил свое выполнение
    stop_signal.set()
    #Мерджим потоки
    return render(request, 'trash123/create_page.html')
    thread_for_recognizer.join()

def download(request):
    print("download has been called")
    docx_writer.turn_txt_to_docx('srenogramma.txt')
    return render(request, 'user_window/u_window.html')
