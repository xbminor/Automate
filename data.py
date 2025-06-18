import pandas as pd
import json




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
    ssns = []
    for i in range(employeeTotal):
        data =  {
            "employee_ssn": dataFrame.iloc[indexRow+1+3*i, indexCol],
        }
        ssns.append(data)

    return ssns




def HandleEmployees(cell, indexRow, indexCol, dataFrame, employees):
    employeeTotal = int((len(dataFrame)-8)/3)
    employeeData = None
    if cell == "Employee Name":
        employeeData = ParseNames(dataFrame, indexRow, indexCol, employeeTotal)
    elif cell == "SSN":
        employeeData = ParseSSN(dataFrame, indexRow, indexCol, employeeTotal)

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
        while len(header) <= 0:
                header.append({})

        header[0].update(headerData)

    return




def parse_cpr_excel(file_path):
    dataFrame = pd.read_excel(file_path, engine='openpyxl', header=None)
    with open("output_logs/dataframe.txt", "w") as f:
        f.write(dataFrame.to_string(index=True))

    header = []
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

    
    for x in header:
        print(x)

    for y in employees:
        print(y)

    return dataFrame





if __name__ == "__main__":
    path = ".\data\CP #16 ending 7.6.24.xlsx"
    parsed_data = parse_cpr_excel(path)

    #print(parsed_data)

    # # Save as JSON
    # with open("employee_data.json", "w") as f:
    #     json.dump(parsed_data, f, indent=2)

    # print(f"Parsed {len(parsed_data)} employees from CPR Excel.")
