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


def _extract_date(fileName: str):
    match = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{2,4})', fileName)
    if not match:
        return None
    month, day, year = match.groups()
    try:
        return datetime.strptime(f"{month}.{day}.{year}", "%m.%d.%y")
    except ValueError:
        return None


def gui_indexer(_pathInputFolder: str, _pathOutputFolder: str, _indexStart: int=1, _indexPrecision: int=2):
    listFileNames = [f for f in os.listdir(_pathInputFolder) if os.path.isfile(os.path.join(_pathInputFolder, f))]
    dictGroupedFiles = defaultdict(list)
    for fileName in listFileNames:
        dateObj = _extract_date(fileName)
        if dateObj:
            dictGroupedFiles[dateObj].append(fileName)
        else:
            print(f"Skipping (no date found): {fileName}")
    sortedDates = sorted(dictGroupedFiles.keys())


    index = _indexStart
    for date in sortedDates:
        for fileNameInput in sorted(dictGroupedFiles[date]):
            indexFormatted = f"{index:0{_indexPrecision}}"
            fileNameOutput = f"{indexFormatted}_{fileNameInput}"

            pathInputFile = os.path.join(_pathInputFolder, fileNameInput)
            pathOutputFile = os.path.join(_pathOutputFolder, fileNameOutput)

            try:
                shutil.copy2(pathInputFile, pathOutputFile)
                print(f"Indexed: {fileNameInput} → {fileNameOutput}")
            except Exception as e:
                print(f"Failed to index {fileNameInput}: {e}")
        index += 1
    
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