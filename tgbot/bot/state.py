from enum import Enum


class State:
    NOT_REGISTERED = 0
    INPUT_NAME = 1
    MAIN = 2
    GROUP_CREATING = 3
    GROUP_JOINING = 4
    GROUP = 5
    QUEUE_CREATING = 6
    QUEUE = 7
