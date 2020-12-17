import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--key",
                    required=True, type=str)
parser.add_argument("--path",
                    required=True, type=str)
parser.add_argument("--template",
                    choices=["financial", "identity", "structuredPdf", "plainText"],
                    default="financial", type=str)
parser.add_argument("--text_extraction",
                    choices=["fast","full"],
                    default="fast", type=str)
parser.add_argument("--monitor",
                    choices=["passive","proactive"],
                    type=str)



args = parser.parse_args()

key = args.key
path = args.path
template = args.template
text_extraction = args.text_extraction
monitor = args.monitor

print(key)
print(path)
print(template)
print(text_extraction)
print(monitor)

# import threading
# import os
# import base64
# import os
# import time
# from watchdog.observers import Observer
# from watchdog.events import PatternMatchingEventHandler
# import pathlib
# import json
# import requests
#
# def on_created(event):
#  print(f"hey, {event.src_path} has been created!")
#
# def initWatchDog():
#     print("Watch dog assigned to thread: {}".format(threading.current_thread().name))
#     #print("ID of process running task 1: {}".format(os.getpid()))
#
#     patterns = "*"
#     ignore_patterns = ""
#     ignore_directories = False
#     case_sensitive = True
#     my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
#     my_event_handler.on_created = on_created
#
#     path = ".\\items"
#     go_recursively = True
#     my_observer = Observer()
#     my_observer.schedule(my_event_handler, path, recursive=go_recursively)
#     my_observer.start()
#
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         my_observer.stop()
#         my_observer.join()
#
#
# def task2():
#     print("Task 2 assigned to thread: {}".format(threading.current_thread().name))
#     #print("ID of process running task 2: {}".format(os.getpid()))
#
# if __name__ == "__main__":
#     # print ID of current process
#     #print("ID of process running main program: {}".format(os.getpid()))
#
#     # print name of main thread
#     #print("Main thread name: {}".format(threading.current_thread().name))
#
#     # creating threads
#     t1 = threading.Thread(target=initWatchDog, name='t1')
#     t2 = threading.Thread(target=task2, name='t2')
#
#     # starting threads
#     t1.start()
#     t2.start()
#
#     # wait until all threads finish
#     t1.join()
#     t2.join()
#
# #
# # # test = input("Voer je API key in: ")
# # # print("API key: " + test)
# # #
# # # useTemplate = input("Wil je een template gebruiken? De default is Template Financial (j/N)")
# # # if useTemplate == "j":
# # #     print("Welke template gebruiken?")
# # # else:
# # #     print("Doorgaan met Template Financial")
# #
# # # path = "C:\\Users\\Johan\\Desktop\\success_response.json"
# # # for path in pathlib.Path(path).iterdir():
# # #     if path.is_file():
# # path = "C:\\Users\\Johan\\Desktop\\success_response.txt"
# # current_file = open(path, "r")
# # print(current_file)
# # data = json.load(open(current_file.name))
# # with open(os.path.splitext(current_file.name)[0]+ '.json', 'w') as outfile:
# #     json.dump(data, outfile)
# # try:
# #
# #     print(current_file.read())
# #     # for line in current_file.readlines():
# #     #     f = open("guru99.txt", "w+")
# #     #     f.write(line)
# #     #     f.close()
# #     current_file.close()
# # except:
# #     print("no")
# #
#
# # # with open("C:\\users\\johan\\desktop\\bonnetje.jpg", "rb") as image_file:
# # #    encoded_string = base64.b64encode(image_file.read())
# # #    decoded_string = encoded_string.decode("utf-8")
# #
# #    # url = "https://test.custom-ocr.klippa.com/api/v1/parseDocument"
# #    # data = {'document': decoded_string}
# #    # headers = {'X-Auth-Key':'lIr1BRW1VEjjy2d88HaRiFg5hQRE3FHL','Content-type': 'application/json', 'Accept': 'application/json'}
# #    # r = requests.post(url, data=json.dumps(data), headers=headers)
# #    # print(r)
# #
# # # gewoon tekst opvragen, dit telt geen tickets.
# #
# #    # url = "https://test.custom-ocr.klippa.com/api/v1/credits"
# #    # headers = {'X-Auth-Key': 'lIr1BRW1VEjjy2d88HaRiFg5hQRE3FHL', 'Content-type': 'application/json',
# #    #            'Accept': 'application/json'}
# #    # response = requests.get(url, headers=headers)
# #    # print(response.request.body)
# #    # print(response.request.headers)
# #    # print(response.json())
# #    # print(response.text)
