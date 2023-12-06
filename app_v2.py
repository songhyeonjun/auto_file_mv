import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread
from watcher import Watcher
import os
import shutil

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("파일 감시 프로그램")  # 윈도우 타이틀 설정
        self.root.geometry("400x500")  # 윈도우 크기 설정

        # 감시할 폴더 경로 입력 필드 생성
        self.create_input_field("감시할 폴더 경로:", "source_path")

        self.destination_frames = []  # 프레임을 저장할 리스트
        
        # 이동 버튼
        self.move_button_1 = tk.Button(root, text="파일 이동", command=self.move_files, bg='blue', fg='white', width=20, height=2)
        self.move_button_1.pack(side="bottom")
        
        # 종료 버튼
        self.stop_button = tk.Button(root, text="종료", command=self.stop_watcher, bg='red', fg='black', width=20, height=2)
        self.stop_button.pack(side="bottom")
        
        # 시작 버튼
        self.start_button = tk.Button(root, text="시작", command=self.start_watcher, bg='green', fg='black', width=20, height=2)
        self.start_button.pack(side="bottom")
        
        # 이동할 폴더 제거 버튼
        self.remove_destination_button = tk.Button(root, text="이동할 폴더 제거", command=self.remove_destination_field, bg='black', fg='white', width=20, height=2)
        self.remove_destination_button.pack(side="bottom")
        
        # 이동할 폴더 추가 버튼
        self.add_destination_button = tk.Button(root, text="이동할 폴더 추가", command=self.add_destination_field, bg='white', fg='black', width=20, height=2)
        self.add_destination_button.pack(side="bottom")


        # 감시 스레드 및 Watcher 객체 초기화
        self.watcher_thread = None
        self.watcher = None

   # 경로 입력 필드와 라벨, 버튼을 포함하는 프레임 생성 함수
    def create_input_field(self, label_text, field_name=None):
        frame = tk.Frame(self.root)
        label = tk.Label(frame, text=label_text)
        label.pack(side='left')

        if field_name:
            entry_var = tk.StringVar()
            setattr(self, field_name, entry_var)
            entry = tk.Entry(frame, textvariable=entry_var)
        else:
            entry = tk.Entry(frame)
            self.destination_entries.append(entry)  # 이동할 폴더 경로들을 저장할 리스트에 추가

        entry.pack(side='left', expand=True, fill='x')

        button = tk.Button(frame, text="찾아보기", command=lambda: self.browse_folder(entry))
        button.pack(side='right')

        frame.pack(padx=10, pady=5, fill='x')

    # 이동할 폴더 경로 추가 함수
    def add_destination_field(self):
        frame = tk.Frame(self.root)
        label = tk.Label(frame, text="이동할 폴더 경로:")
        label.pack(side='left')

        entry = tk.Entry(frame)
        entry.pack(side='left', expand=True, fill='x')

        button = tk.Button(frame, text="찾아보기", command=lambda: self.browse_folder(entry))
        button.pack(side='right')

        frame.pack(padx=10, pady=5, fill='x')

        self.destination_frames.append(frame)

    # 이동할 폴더 경로 제거 함수
    def remove_destination_field(self):
        if self.destination_frames:
            frame_to_remove = self.destination_frames.pop()
            frame_to_remove.destroy()

    # 폴더 탐색기를 통해 경로 선택 함수
    def browse_folder(self, entry):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            entry.delete(0, tk.END)
            entry.insert(0, folder_selected)

    # 감시 시작 함수
    def start_watcher(self):
        if not self.watcher_thread or not self.watcher_thread.is_alive():
            source_path = self.source_path.get()
            destinations = [entry.get() for entry in self.destination_frames if entry.get()]

            # 모든 필수 경로가 입력되었는지 확인
            if not source_path or not destinations:
                messagebox.showwarning("경고", "모든 필수 경로를 입력해주세요.")
                return

            directories_to_watch = {source_path: destinations}

            self.watcher = Watcher(directories_to_watch)
            self.watcher_thread = Thread(target=self.watcher.run)
            self.watcher_thread.start()
            messagebox.showinfo("성공", "파일 이동 완료")
        else :
            messagebox.showwarning("경고", "유효한 소스 폴더 경로를 입력해주세요.")
            
    # 감시 종료 함수
    def stop_watcher(self):
        if self.watcher:
            self.watcher.observer.stop()
            self.watcher.observer.join()
            self.watcher_thread = None
    
    # 파일 이동 함수 
    def move_files(self):
        """지정된 폴더의 모든 파일을 다른 경로로 이동합니다."""
        source_path = self.source_path.get()  # 소스 폴더 경로
        destination_paths = [entry.get() for entry in self.destination_frames if entry.get()]  # 이동할 폴더 경로들

        if not source_path or not destination_paths:
            messagebox.showwarning("경고", "모든 필수 경로를 입력해주세요.")
            return

        # 소스 폴더의 모든 파일을 각 대상 폴더로 이동
        if os.path.isdir(source_path):
            for filename in os.listdir(source_path):
                file_path = os.path.join(source_path, filename)
                if os.path.isfile(file_path):
                    for dest_path in destination_paths:
                        shutil.move(file_path, os.path.join(dest_path, filename))
            messagebox.showinfo("성공", "파일 이동 완료")
        else:
            messagebox.showwarning("경고", "유효한 소스 폴더 경로를 입력해주세요.")
            

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()