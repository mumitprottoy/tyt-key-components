import threading
from utils.models import Tracker
from utils.constants import APNT_HOLD_LIMIT
from finances.models import Invoice


def execute_scheduled_task(timer, task) -> None:
    threading.Timer(timer, task).start()
    

