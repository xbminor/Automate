from datetime import datetime

class STATUS_CODES :
    PASS = 0
    ERROR = 1
    LOG = 2

statusLookup = {
    STATUS_CODES.PASS: "PASS",
    STATUS_CODES.ERROR: "ERROR",
    STATUS_CODES.LOG: "LOG",
}


def log_message(status: int, msg: str, filePath: str, isPrint: bool):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    statusText = statusLookup.get(status, f"NULL ({status})")
    log = f"{timestamp} - {statusText:^4} - {msg}"
    with open(filePath, "a", encoding="utf-8") as f:
        f.write(f"{log}\n")
    
    if isPrint:
        print(log)

