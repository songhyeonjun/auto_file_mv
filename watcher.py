import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import tkinter as tk
from threading import Thread


# Watcher 클래스 : 여러 디렉토리를 감시하기 위한 클래스
class Watcher:
    # 생성자 : 감시할 디렉토리의 목록을 초기화
    def __init__(self, directories_to_watch):
        self.observer = Observer()
        self.directories_to_watch = directories_to_watch

    # run 메서드 : 각 디렉토리에 대한 감시를 시작
    def run(self):
        for directory, destinations in self.directories_to_watch.items():
            event_handler = Handler(destinations)
            self.observer.schedule(event_handler, directory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

# Handler 클래스: 파일 시스템 이벤트 처리를 위한 클래스
class Handler(FileSystemEventHandler):
    # 생성자: 이동할 대상 디렉토리의 목록을 초기화
    def __init__(self, destination_directories):
        self.destination_directories = destination_directories

    # on_created 메서드: 파일 생성 이벤트가 발생했을 때 호출
    def on_created(self, event):
        if event.is_directory:
            return None
        else:
            filename = os.path.basename(event.src_path)

            # 마지막 대상 폴더를 제외한 모든 폴더로 복사
            for destination_directory in self.destination_directories[:-1]:
                destination_path = os.path.join(destination_directory, filename)
                shutil.copy(event.src_path, destination_path)

            # 마지막 대상 폴더로 이동
            final_destination = os.path.join(self.destination_directories[-1], filename)
            if os.path.isfile(final_destination):
                os.remove(final_destination)    # 대상 파일이 존재하면 삭제
            shutil.move(event.src_path, final_destination)  # 파일 이동