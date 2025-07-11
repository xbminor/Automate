import os
import re
import shutil
from datetime import datetime, timedelta
from collections import defaultdict



def extract_date(fileName: str):
    """
    Extracts MM.DD.YY from the fileName and returns a datetime object.
    If no valid date is found, returns None.
    """
    match = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{2})', fileName)
    #match = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{2})', fileName)
    if not match:
        return None
    month, day, year = match.groups()
    try:
        return datetime.strptime(f"{month}.{day}.{year}", "%m.%d.%y")
    except ValueError:
        return None


def gui_bulk_file_index_by_date(pathFolderInput: str, pathFolderOutput: str, startIndex: int = 1):
    listFileNames = [f for f in os.listdir(pathFolderInput) if os.path.isfile(os.path.join(pathFolderInput, f))]

    # Group files by date
    dictGroupedFiles = defaultdict(list)
    for fileName in listFileNames:
        dateObj = extract_date(fileName)
        if dateObj:
            dictGroupedFiles[dateObj].append(fileName)
        else:
            print(f"Skipping (no date found): {fileName}")


    sortedDates = sorted(dictGroupedFiles.keys())
    totalGroups = len(sortedDates)
    paddingLength = len(str(startIndex + totalGroups - 1))

    plannedRenames = []
    index = startIndex
    for date in sortedDates:
        listFiles = sorted(dictGroupedFiles[date])
        strIndex = str(index).zfill(paddingLength)
        for fileName in listFiles:
            if fileName.startswith(strIndex + "_"):
                continue
            newFileName = f"{strIndex}_{fileName}"
            plannedRenames.append((fileName, newFileName))
        index += 1

    if not plannedRenames:
        print("No files to rename.")
        return

    for oldName, newName in plannedRenames:
        os.rename(os.path.join(pathFolderInput, oldName), os.path.join(pathFolderOutput, newName))
    
    print("Operation complete.")



def bulk_cpr_index_by_order(folderPath, index, indexPrecision):

    listFileNames = [f for f in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, f))]

    pattern = re.compile(r'^\d+_(\d+)_([\d\-]+)_PRRUN(\d+)(?: (NP))?\.pdf$')

    listFilesRenamed = []
    for fileName in listFileNames:
        match = pattern.search(fileName)
        if match:
            project = dictProjectNames.get(match.group(1), f"Unknown Project")
            date = datetime.strptime(match.group(2), "%Y-%m-%d").strftime("%m.%d.%y")
            prrun = match.group(3)
            suffixNP = " NP" if match.group(4) else ""

            formattedIndex = f"{index:0{indexPrecision}}"
            newFileName = f"eCPR {formattedIndex} {project} ending {date} PRRUN{prrun}{suffixNP}.pdf"
            listFilesRenamed.append((fileName, newFileName))
            index += 1

    
    maxLenOld = max(len(old) for old, _ in listFilesRenamed)
    maxLenNew = max(len(new) for _, new in listFilesRenamed)
    arrow = ' → '
    contentWidth = maxLenOld + len(arrow) + maxLenNew

    print('╭' + '─' * (contentWidth+2) + '╮')
    print(f"│ {'Planned Renames:'.ljust(contentWidth+1)}│")
    print('├' + '─' * (contentWidth+2) + '┤')
    for oldName, newName in listFilesRenamed:
        line = f"{oldName.ljust(maxLenOld)}{arrow}{newName.ljust(maxLenNew)}"
        print(f"│ {line.ljust(contentWidth)} │")
    print('╰' + '─' * (contentWidth+2) + '╯')
        
    choice = input("\nProceed with renaming? (y/n): ").strip().lower()
    if choice != "y":
        print("Operation canceled.\n")
        return
    
    for oldName, newName in listFilesRenamed:
        oldPath = os.path.join(folderPath, oldName)
        newPath = os.path.join(folderPath, newName)

        os.rename(oldPath, newPath)
    
    print("Operation complete.\n")


