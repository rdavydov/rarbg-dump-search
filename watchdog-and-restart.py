# run command: TZ='Europe/Moscow' python watchdog-and-restart.py

import subprocess
import time
import logging
from datetime import datetime


def setup_logger():
    logger = logging.getLogger("watchdog")
    logger.setLevel(logging.INFO)

    # Create a formatter with timezone information
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S %Z%z",
    )

    # Create a StreamHandler for logging to the console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Create a FileHandler for logging to a file
    file_handler = logging.FileHandler("watchdog-and-restart.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def run_uvicorn(logger):
    command = [
        "uvicorn",
        "backend-2dbs:app",
        "--host",
        "0.0.0.0",
        "--port",
        "31337",
        "--log-config",
        "uvicorn_logging.conf"
    ]
    subprocess.run(command)


def restart_uvicorn(logger):
    logger.info("Restarting Uvicorn process...")
    process = subprocess.Popen(
        ["pgrep", "-f", "uvicorn backend-2dbs:app"], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    if process.returncode == 0:
        process_ids = output.decode().strip().split("\n")
        for process_id in process_ids:
            subprocess.run(["kill", process_id])
    run_uvicorn(logger)


def watchdog():
    logger = setup_logger()
    while True:
        current_time = datetime.now()
        # restarts uvicorn every 4 hours
        if current_time.hour % 4 == 0 and current_time.minute == 0:
            restart_uvicorn(logger)
        else:
            process = subprocess.Popen(
                ["pgrep", "-f", "uvicorn backend-2dbs:app"], stdout=subprocess.PIPE)
            # Since we are only interested in whether the command executed successfully or not, and not the actual output,
            # we assign the output stream to output and ignore the error stream by using the _ variable. By convention,
            # the _ variable is often used as a throwaway variable to indicate that a value
            # is intentionally being ignored or not used in the code.
            output, _ = process.communicate()
            if process.returncode != 0:
                logger.info("Uvicorn process is not running. Restarting...")
                run_uvicorn(logger)
        time.sleep(10)  # sleep for 10 seconds


if __name__ == "__main__":
    watchdog()
