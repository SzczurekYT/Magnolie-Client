import datetime
from textwrap import indent
from turtle import update
import requests as rq
from pathlib import Path
import json
import os
from io import BytesIO
import zipfile
import subprocess
import shutil
from getpass import getuser
from loadAnim import LoadAnim

# Define consts
user = getuser()
modpackDir = Path(f"C:\\Users\\{user}\\AppData\\Roaming\\.minecraft\\Profile\\MagnolieSMP6")
forgePath = Path(f"C:\\Users\\{user}\\AppData\\Roaming\\.minecraft\\versions\\1.18.1-forge-39.0.75\\1.18.1-forge-39.0.75.json")
versionFile = Path(f"C:\\Users\\{user}\\AppData\\Roaming\\.minecraft\\Profile\\MagnolieSMP6\\versions.json")
javaw = Path(f"C:\\Users\\{user}\\AppData\\Roaming\\.minecraft\\Profile\\MagnolieSMP6\\graalvm-ce-java17-22.0.0.2\\bin\\javaw.exe")
mcLauncherProfiles = Path(f"C:\\Users\\{user}\\AppData\\Roaming\\.minecraft\\launcher_profiles.json")
mcLauncherTemplate = "https://raw.githubusercontent.com/SzczurekYT/Magnolie-Client/main/profile.json"
versionsUrl = "https://raw.githubusercontent.com/SzczurekYT/Magnolie-Client/main/versions.json"
javaURL = "https://github.com/graalvm/graalvm-ce-builds/releases/download/vm-22.0.0.2/graalvm-ce-java17-windows-amd64-22.0.0.2.zip"
forgeURL = "https://maven.minecraftforge.net/net/minecraftforge/forge/1.18.1-39.0.75/forge-1.18.1-39.0.75-installer.jar"
bstringMc = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACABAMAAAAxEHz4AAAAGFBMVEUAAAA4NCrb0LTGvKW8spyAem2uppSakn5SsnMLAAAAAXRSTlMAQObYZgAAAJ5JREFUaIHt1MENgCAMRmFWYAVXcAVXcAVXcH3bhCYNkYjcKO8dSf7v1JASUWdZAlgb0PEmDSMAYYBdGkYApgf8ER3SbwRgesAf0BACMD1gB6S9IbkEEBfwY49oNj4lgLhA64C0o9R9RABTAvp4SX5kB2TA5y8EEAK4pRrxB9QcA4QBWkj3GCAMUCO/xwBhAI/kEsCagCHDY4AwAC3VA6t4zTAMj0OJAAAAAElFTkSuQmCC"

remVersions = rq.get(versionsUrl).json()
cid = remVersions["client6id"]
cname = remVersions["client6name"]

modpackURL = f"https://www.dropbox.com/s/{cid}/{cname}?dl=1"


def animBufferDownload(url):
    req = rq.get(url, stream= True)
    buffer = BytesIO()
    size = req.headers.get("content-length", None)
    mbsize = "¯\_(ツ)_/¯ "
    if size != None:
        mbsize = int(int(size) / 1048576)
    i = 0
    for chunk in req.iter_content(chunk_size=1024 * 1024):
        if chunk:
            i += 1
            buffer.write(chunk)
            print(f"Pobrano {i}mb z {mbsize}mb.", end="\r")
    return buffer



def installModpack():
    print("Pobieranie modpacka: ")

    # Tworzenie folderu na modpack
    print("Tworzenie folderu na mody")
    os.makedirs(modpackDir, exist_ok=True)

    # Pobieranie javy
    if not javaw.is_file():
        print("Pobieranie Javy")
        print("To może chwilę potrwać")
        zip = zipfile.ZipFile(animBufferDownload(javaURL))
        print("Pobrano javę")
        zip.extractall(modpackDir)
        print("Wypakowano jave")
    else:
        print("Java już jest")

    # Pobieranie i instalowanie forge.
    if not forgePath.is_file():
        print("Pobieranie forge")
        with open(modpackDir / "forge.jar", "wb") as file:
            file.write(rq.get(forgeURL).content)
        
        print("Teraz będziesz musiał kliknąć przycisk \"Ok\"")
        args = [javaw, "-jar", modpackDir / "forge.jar"]
        subprocess.run(args)
        os.remove(modpackDir / "forge.jar")
        print("Forge powinien być gotowy")
    else:
        print("Forge jest")

    # Pobieranie i rozpakowanie modpacku
    print("Pobieranie modpacka")
    print("To może chwilę potrwać")

    zip = zipfile.ZipFile(animBufferDownload(modpackURL))
    print("Pobrano modpack")
    zip.extractall(modpackDir)
    print("Wypakowano modpack")

    print("Zapisywanie wersji")
    with open(versionFile, "w") as f:
        json.dump(rq.get(versionsUrl).json(), f)
    print("Wersja zapisana!")

    
    print("Tworzenie profilu na minecraftowy launcher.")
    with open(mcLauncherProfiles, "r") as f:
        prof = json.load(f)
    print(type(prof))
    template = rq.get(mcLauncherTemplate).json()
    template["gameDir"] = str(modpackDir)
    template["javaDir"] = str(javaw)
    template["lastUsed"] = datetime.datetime.now().isoformat()
    template["created"] = datetime.datetime.now().isoformat()
    prof["profiles"].update({"magnoliesmp6": template})
    with open(mcLauncherProfiles, "w") as f:
        json.dump(prof, f, indent=2)
    

def updateModpack():
    print("Aktualizowanie modpacka")

    # Delete mods
    print("Usuwanie modów.")
    shutil.rmtree(modpackDir / "mods")
    
    # Pobieranie i rozpakowanie modpacku
    print("Pobieranie modpacka")
    print("To może chwilę potrwać")

    zip = zipfile.ZipFile(animBufferDownload(modpackURL))
    print("Pobrano modpack")
    zip.extractall(modpackDir)
    print("Wypakowano modpack")

    print("Zapisywanie wersji")
    with open(versionFile, "w") as f:
        json.dump(rq.get(versionsUrl).json(), f)
    print("Wersja zapisana!")

       



if __name__ == "__main__":
    print("Sprawdzam twoją wersję modpacka!")

    if versionFile.is_file():
        print("Modpack jest pobrany sprawdzam wersję.")
        with open(versionFile, "r") as f:
            locVersions = json.load(f)
            if remVersions["client6"] > locVersions["client6"]:
                updateModpack()
                input("Gotowe, kliknij enter by zakończyć!")
    else:
        # No modpack installed
        installModpack()
        input("Gotowe, kliknij enter by zakończyć!")





# bstring = "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"