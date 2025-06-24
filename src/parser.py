import src.util as Util
import pandas as pd
from datetime import datetime, timedelta
import json
import os


emptyCellString = ""
emptyCellFloat = 0.0
emptyCellInt = 0

def _extract_header_contractor(dataFrame, indexRow, indexCol):
    data =  {
        "contractor_name": dataFrame.iloc[indexRow, indexCol+2],
        "contractor_address1": dataFrame.iloc[indexRow+1, indexCol+2],
        "contractor_address2": dataFrame.iloc[indexRow+2, indexCol+2],
    }

    return data


def _extract_header_project(dataFrame, indexRow, indexCol):
    data =  {
        "project_name": dataFrame.iloc[indexRow, indexCol+1],
    }

    return data


def _extract_header_payroll_number(dataFrame, indexRow, indexCol):
    data =  {
        "payroll_number": dataFrame.iloc[indexRow, indexCol+3],
    }

    return data


def _extract_header_week_ending(dataFrame, indexRow, indexCol):
    data =  {
        "week_ending": dataFrame.iloc[indexRow, indexCol+3].date().isoformat(),
    }

    return data




def _extract_employee_info(dataFrame, indexRow, indexCol, employeeTotal):
    names = []
    for i in range(employeeTotal):
        data = {
            "employee_name": dataFrame.iloc[indexRow+1+3*i, indexCol],
            "employee_address1": dataFrame.iloc[indexRow+2+3*i, indexCol],
            "employee_address2": dataFrame.iloc[indexRow+3+3*i, indexCol],
        }
        names.append(data)

    return names


def _extract_employee_social(dataFrame, indexRow, indexCol, employeeTotal):
    output = []
    for i in range(employeeTotal):
        data =  {
            "employee_ssn": dataFrame.iloc[indexRow+1+3*i, indexCol],
        }
        output.append(data)

    return output


def _extract_employee_work_class(dataFrame, indexRow, indexCol, employeeTotal):
    output = []
    for i in range(employeeTotal):
        data =  {
            "work_classification": dataFrame.iloc[indexRow+1+3*i, indexCol],
        }
        output.append(data)

    return output


def _extract_employee_hours_paid(dataFrame, indexRow, indexCol, employeeTotal, strWeekEnding):
    output = []
    weekDays = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
    dateWeekEnding = datetime.strptime(strWeekEnding, "%Y-%m-%d").date()
    dateWeekStart = dateWeekEnding - timedelta(days=6)

    for i in range(employeeTotal):
        data = {}
        rt = dataFrame.iloc[indexRow+1+3*i, indexCol]
        ot = dataFrame.iloc[indexRow+2+3*i, indexCol]
        dt = dataFrame.iloc[indexRow+3+3*i, indexCol]

        data["work_pay_type_RT"] = False if pd.isna(rt) else True
        data["work_pay_type_OT"] = False if pd.isna(ot) else True
        data["work_pay_type_DT"] = False if pd.isna(dt) else True
       
        
        indexColSun = indexCol + 1
        dataWeekRT, dataWeekOT, dataWeekDT = [], [], []
        for j, day in enumerate(weekDays):
            date = (dateWeekStart + timedelta(days=j)).isoformat()

            rtHours = dataFrame.iloc[indexRow+1+3*i, indexColSun+j]
            otHours = dataFrame.iloc[indexRow+2+3*i, indexColSun+j]
            dtHours = dataFrame.iloc[indexRow+3+3*i, indexColSun+j]
            
            dataWeekRT.append({"day": day, "date": date, "value": emptyCellFloat if pd.isna(rtHours) else float(rtHours)})
            dataWeekOT.append({"day": day, "date": date, "value": emptyCellFloat if pd.isna(otHours) else float(otHours)})
            dataWeekDT.append({"day": day, "date": date, "value": emptyCellFloat if pd.isna(dtHours) else float(dtHours)})

        data["hours_rt"] = dataWeekRT
        data["hours_ot"] = dataWeekOT
        data["hours_dt"] = dataWeekDT
        
        output.append(data)

    return output


