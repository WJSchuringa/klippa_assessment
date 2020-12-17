import argparse
import threading
import os
import base64
import os
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import pathlib
import json
import requests

def on_created(event):
    print("hey, " + event.src_path + " has been created!")

def initWatchDog(path,mode,file_searcher):
    if mode == "passive":
        print("Watch dog assigned to thread: {}".format(threading.current_thread().name))
        #print("ID of process running task 1: {}".format(os.getpid()))

        patterns = "*"
        ignore_patterns = ""
        ignore_directories = False
        case_sensitive = True
        my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        my_event_handler.on_created = on_created

        go_recursively = True
        my_observer = Observer()
        my_observer.schedule(my_event_handler, path, recursive=go_recursively)
        my_observer.start()

        try:
            while file_searcher.is_alive():
                time.sleep(1)
        except KeyboardInterrupt:
            my_observer.stop()
            my_observer.join()

def parseFile(path):
    with open(path, "rb") as file:
       encoded_string = base64.b64encode(file.read())
       decoded_string = encoded_string.decode("utf-8")
       #print(decoded_string)
       print(path)
       time.sleep(2)
    file.close()
    apiRequest(path)

def apiRequest(document):
    #gewoon tekst opvragen, dit telt geen tickets.

    apiUrl = "https://test.custom-ocr.klippa.com/api/v1/credits"
    headers = {'X-Auth-Key': 'lIr1BRW1VEjjy2d88HaRiFg5hQRE3FHL', 'Content-type': 'application/json',
              'Accept': 'application/json'}
    response = requests.get(apiUrl, headers=headers)
    print(json.dumps(response.json(),indent=4))
    storeOutput(response.json(), document)

def storeOutput(data, path):
    current_file = open(path, "r")
    with open(os.path.splitext(current_file.name)[0] + '.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

def initFileSearcher(path):
    print("File searcher assigned to thread: {}".format(threading.current_thread().name))
    if os.path.isdir(path):
        for path in pathlib.Path(path).iterdir():
            if path.is_file():
                if os.path.splitext(path)[1].upper() in {".PDF", ".GIF", ".PNG", ".JPG", ".HEIC", ".HEIF"} :
                    file_parser = threading.Thread(target=parseFile(path), name='FileParser')
                    file_parser.start()
    else:
        if os.path.splitext(path)[1].upper() in {".PDF", ".GIF", ".PNG", ".JPG", ".HEIC", ".HEIF"}:
            print("Ondersteund bestand gevonden: " + path)
            file_parser = threading.Thread(target=parseFile(path), name='FileParser')
            file_parser.start()





if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--key",
                        required=True, type=str)
    parser.add_argument("--path",
                        required=True, type=str)
    parser.add_argument("--template",
                        choices=["financial", "identity", "structuredPdf", "plainText"],
                        default="financial", type=str)
    parser.add_argument("--text_extraction",
                        choices=["fast", "full"],
                        default="fast", type=str)
    parser.add_argument("--monitor",
                        choices=["passive", "proactive"],
                        type=str)

    args = parser.parse_args()

    key = args.key
    path = args.path
    template = args.template
    text_extraction = args.text_extraction
    monitor = args.monitor

    # # creating threads
    FileSearcher = threading.Thread(target=initFileSearcher(path), name='FileSearcher')
    if monitor is not None:
        WatchDog = threading.Thread(target=initWatchDog(path,monitor,FileSearcher), name='WatchDog')


    if monitor is not None:
        WatchDog.start()
        FileSearcher.start()
    else:
        WatchDog.start()
        FileSearcher.start()

    # wait until all threads finish
    if monitor is not None:
        WatchDog.join()
        FileSearcher.join()
    else:
        WatchDog.join()
        FileSearcher.join()


#    # url = "https://test.custom-ocr.klippa.com/api/v1/parseDocument"
#    # data = {'document': decoded_string}
#    # headers = {'X-Auth-Key':'lIr1BRW1VEjjy2d88HaRiFg5hQRE3FHL','Content-type': 'application/json', 'Accept': 'application/json'}
#    # r = requests.post(url, data=json.dumps(data), headers=headers)
#    # print(r)
#
