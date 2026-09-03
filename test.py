from loading_bar_def import run_loading
import time
import PySimpleGUI as sg


def fake_task():
    time.sleep(100)  # simulate work


def after_task():
    sg.popup("Task finished")


run_loading(task_func=fake_task, next_func=after_task)
