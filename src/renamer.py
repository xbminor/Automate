import os
import re
import shutil
from datetime import datetime, timedelta
from collections import defaultdict


dictProjectNames = {
    "506809" : "Sanger Complex III",
    "506782" : "Sanger Aquatics",
    "496589" : "Parlier High",
    "493551" : "Avenal Tamarack",
}


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


def gui_bulk_file_index_by_date(pathFolderInput: str, startIndex: int = 1):
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
        os.rename(os.path.join(pathFolderInput, oldName), os.path.join(pathFolderInput, newName))
    
    print("Operation complete.")



def gui_bulk_cpr_index_by_order(folderPath, index, indexPrecision):
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

    if not listFilesRenamed:
        print("No files to rename.")
        return
    
    for oldName, newName in listFilesRenamed:
        oldPath = os.path.join(folderPath, oldName)
        newPath = os.path.join(folderPath, newName)
        os.rename(oldPath, newPath)
        print(f"Renamed: {oldPath} -> {newPath}")
    
    print("Operation complete.\n")



def gui_bulk_cpr_copy(_pathInputFile: str, _pathOutputFolder: str, _weeksToCountBack: int=1):
    if not os.path.exists(_pathInputFile) or not os.path.exists(_pathOutputFolder):
        return None
    
    fileName = os.path.basename(_pathInputFile)

    fileNameParts = fileName.split("_")
    fileNameDate = fileNameParts[2]
    dateStart = datetime.strptime(fileNameDate, "%Y-%m-%d")

    # Loop backward and create renamed copies
    for i in range(_weeksToCountBack):
        dateOutput = dateStart.strftime("%Y-%m-%d")
        fileNameOutput = fileName.replace(fileNameDate, dateOutput)
        pathOutputFile = os.path.join(_pathOutputFolder, fileNameOutput)
    
        shutil.copyfile(_pathInputFile, pathOutputFile)
        print(f"Created: {fileNameOutput}")
    
        dateStart -= timedelta(days=7)

    print("Operation complete.\n")