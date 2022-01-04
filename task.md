Лабораторная работа
Цели
Понять, как ведут себя io bound операции в потоках и процессах в python
Понять, как ведут себя cpu bound операции в потоках и процессах в python
Сравнить время выполнения реализованных программ

Задания
Шаблон отчета — https://docs.google.com/document/d/10hgfMpYGmbykLBHSZ90gQBeJ-w_Qwj4F/edit
В задании нужно дополнить файлы:


io_ops/in_proc.py
io_ops/in_threads.py
io_ops/seq.py
cpu_ops/in_proc.py
cpu_ops/in_threads.py
cpu_ops/seq.py
Для запуска нужно открыть терминал:


В терминале запустить скрипт. Например:


python3 io_ops/in_proc.py
Все необходимые зависимости для выполнения задания уже установлены, их можно посмотреть в файле requirements.txt

IO bound операции
Задание 1. Последовательные запросы.
Файл io_ops/seq.py
Сделать 10 синхронных запросов на сайт https://api.covidtracking.com/v1/us/current.json. Для запросов использовать библиотеку requests. Время выполнения приложите к отчету.

Задание 2. Запросы в тредах
Файл io_ops/in_threads.py
Сделать 10 запросов на сайт https://api.covidtracking.com/v1/us/current.json в разных тредах. Для запросов использовать библиотеку requests. Время выполнения приложите к отчету.

Задание 3. Запросы в процессах
Файл io_ops/in_proc.py
Сделать 10 запросов на сайт https://api.covidtracking.com/v1/us/current.json в разных процессах. Для запросов использовать библиотеку requests. Время выполнения приложите к отчету.

Выводы из заданий 1-3
Напишите выводы после выполнения заданий. В выводе нужно: 
ответить, выполняются ли параллельно io bound операции в потоках/процессах
обосновать, почему они выполняются или не выполняются параллельно

CPU bound операции
Функция, которую будем использовать в заданиях, связанных с cpu bound операциями:

def countdown():
    i = 0
    begin = time.time()
    while i < 5_000_000:
        i += 1
    print(f"duration: {time.time() - begin}")


Задание 4. Синхронное выполнение
Файл cpu_ops/seq.py
10 раз синхронно вызвать функцию countdown(). Время выполнения и код программы приложите к отчету.

Задание 5. Выполнение в тредах
Файл cpu_ops/in_threads.py
Вызвать функцию countdown() в 10 разных тредах. Время выполнения приложите к отчету.

Задание 6. Выполнение в процессах
Файл cpu_ops/in_proc.py
Вызвать функцию countdown() в 10 разных процессах. Время выполнения приложите к отчету.

Выводы из заданий 4-6
Напишите выводы после выполнения заданий. В выводе нужно: 
ответить, выполняются ли параллельно cpu bound операции в потоках/процессах
обосновать, почему они выполняются или не выполняются параллельно





Введение 
Django — синхронный framework: 1 запущенный процесс django будет обрабатывать одного клиента.
Это неплохо, если мы выполняем CPU bound операции. Мы занимаем вычислительную мощность процессора и под эту операцию выделяем отдельный процесс. Но это неэффективно, если выполнять блокирующие IO bound операции. Процесс/поток будет заблокирован на все время ожидания операции.
Чтобы обслужить больше одного клиента одновременно, нужно запустить дополнительные процессы. Получается, что максимальное количество одновременно обслуживаемых клиентов будет равно количеству одновременно запущенных процессов. При этом процессы в большинстве случаев будут ожидать, когда выполнится IO-операция и ничего не делать, а процессор будет тратить ресурсы на переключение между «спящими» процессами.
Большинство монолитных приложений на Django работают только с БД. Зачастую база данных находится на том же сервере, и все запросы к ней выполняются быстро. Но если увеличивается время выполнения запросов к БД, или добавляется логика обращения к другим микросервисам, то производительность и эффективность утилизации ресурсов драматически падает.
В ситуации, когда приложение в основном ожидает выполнения IO bound операций (выполнения запроса в базу или ответа другого микросервиса), подойдет асинхронное программирование и асинхронные фреймворки — например, aiohttp.
Давайте посмотрим, в каких случаях асинхронный подход приносит пользу.

Микросервисная архитектура. Используется микросервисный подход. Для формирования ответа пользователю нужно выполнить много обращений к другим микросервисам.

Задачи доставки информации в реальном времени. Например, уведомления или чаты.
Для реализации таких задач используется технология web socket. Клиент открывает соединение и ждет, когда сервер пришлет новое сообщение или уведомление. В случае с синхронным подходом каждому клиенту нужно выделять отдельный поток/процесс, даже если он не получает сообщений. При таком подходе один сервер может обрабатывать тысячи соединений, а при асинхронном подходе десятки или сотни тысяч.

