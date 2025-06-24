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


        # Starting column of first day of week: Sun-Sat
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
    

        # Starting column of Timesheet Hours
        indexColTimeTotal = indexCol + 8
        rtTime = dataFrame.iloc[indexRow+1+3*i, indexColTimeTotal]
        otTime = dataFrame.iloc[indexRow+2+3*i, indexColTimeTotal]
        dtTime = dataFrame.iloc[indexRow+3+3*i, indexColTimeTotal]

        data["work_time_total_rt"] = emptyCellFloat if pd.isna(rtTime) else float(rtTime)
        data["work_time_total_ot"] = emptyCellFloat if pd.isna(otTime) else float(otTime)
        data["work_time_total_dt"] = emptyCellFloat if pd.isna(dtTime) else float(dtTime)


        # Starting column of Paid Hours
        indexColTimePaid = indexCol + 9
        rtPaid = dataFrame.iloc[indexRow+1+3*i, indexColTimePaid]
        otPaid = dataFrame.iloc[indexRow+2+3*i, indexColTimePaid]
        dtPaid = dataFrame.iloc[indexRow+3+3*i, indexColTimePaid]

        data["work_time_paid_rt"] = emptyCellFloat if pd.isna(rtPaid) else float(rtPaid)
        data["work_time_paid_ot"] = emptyCellFloat if pd.isna(otPaid) else float(otPaid)
        data["work_time_paid_dt"] = emptyCellFloat if pd.isna(dtPaid) else float(dtPaid)


        # Starting column of Pay Rate
        indexColPayRate = indexCol + 10
        rtRate = dataFrame.iloc[indexRow+1+3*i, indexColPayRate]
        otRate = dataFrame.iloc[indexRow+2+3*i, indexColPayRate]
        dtRate = dataFrame.iloc[indexRow+3+3*i, indexColPayRate]

        data["work_pay_rate_rt"] = emptyCellFloat if pd.isna(rtRate) else float(rtRate)
        data["work_pay_rate_ot"] = emptyCellFloat if pd.isna(otRate) else float(otRate)
        data["work_pay_rate_dt"] = emptyCellFloat if pd.isna(dtRate) else float(dtRate)


        # Starting column of Job Gross Pay
        indexColJobGross = indexCol + 11
        grossJob = dataFrame.iloc[indexRow+1+3*i, indexColJobGross]
        data["work_pay_gross_job"] = emptyCellFloat if pd.isna(grossJob) else float(grossJob)

        
        # Starting column of Check Number
        indexColCheckNum = indexCol + 13
        checkNum = dataFrame.iloc[indexRow+1+3*i, indexColCheckNum]
        data["work_pay_check_num"] = emptyCellString if pd.isna(checkNum) else checkNum


        # Starting column of Total Gross Pay
        indexColTotalGross = indexCol + 14
        grossTotal = dataFrame.iloc[indexRow+1+3*i, indexColTotalGross]
        data["work_pay_gross_total"] = emptyCellFloat if pd.isna(grossTotal) else float(grossTotal)


        # Starting column of Social Security Tax
        indexColSocial = indexCol + 15
        taxSocial = dataFrame.iloc[indexRow+1+3*i, indexColSocial]
        data["work_pay_tax_social"] = emptyCellFloat if pd.isna(taxSocial) else float(taxSocial)


        # Starting column of Medicare Tax
        indexColMedicare = indexCol + 16
        taxMedi = dataFrame.iloc[indexRow+1+3*i, indexColMedicare]
        data["work_pay_tax_medic"] = emptyCellFloat if pd.isna(taxMedi) else float(taxMedi)


        # Starting column of Federal Tax
        indexColFederal = indexCol + 17
        taxFed = dataFrame.iloc[indexRow+1+3*i, indexColFederal]
        data["work_pay_tax_fed"] = emptyCellFloat if pd.isna(taxFed) else float(taxFed)


        # Starting column of State Tax
        indexColState = indexCol + 18
        taxState = dataFrame.iloc[indexRow+1+3*i, indexColState]
        data["work_pay_tax_state"] = emptyCellFloat if pd.isna(taxState) else float(taxState)


        # Starting column of Other
        indexColOther = indexCol + 19
        taxOther = dataFrame.iloc[indexRow+1+3*i, indexColOther]
        data["work_pay_tax_other"] = emptyCellFloat if pd.isna(taxOther) else float(taxOther)


        # Starting column of Total Deductions
        indexColDeduct = indexCol + 20
        deductTotal = dataFrame.iloc[indexRow+1+3*i, indexColDeduct]
        data["work_pay_deduction_total"] = emptyCellFloat if pd.isna(deductTotal) else float(deductTotal)


        # Starting column of Net Pay
        indexColNetPay = indexCol + 21
        netPay = dataFrame.iloc[indexRow+1+3*i, indexColNetPay]
        data["work_pay_net"] = emptyCellFloat if pd.isna(netPay) else float(netPay)

        
        data["hours_rt"] = dataWeekRT
        data["hours_ot"] = dataWeekOT
        data["hours_dt"] = dataWeekDT
        
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
            weekEnding = header.get("week_ending")
            if not weekEnding:
                msg = f"<parse_cpr_xlsx_sheet> ({sheet}): Week ending date not found in header."
                Util.log_message(Util.STATUS_CODES.FAIL, msg, pathLogParser, True)
                return None
    
            _handle_employees(cell.strip(), indexRow, indexCol, dataFrame, employees, weekEnding)
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
            Util.log_message(Util.STATUS_CODES.FAIL, msg, pathLogParser, True)
            continue

        parsedData = {
            "header": header,
            "employees": employees
}
        with open(os.path.join(f"{pathOutputData}_parse", f"Parsed_{sheet}.json"), "w") as parsedCPR:
            json.dump(parsedData, parsedCPR, indent=2, ensure_ascii=False)