def convert_year_to_two_digits(folderPath: str, dryRun: bool = True):
    """
    Converts 4-digit years to 2-digit years in filenames with 'ending MM.DD.YYYY'.
    Example: 'eCPR 05 Project ending 07.06.2024 PRRUNxxxxx.pdf' -> 'eCPR 05 Project ending 07.06.24 PRRUNxxxxx.pdf'

    Args:
        folderPath (str): Path to folder containing files.
        dryRun (bool): If True, previews changes without renaming files.
    """
    pattern = re.compile(r'(ending \d{2}\.\d{2})\.(\d{4})(\b)')

    listFilesRenamed = []
    
    for filename in os.listdir(folderPath):
        if not filename.lower().endswith(".pdf"):
            continue

        match = pattern.search(filename)
        if match:
            yearFull = match.group(2)
            yearShort = yearFull[-2:]
            newFilename = pattern.sub(rf'\1.{yearShort}\3', filename)

            if newFilename != filename:
                listFilesRenamed.append((filename, newFilename))
                if not dryRun:
                    os.rename(os.path.join(folderPath, filename), os.path.join(folderPath, newFilename))

    # Show preview box
    if listFilesRenamed:
        arrow = ' → '
        maxLenOld = max(len(old) for old, _ in listFilesRenamed)
        maxLenNew = max(len(new) for _, new in listFilesRenamed)
        contentWidth = maxLenOld + len(arrow) + maxLenNew

        print('╭' + '─' * (contentWidth + 2) + '╮')
        print(f"│ {'Renamed Files (dry run)'.ljust(contentWidth + 1) if dryRun else 'Renamed Files:'.ljust(contentWidth + 1)}│")
        print('├' + '─' * (contentWidth + 2) + '┤')
        for oldName, newName in listFilesRenamed:
            line = f"{oldName.ljust(maxLenOld)}{arrow}{newName.ljust(maxLenNew)}"
            print(f"│ {line.ljust(contentWidth)} │")
        print('╰' + '─' * (contentWidth + 2) + '╯')
    else:
        print("No files needed renaming.")





def bulk_copy_cpr_np(folderPath: str, rangeN: int):

    # INPUT CONFIGURATION
    listCPR = os.listdir(folderPath)
    cprFile = listCPR[0]
    cprName = str(cprFile)
    endDateTarget = datetime.strptime("2024-03-23", "%Y-%m-%d")

    # Parse current date from filename
    parts = cprName.split("_")
    datePart = parts[2]  # e.g. '2024-11-16'
    currentDate = datetime.strptime(datePart, "%Y-%m-%d")

    print(currentDate, endDateTarget)
    pathFolderNew = f"{folderPath}\Copies"

    # Loop backward and create renamed copies
    for i in range(rangeN):
        newDateStr = currentDate.strftime("%Y-%m-%d")
        newFileName = cprName.replace(datePart, newDateStr)
    
        pathOld = os.path.join(folderPath, cprName)
        pathNew = os.path.join(pathFolderNew, newFileName)
    
        shutil.copyfile(pathOld, pathNew)
        print(f"Created: {newFileName}")
    
        currentDate -= timedelta(days=7)




if __name__ == "__main__":
    pathFolderFiles = r".\FilesToIndex"
    pathFolderCPRs = r".\CPRsToIndex"
    pathFolderNPs = r".\CPRsToCopyNP"
    pathFolderTemp = r".\Temp"
    indexFile = 1
    #bulk_file_index_by_date(pathFolderFiles, indexFile)

    indexCPR = 1
    indexPrecision = 2
    bulk_cpr_index_by_order(pathFolderCPRs, indexCPR, indexPrecision)

    #convert_year_to_two_digits(pathFolderTemp, False

    rangeNum = 3
    #bulk_copy_cpr_np(pathFolderNPs, rangeNum)