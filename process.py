import pydirectinput as direct
import pyautogui as auto
from python_imagesearch.imagesearch import imagesearcharea as search
from python_imagesearch.imagesearch import imagesearch_region_loop as searchloop
from python_imagesearch.imagesearch import imagesearch_numLoop as searchnumloop
from time import sleep
from os import listdir
import random
import logging

auto.FAILSAFE = False

def move(pos, duration=0.8, tween=auto.easeInOutBack):
    auto.moveTo(pos[0], pos[1], duration, tween)

def find_onscreen(path, precision=0.8):
    return search(path, 0, 0, 2560, 1440, precision=precision)


def loop_find_onscreen(path, delay=1, precision=0.8):
    return searchloop(path, delay, 0, 0, 2560, 1440, precision=precision)


def numloop_find_onscreen(path, delay=1, max_samples=10):
    return searchnumloop(path, delay, max_samples)


def find_move(path, precision=0.8):
    pos = find_onscreen(path, precision)
    move(pos)
    logging.info(pos)
    return pos


def move_onfind(path, delay=1):
    pos = loop_find_onscreen(path, delay)
    move(pos)


def click_ingame(button="left"):
    auto.mouseDown(button=button)
    sleep(0.01)
    auto.mouseUp(button=button)


# Queue steps
def find_match():
    move_onfind("./captures/find_match.png", 1)
    direct.click()


def wait_for_match():
    move_onfind("./captures/accept.png", 1)
    direct.click()
    pos = find_onscreen("./captures/settings_icon.png")
    while pos[0] == -1:
        direct.click()
        sleep(1)
        pos = find_onscreen("./captures/settings_icon.png")
    logging.info("Game started")


def wait_for_end():
    move_onfind("./captures/exit_now.png", 60)
    click_ingame()
    logging.info("Game exited")
    move_onfind("./captures/play_again.png", 2)
    direct.click()
    logging.info("Entered new lobby")


def play_match():
    # sleep(59)
    while True:
        match_end = find_onscreen("./captures/exit_now.png")
        if match_end[0] != -1:
            move(match_end)
            click_ingame()
        match_end = numloop_find_onscreen("./captures/skip_waiting_for_stats.png", 1, 10)
        if match_end[0] != -1:
            move(match_end)
            direct.click()
            move_onfind("./captures/quick_play.PNG")
            direct.click()
            return
        else:
            match_end = find_onscreen("./captures/play_again.png")
            if match_end[0] != -1:
                move(match_end)
                direct.click()
                logging.info("Entered new lobby")
                return
            else:
                move_randomly()
                buy_random()


def move_randomly():
    move([random.randrange(800, 1600), random.randrange(300, 900)])
    click_ingame("right")


def buy_random():
    traits = listdir("captures/traits")
    trait = traits[random.randrange(len(traits))]
    for i in range(5):
        sleep(1)
        pos = find_onscreen(f"captures/traits/{trait}", 0.9)
        if pos[0] != -1:
            move(pos)
            sleep(0.01)
            click_ingame()
            move([575+(random.randrange(1320)), 1050], 0.8, auto.easeInOutBack)
            direct.press('w')
        else:
            trait = traits[random.randrange(len(traits))]
    direct.press('d')
    direct.press('f')


def queue():
    find_match()
    wait_for_match()
    play_match()


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

match_count = 0 
while True:
    queue()
    match_count += 1
    logging.info(f"Current match count: {match_count}")
