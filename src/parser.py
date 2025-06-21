import pandas as pd
import json
import os




def ParseContractor(dataFrame, indexRow, indexCol):
    data =  {
        "contractor_name": dataFrame.iloc[indexRow, indexCol+2],
        "contractor_address1": dataFrame.iloc[indexRow+1, indexCol+2],
        "contractor_address2": dataFrame.iloc[indexRow+2, indexCol+2],
    }

    return data


def ParseProject(dataFrame, indexRow, indexCol):
    data =  {
        "project_name": dataFrame.iloc[indexRow, indexCol+1],
    }

    return data


def ParsePayrollNumber(dataFrame, indexRow, indexCol):
    data =  {
        "payroll_number": dataFrame.iloc[indexRow, indexCol+3],
    }

    return data


def ParseWeekEnding(dataFrame, indexRow, indexCol):
    data =  {
        "week_ending": dataFrame.iloc[indexRow, indexCol+3].date().isoformat(),
    }

    return data




def ParseNames(dataFrame, indexRow, indexCol, employeeTotal):
    names = []
    for i in range(employeeTotal):
        data = {
            "employee_name": dataFrame.iloc[indexRow+1+3*i, indexCol],
            "employee_address1": dataFrame.iloc[indexRow+2+3*i, indexCol],
            "employee_address2": dataFrame.iloc[indexRow+3+3*i, indexCol],
        }
        names.append(data)

    return names


def ParseSSN(dataFrame, indexRow, indexCol, employeeTotal):
    output = []
    for i in range(employeeTotal):
        data =  {
            "employee_ssn": dataFrame.iloc[indexRow+1+3*i, indexCol],
        }
        output.append(data)

    return output


def ParseClassification(dataFrame, indexRow, indexCol, employeeTotal):
    output = []
    for i in range(employeeTotal):
        data =  {
            "work_classification": dataFrame.iloc[indexRow+1+3*i, indexCol],
        }
        output.append(data)

    return output




def HandleEmployees(cell, indexRow, indexCol, dataFrame, employees):
    employeeTotal = int((len(dataFrame)-8)/3)
    employeeData = None
    if cell == "Employee Name":
        employeeData = ParseNames(dataFrame, indexRow, indexCol, employeeTotal)
    elif cell == "SSN":
        employeeData = ParseSSN(dataFrame, indexRow, indexCol, employeeTotal)
    elif cell == "Classification":
        employeeData = ParseClassification(dataFrame, indexRow, indexCol, employeeTotal)

    if employeeData:
        for i in range(employeeTotal):
            while len(employees) <= i:
                employees.append({})

            employees[i].update(employeeData[i])

    return


def HandleHeader(cell, indexRow, indexCol, dataFrame, header):
    headerData = None
    if cell == "Contractor":
        headerData = ParseContractor(dataFrame, indexRow, indexCol)
    elif cell == "Project":
        headerData = ParseProject(dataFrame, indexRow, indexCol)
    elif cell == "Payroll Number":
        headerData = ParsePayrollNumber(dataFrame, indexRow, indexCol)
    elif cell == "For Week Ending":
        headerData = ParseWeekEnding(dataFrame, indexRow, indexCol)

    if headerData:
        header.update(headerData)

    return




def parse_cpr_excel(sheet, pathInputSheet, pathOutputData):
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
                HandleHeader(cell, indexRow, indexCol, dataFrame, header)
            elif indexRow >= 7:
                HandleEmployees(cell, indexRow, indexCol, dataFrame, employees)


    return dataFrame, header, employees


def CPRxlsxBulk(xlsxSheets: list, pathInputData: str, pathOutputData: str,  pathLogParser: str):
    for sheet in xlsxSheets:
        pathInputSheet = os.path.join(pathInputData, sheet)


        try:
            frame, header, employees = parse_cpr_excel(sheet, pathInputSheet, pathOutputData)
            print(f"Parsed {len(employees)} employees from {sheet}")
        except Exception as e:
            print(f"Failed to parse {sheet}: {e}")
            continue

        parsedData = {
            "header": header,
            "employees": employees
}
        with open(os.path.join(f"{pathOutputData}_parse", f"Parsed_{sheet}.json"), "w") as parsedCPR:
            json.dump(parsedData, parsedCPR, indent=2, ensure_ascii=False)