Стриминговая загрузка. Например, в s3-хранилище.
Обычный синхронный подход для загрузки файлов — получить весь файл, затем отправить его дальше в s3-хранилище. Такой подход удовлетворительно работает, когда размеры файлов сравнительно небольшие: 10-100 Мб. Но если файл весит гигабайты, использовать веб-сервер как буфер будет плохой идеей. 
Решение проблемы загрузки больших файлов — сразу отправлять полученные данные дальше в пункт назначения, то есть «стримить». Aiohttp позволяет эффективно решать такую задачу и параллельно обрабатывать других клиентов.

Сравним aiohttp и Django
Мы не будем сравнивать rps, в этом нет никакого смысла. Внутри django много написанных модулей, которые замедляют ее работу, но позволяют программистам быстрее писать код. В aiohttp на старте такого нет, и уже поэтому он будет быстрее.
Поэтому мы:
Сравним динамику изменения rps при увеличении числа параллельных запросов
Сравним динамику изменения rps при увеличении времени aiobound-операции
Посмотрим, как деградирует производительность асинхронного сервера aiohttp при использовании синхронных операций.
Для выполнения практики нам понадобится mercury из предыдущей лабораторной работы.

Для сравнения будем использовать 2 функции из aiohttp и django соответственно:
aiohttp, функция handle

# servers/aio/server.py

import asyncio
import time

from aiohttp import web


async def handle(request):
    await asyncio.sleep(0.2)
    return web.Response(text='Hello, Anonymous')

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])

if __name__ == '__main__':
    web.run_app(app, port=8088, host='0.0.0.0')


django, функция index

# servers/dj/dj/urls.py
import time

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path


def index(request):
    time.sleep(0.1)
    return HttpResponse(status=200, content='Hello, Anonymous')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index)
]


Будем использовать sleep, так как он повторяет поведение синхронной и асинхронной операции ввода и вывода — io bound операции.

Подготовка
Откройте терминал:



Запустите еще 2 терминала: в первом будет запущен django, во втором aiohttp, а в третьем будем проводить эксперименты:


В первом терминале запустите django:


cd servers/dj/
sh start.sh

# должно появиться сообщение об успешном запуске 
[2021-10-17 21:21:58 +0000] [179] [INFO] Starting gunicorn 20.0.4
[2021-10-17 21:21:58 +0000] [179] [INFO] Listening at: http://0.0.0.0:8089 (179)
[2021-10-17 21:21:58 +0000] [179] [INFO] Using worker: sync
[2021-10-17 21:21:58 +0000] [180] [INFO] Booting worker with pid: 180

Во втором терминале запустите aiohttp:


cd servers/aio/
python3 server.py 

# должно появиться сообщение об успешном запуске 
======== Running on http://0.0.0.0:8088 ========
(Press CTRL+C to quit)

В третьем терминале запустите:
ab -n 1000 -c 10  http://127.0.0.1:8088/
-n — количество запросов, которое будет выполнено при тестировании
-c — количество параллельных потоков, которые делают запросы. 
Перед выполнением задач ознакомьтесь с документацией утилиты ab
В результате выполнения получим:


This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests


Server Software:        Python/3.9
Server Hostname:        127.0.0.1
Server Port:            8088

Document Path:          /
Document Length:        16 bytes

