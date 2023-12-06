import os
import shutil
import tkinter as tk
from threading import Thread
from watcher import Watcher
from tkinter import filedialog, messagebox

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("파일 감시 프로그램") # 타이틀
        self.root.geometry("275x400+100+100") # 크기
        self.root.resizable(True, True)   
        
        self.start_button = tk.Button(root, text="시작", command=self.start_watcher, bg='green', fg='black', width=37, height=5)
        self.start_button.pack(expand=True)

        self.stop_button = tk.Button(root, text="종료", command=self.stop_watcher, bg='red', fg='black', width=37, height=5)
        self.stop_button.pack(expand=True)
        
        self.move_button_1 = tk.Button(root, text="새폴더 파일 이동", command=self.move_files, bg='blue', fg='white', width=37, height=5)
        self.move_button_1.pack(expand=True)
        
        self.move_button_2 = tk.Button(root, text="새폴더 (3) 파일 이동", command=self.move_files2, bg='blue', fg='white', width=37, height=5)
        self.move_button_2.pack(expand=True)

        self.watcher_thread = None
        self.watcher = None
    
    # 새폴더 -> 새폴더 (2) 파일 이동
    def move_files(self):
        """지정된 폴더의 모든 파일을 다른 경로로 이동합니다."""
        source_path = "C:/Users/p13259/Desktop/새 폴더"  # 소스 폴더 경로
        destination_paths = ["C:/Users/p13259/Desktop/새 폴더 (2)"]  # 이동할 폴더 경로들

        # 소스 폴더의 모든 파일을 각 대상 폴더로 이동
        for filename in os.listdir(source_path):
            file_path = os.path.join(source_path, filename)
            if os.path.isfile(file_path):
                for dest_path in destination_paths:
                    shutil.move(file_path, os.path.join(dest_path, filename))
        messagebox.showwarning("파일 이동 완료", "파일 이동 완료!!!!!!!!!")
        
    # 새폴더 (3) -> 새폴더 (4) 이동
    def move_files2(self):
        """지정된 폴더의 모든 파일을 다른 경로로 이동합니다."""
        source_path = "C:/Users/p13259/Desktop/새 폴더 (3)"  # 소스 폴더 경로
        destination_paths = ["C:/Users/p13259/Desktop/새 폴더 (4)"]  # 이동할 폴더 경로들

        # 소스 폴더의 모든 파일을 각 대상 폴더로 이동
        for filename in os.listdir(source_path):
            file_path = os.path.join(source_path, filename)
            if os.path.isfile(file_path):
                for dest_path in destination_paths:
                    shutil.move(file_path, os.path.join(dest_path, filename))
        messagebox.showwarning("파일 이동 완료", "파일 이동 완료!!!!!!!!!")
    
    
    # 폴더 감시
    def start_watcher(self):
        if not self.watcher_thread or not self.watcher_thread.is_alive():
            directories_to_watch = {
                "C:/Users/p13259/Desktop/새 폴더" : ["C:/Users/p13259/Desktop/새 폴더 (2)"], # 소스 폴더 경로 : [이동할 폴더들 경로]
                "C:/Users/p13259/Desktop/새 폴더 (3)" : ["C:/Users/p13259/Desktop/새 폴더 (4)"],
                "C:/Users/p13259/Desktop/새 폴더 (5)" : ["C:/Users/p13259/Desktop/새 폴더 (6)", "C:/Users/p13259/Desktop/새 폴더 (7)", "C:/Users/p13259/Desktop/새 폴더 (8)"]
        # 추가적인 폴더 감시 설정
            }
            self.watcher = Watcher(directories_to_watch)
            self.watcher_thread = Thread(target=self.watcher.run)
            self.watcher_thread.start()
            messagebox.showwarning("파일 감시 시작", "파일 감시 시작!!!!!!!!!")

    def stop_watcher(self):
        if self.watcher:
            self.watcher.observer.stop()
            self.watcher.observer.join()
            self.watcher_thread = None
            messagebox.showwarning("파일 감시 종료", "파일 감시 종료!!!!!!!!!")

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    
    