def _extract_employee_fringe_benefits(dataFrame, indexRow, indexCol, employeeTotal):
    output = []
    for i in range(employeeTotal):
        data =  {
            "fringe": dataFrame.iloc[indexRow+1+3*i, indexCol],
        }
        output.append(data)

    return output


def _handle_employees(cell, indexRow, indexCol, dataFrame, employees, dateWeekEnding):
    employeeTotal = int((len(dataFrame)-8)/3)
    employeeData = None

    if cell == "Employee Name":
        employeeData = _extract_employee_info(dataFrame, indexRow, indexCol, employeeTotal)
    elif cell == "SSN":
        employeeData = _extract_employee_social(dataFrame, indexRow, indexCol, employeeTotal)
    elif cell == "Classification":
        employeeData = _extract_employee_work_class(dataFrame, indexRow, indexCol, employeeTotal)
    elif cell == "Type":
        employeeData = _extract_employee_hours_paid(dataFrame, indexRow, indexCol, employeeTotal, dateWeekEnding)
    elif cell == "Gross Pay":
        employeeData = _extract_employee_fringe_benefits(dataFrame, indexRow, indexCol, employeeTotal)

    if employeeData:
        for i in range(employeeTotal):
            while len(employees) <= i:
                employees.append({})

            employees[i].update(employeeData[i])

    return


def _handle_header(cell, indexRow, indexCol, dataFrame, header):
    headerData = None
    if cell == "Contractor":
        headerData = _extract_header_contractor(dataFrame, indexRow, indexCol)
    elif cell == "Project":
        headerData = _extract_header_project(dataFrame, indexRow, indexCol)
    elif cell == "Payroll Number":
        headerData = _extract_header_payroll_number(dataFrame, indexRow, indexCol)
    elif cell == "For Week Ending":
        headerData = _extract_header_week_ending(dataFrame, indexRow, indexCol)

    if headerData:
        header.update(headerData)

    return




def parse_cpr_xlsx_sheet(sheet, pathInputSheet, pathOutputData, pathLogParser):
    dataFrame = pd.read_excel(pathInputSheet, engine='openpyxl', header=None)

    with open(os.path.join(f"{pathOutputData}_frame", f"Frame_{sheet}.txt"), "w") as outputFrame:
        outputFrame.write(dataFrame.to_string(index=True))

    header = {}
    employees = []
    for indexRow in range(1, 4):
        for indexCol in range(dataFrame.shape[1]):
            cell = dataFrame.iat[indexRow, indexCol]

            if isinstance(cell, str):
                _handle_header(cell.strip(), indexRow, indexCol, dataFrame, header)

    indexRow = 7
    for indexCol in range(dataFrame.shape[1]):
        cell = dataFrame.iat[indexRow, indexCol]
        
        if isinstance(cell, str):
            _handle_employees(cell.strip(), indexRow, indexCol, dataFrame, employees, header["week_ending"])

    return dataFrame, header, employees


def parse_cpr_xlsx_bulk(xlsxSheets: list, pathInputData: str, pathOutputData: str,  pathLogParser: str):
    for sheet in xlsxSheets:
        pathInputSheet = os.path.join(pathInputData, sheet)

        try:
            frame, header, employees = parse_cpr_xlsx_sheet(sheet, pathInputSheet, pathOutputData, pathLogParser)
            msg = f"<parse_cpr_xlsx_bulk> Parsed {len(employees)} employees from ({sheet})."
            Util.log_message(Util.STATUS_CODES.PASS, msg, pathLogParser, True)
        except Exception as e:
            msg = f"<parse_cpr_xlsx_bulk> Failed to parse ({sheet}): {e}."
            Util.log_message(Util.STATUS_CODES.ERROR, msg, pathLogParser, True)
            continue

        parsedData = {
            "header": header,
            "employees": employees
}
        with open(os.path.join(f"{pathOutputData}_parse", f"Parsed_{sheet}.json"), "w") as parsedCPR:
            json.dump(parsedData, parsedCPR, indent=2, ensure_ascii=False)
