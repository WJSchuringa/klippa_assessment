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


class WatchDog:

    def __init__(self, key, template, text_extraction, path, mode, file_searcher, store_output):
        self.key = key
        self.template = template
        self.text_extraction = text_extraction
        self.path = path
        self.mode = mode
        self.file_searcher = file_searcher
        self.store_output = store_output
        self.threads = []

    def on_created(self, event):
        print(event.src_path + " has been created!")
        if self.mode == "proactive":
            fileSearcher = FileSearcher(self.key, self.template, self.text_extraction, event.src_path,
                                        self.store_output)
            t1 = threading.Thread(target=fileSearcher.run)
            self.threads.append(t1)
            t1.start()
            t1.join()

    def run(self):
        print("Watch dog assigned to thread: {}".format(threading.current_thread().name))
        # print("ID of process running task 1: {}".format(os.getpid()))

        patterns = "*"
        ignore_patterns = ""
        ignore_directories = False
        case_sensitive = True
        my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories,
                                                       case_sensitive)
        my_event_handler.on_created = self.on_created

        go_recursively = True
        my_observer = Observer()
        my_observer.schedule(my_event_handler, path, recursive=go_recursively)
        my_observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            my_observer.stop()
            my_observer.join()


class FileSearcher:

    def __init__(self, key, template, text_extraction, path, store_output):
        self.key = key
        self.template = template
        self.text_extraction = text_extraction
        self.path = path
        self.store_output = store_output

    def parseFile(self, path):
        with open(path, "rb") as file:
            encoded_string = base64.b64encode(file.read())
            decoded_string = encoded_string.decode("utf-8")
            print(decoded_string)
            print(path)
            time.sleep(2)
        file.close()
        self.apiRequest(decoded_string, path)

    def apiRequest(self, decoded_string, path):
        # # gewoon tekst opvragen, dit telt geen tickets.

        # apiUrl = "https://test.custom-ocr.klippa.com/api/v1/credits"
        # headers = {'X-Auth-Key': self.key, 'Content-type': 'application/json',
        #            'Accept': 'application/json'}
        # response = requests.get(apiUrl, headers=headers)
        # print(json.dumps(response.json(), indent=4))

        apiUrl = "https://test.custom-ocr.klippa.com/api/v1/parseDocument"
        if self.template == "identity":
            apiUrl = "https://test.custom-ocr.klippa.com/api/v1/parseDocument/identity"

        data = {'document': decoded_string, 'pdf_text_extraction': self.text_extraction}
        headers = {'X-Auth-Key': self.key, 'Content-type': 'application/json',
                   'Accept': 'application/json'}
        response = requests.post(apiUrl, data=json.dumps(data), headers=headers)
        print(json.dumps(response.json(), indent=4))

        if self.store_output == "yes":
            self.storeOutput(response.json(), path)

    def storeOutput(self, data, path):
        current_file = open(path, "r")
        with open(os.path.splitext(current_file.name)[0] + '.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def run(self):
        print("File searcher assigned to thread: {}".format(threading.current_thread().name))
        if os.path.isdir(self.path):
            for path in os.listdir(self.path):
                    if os.path.splitext(path)[1].upper() in {".PDF", ".GIF", ".PNG", ".JPG", ".HEIC", ".HEIF"}:
                        file_parser = threading.Thread(target=self.parseFile(path), name='FileParser')
                        file_parser.start()
        else:
            if os.path.splitext(self.path)[1].upper() in {".PDF", ".GIF", ".PNG", ".JPG", ".HEIC", ".HEIF"}:
                print("Ondersteund bestand gevonden: " + self.path)
                file_parser = threading.Thread(target=self.parseFile(self.path), name='FileParser')
                file_parser.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--key",
                        required=True, type=str)
    parser.add_argument("--path",
                        required=True, type=str)
    parser.add_argument("--template",
                        choices=["financial", "identity"],
                        default="financial", type=str)
    parser.add_argument("--text_extraction",
                        choices=["fast", "full"],
                        default="fast", type=str)
    parser.add_argument("--monitor",
                        choices=["passive", "proactive"],
                        default="passive", type=str)
    parser.add_argument("--store_output",
                        choices=["yes", "no"],
                        type=str)

    args = parser.parse_args()

    key = args.key
    path = args.path
    template = args.template
    text_extraction = args.text_extraction
    monitor = args.monitor
    store_output = args.store_output

    # if monitor is not None and monitor_duration is None:
    #     parser.error("--monitor requires --monitor_duration to be set.")

    # # creating threads
    fileSearcher = FileSearcher(key, template, text_extraction, path, store_output)
    watchDog = WatchDog(key, template, text_extraction, path, monitor, fileSearcher, store_output)
    t1 = threading.Thread(target=fileSearcher.run)
    t2 = threading.Thread(target=watchDog.run)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
