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



def HandleHeader(cell, indexRow, indexCol, dataFrame):
    cell = cell.strip()
    output = False
    if cell == "Contractor":
        output = ParseContractor(dataFrame, indexRow, indexCol)
    elif cell == "Project":
        output = ParseProject(dataFrame, indexRow, indexCol)
    elif cell == "Payroll Number":
        output = ParsePayrollNumber(dataFrame, indexRow, indexCol)
    elif cell == "For Week Ending":
        output = ParseWeekEnding(dataFrame, indexRow, indexCol)


    if output: print(output)

    return





def ParseNames(dataFrame, indexRow, indexCol):
    totalNames = int((len(dataFrame)-indexRow-1)/3)

    employees = {}
    for i in range(totalNames):
        employee = {
            "employee_name": dataFrame.iloc[indexRow+1+3*i, indexCol],
            "employee_address1": dataFrame.iloc[indexRow+2+3*i, indexCol],
            "employee_address2": dataFrame.iloc[indexRow+3+3*i, indexCol],
        }
        print(employee)

        employees[employee["employee_name"]] = employee

    return employees



def ParseSSN(dataFrame, indexRow, indexCol):
    data =  {
        "employee_ssn": dataFrame.iloc[indexRow+1, indexCol],
    }

    return data



def HandleEmployees(cell, indexRow, indexCol, dataFrame):
    cell = cell.strip()
    output = False
    if cell == "Employee Name":
        output = ParseNames(dataFrame, indexRow, indexCol)
    elif cell == "SSN":
        output = ParseSSN(dataFrame, indexRow, indexCol)


    if output: print(output)

    return





def parse_cpr_excel(file_path):
    # Load the file raw to search for where the table starts
    dataFrame = pd.read_excel(file_path, engine='openpyxl', header=None)
    with open("output_logs/dataframe.txt", "w") as f:
        f.write(dataFrame.to_string(index=True))


    # Compare cell to neighbor on the left
    for indexRow in range(0, len(dataFrame)):
        for indexCol in range(0, len(dataFrame.columns)):
            cell = dataFrame.iloc[indexRow, indexCol]

            if pd.isna(cell):
                continue

            if not isinstance(cell, str):
                continue

            if indexRow < 7:
                HandleHeader(cell, indexRow, indexCol, dataFrame)
            elif indexRow >= 7:
                HandleEmployees(cell, indexRow, indexCol, dataFrame)

                
    return dataFrame





if __name__ == "__main__":
    path = ".\data\CP #16 ending 7.6.24.xlsx"
    parsed_data = parse_cpr_excel(path)

    #print(parsed_data)

    # # Save as JSON
    # with open("employee_data.json", "w") as f:
    #     json.dump(parsed_data, f, indent=2)

    # print(f"Parsed {len(parsed_data)} employees from CPR Excel.")
