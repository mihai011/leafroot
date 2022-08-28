"""Scripts."""

import os
import subprocess


def get_pids(command):
    """Return list of pids of process ids.

    Params:
        command: os command that must return each pid on a line
    """
    if not command:
        return []

    with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) as task:
        pids = task.stdout.read().decode("utf-8").split("\n")[:-1]

    return pids


def close_local_processes(pids):
    """Receives a list of pids and kills the processes.

    Params:
        pids: list of pids
    """
    if not pids:
        return False

    for pid in pids:
        os.system("kill -9 {}".format(pid))

    return True


if __name__ == "__main__":

    command = "ps auxww | pgrep 'celery_worker' | grep -v grep | awk '{print $2}'"

    pids = get_pids(command)

    close_local_processes(pids)
