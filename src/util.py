import re
from datetime import datetime

class STATUS_CODES :
    PASS = 0
    FAIL = 1
    LOG = 2

statusLookup = {
    STATUS_CODES.PASS: "PASS",
    STATUS_CODES.FAIL: "FAIL",
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


def name_to_last_first(fullName: str) -> str:
    parts = fullName.strip().split()
    if len(parts) >= 2:
        first = " ".join(parts[:-1])
        last = parts[-1]
        return f"{last}, {first}"
            
    return fullName  # fallback if name is malformed


def name_trim_middle(fullName: str) -> str:
    parts = fullName.strip().split()
    if len(parts) >= 2:
        return f"{parts[0]} {parts[-1]}"
    return fullName  # fallback if malformed or single name


def payroll_number_trim(payrollNum: str) -> str:
    match = re.search(r"\d+", payrollNum)
    return match.group() if match else "0"


def number_to_string(value) -> str:
    if isinstance(value, float):
        return f"{value:.2f}"

    return str(value)