Concurrency Level:      10
Time taken for tests:   10.777 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      167000 bytes
HTML transferred:       16000 bytes
Requests per second:    92.79 [#/sec] (mean)
Time per request:       107.773 [ms] (mean)
Time per request:       10.777 [ms] (mean, across all concurrent requests)
Transfer rate:          15.13 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.6      0       6
Processing:   102  106   1.5    106     112
Waiting:      101  104   1.3    104     112
Total:        102  107   1.5    107     112

Percentage of the requests served within a certain time (ms)
  50%    107
  66%    107
  75%    108
  80%    108
  90%    108
  95%    109
  98%    110
  99%    112
 100%    112 (longest request)
В экспериментах будем ориентироваться на параметры:


Requests per second:    92.79 [#/sec] (mean)
Time per request:       107.773 [ms] (mean)
Time per request:       10.777 [ms] (mean, across all concurrent requests)

Time per request (mean) — время, за которое отвечает 1 запрос, если бы вы его вызвали в баузере.
Time per request (mean, across all concurrent requests) — считается количество выполненных запросов суммарно по всем параллельным потокам. Если -с=1, то эти 2 параметра должны совпадать.


Рубрика «Эээксперименты!»
Цели:
Понять преимущества асинхронного подхода перед синхронным 
Понять последствия использования синхронных операций в асинхронном коде 

Задание 7. Сравнение производительности aiohttp и Django при увеличении количества параллельных запросов

Запустите команды ab c соответствующими параметрами и заполните таблицу результатов в отчете. Изменяемый параметр: число параллельных соединений, значения: 5, 10, 20, 40.
ab -n 100 -c <Число параллельных соединений> http://127.0.0.1:8088/
ab -n 100 -c <Число параллельных соединений> http://127.0.0.1:8089/
Постройте графики для aiohttp и Django и приложите их к отчету. Графики:
ось X — количество параллельных запросов, ось Y — время запроса. На графике должно быть 2 линии: per request, all concurrent
ось X — количество параллельных запросов, ось Y — количество RPS

Задание 8. Сравнение производительности aiohttp и Django при увеличении времени io bound операции
Одновременно изменяйте параметр sleep в aiohttp и Django. Изменяемый параметр: время сна, значения: 0.1, 0.2, 0.3.
PS: не забывайте перезапускать веб-серверы, иначе параметры не будут меняться.

# servers/aio/server.py
await asyncio.sleep(0.1)

# servers/dj/dj/urls.py
time.sleep(0.1)
Запустите команды ab c соответствующими параметрами и заполните таблицу результатов в отчете.
ab -n 100 -c 10 http://127.0.0.1:8088/
ab -n 100 -c 10 http://127.0.0.1:8089/
Постройте графики для aiohttp и Django и приложите их к отчету. Графики:
ось X — время сна, ось Y — время запроса. На графике должно быть 2 линии: per request, all concurrent
ось X — время сна, ось Y — количество RPS

Задание 9. Сравнение производительности aiohttp и Django при увеличении количества параллельных запросов, если в aiohttp использовать синхронную операцию.


# замените в файле servers/aio/server.py
# строку 
await asyncio.sleep(0.1)
# на
time.sleep(0.1)
# и перезапустите aiohttp

Запустите команды ab c соответствующими параметрами и заполните таблицу результатов в отчете. Изменяемый параметр — число параллельных соединений, значения: 5, 10, 20, 40.
ab -n 100 -c <Число параллельных соединений> http://127.0.0.1:8088/
Постройте графики для aiohttp, сравните их с Django из задания 7 и приложите к отчету. Графики:
ось X — количество параллельных запросов, ось Y — время запроса. На графике должно быть 2 линии: per request, all concurrent
ось X — количество параллельных запросов, ось Y — количество RPS

Что нужно понять, когда проведете эээксперименты:
Как ведет себя aiohttp при увеличении количества одновременных клиентов
Как ведет вебя Django при увеличении количества одновременных клиентов
Как ведет себя aiohttp при увеличении времени выполнения io-операции
Как ведет себя Django при увеличении времени выполнения io-операции
Как ведет себя aiohttp при использовании синхронной операции
Ответы на эти вопросы должны быть отражены в выводах в отчете.

Django 3.0
В 3-й версии Django добавилась поддержка асинхронности.
https://docs.djangoproject.com/en/3.2/releases/3.0/
“Django 3.0 begins our journey to making Django fully async-capable by providing support for running as an ASGI application.”
3-я версия — это начало поддержки асинхронности. Для полной совместимости еще многое нужно сделать в самой Django и в ее экосистеме.
Как видно из экспериментов, если в асинхронном фреймворке использовать синхронную операцию, производительность драматически падает. Даже если в одном месте использовать быструю синхронную операцию, последствия все равно будут заметны.
Что нужно сделать в Django для поддержки полной асинхронности?

Внутренние компоненты. Работа с ORM, с cache и прочим остается синхронной. Эти компоненты пока не переписали, но сделали костыль sync_to_async. Он нем можно почитать тут: https://docs.djangoproject.com/en/3.2/topics/async/
В следующих версиях Django в них, скорее всего, добавят нативную поддержку async await интерфейса без костылей.

Внутренние библиотеки contrib. Внутри Django есть набор готовых компонент, которые позволяют быстрее писать код. Например, django.contrib.auth. Для поддержки асинхронности нужно переписать все эти компоненты.

Внешние библиотеки. Если предыдущие шаги зависели от разработчиков библиотеки, и это централизованно можно было бы изменить, то огромная база написанных библиотек сторонними разработчиками тоже должна поддержать асинхронность и переписать свои библиотеки под asyn await интерфейс. При этом нужно сохранить обратную совместимость, что является нетривиальной задачей.
Исходя из сказанного, путь полной поддержки в django будет достаточно долгий, но с большой вероятностью в будущем мы придем в асинхронности в Django.