import src.util as Util
import pandas as pd
import json
import os




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




def _handle_employees(cell, indexRow, indexCol, dataFrame, employees):
    employeeTotal = int((len(dataFrame)-8)/3)
    employeeData = None
    if cell == "Employee Name":
        employeeData = _extract_employee_info(dataFrame, indexRow, indexCol, employeeTotal)
    elif cell == "SSN":
        employeeData = _extract_employee_social(dataFrame, indexRow, indexCol, employeeTotal)
    elif cell == "Classification":
        employeeData = _extract_employee_work_class(dataFrame, indexRow, indexCol, employeeTotal)

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




def parse_cpr_xlsx_sheet(sheet, pathInputSheet, pathOutputData):
    dataFrame = pd.read_excel(pathInputSheet, engine='openpyxl', header=None)

    with open(os.path.join(f"{pathOutputData}_frame", f"Frame_{sheet}.txt"), "w") as outputFrame:
        outputFrame.write(dataFrame.to_string(index=True))

    header = {}
    employees = []
    for indexRow in range(0, len(dataFrame)):
        for indexCol in range(0, len(dataFrame.columns)):
            cell = dataFrame.iloc[indexRow, indexCol]

            if pd.isna(cell):
                continue

            if not isinstance(cell, str):
                continue
                
            cell = cell.strip()
            if indexRow < 7:
                _handle_header(cell, indexRow, indexCol, dataFrame, header)
            elif indexRow >= 7:
                _handle_employees(cell, indexRow, indexCol, dataFrame, employees)


    return dataFrame, header, employees


def parse_cpr_xlsx_bulk(xlsxSheets: list, pathInputData: str, pathOutputData: str,  pathLogParser: str):
    for sheet in xlsxSheets:
        pathInputSheet = os.path.join(pathInputData, sheet)

        try:
            frame, header, employees = parse_cpr_xlsx_sheet(sheet, pathInputSheet, pathOutputData)
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
