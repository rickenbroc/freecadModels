# -*- coding: utf-8 -*-

import argparse
import os.path
import zipfile
import xml.etree.ElementTree as ET
import base64
import re
import sys

__title__ = "Job Fixer"
__author__ = "sliptonic, Russ4262, Gauthier, chrisb"
__doc__ = "Helper script to migrate pre-0.21 Path Job to 0.21 code structure."
__usage__ = 'This script has three modes: in_out, target_directory, and working_directory. Migrated files will created with "_current" suffix added to filename.\
    Usage examples:\
    **Depending on your Python installation, your command might be "python3 ..." instead of "python ..." as seen below.\
    python JobFixerCopy_V5.py -h\
    python JobFixerCopy_V5.py -d "D:\Target\Folder\projects" --s "_fixed"\
    python JobFixerCopy_V5.py -i "D:\Target\Folder\Subfolder\square.FCStd" -o "D:\Target\Folder\Subfolder\square_fixed.FCStd"\
    python JobFixerCopy_V5.py -i "D:\Target\Folder\Subfolder\square.fcstd"\
    python JobFixerCopy_V5.py --s "_fixed"\
    python JobFixerCopy_V5.py -d "%arg1%"\
    python JobFixerCopy_V5.py -i "test.FCStd" -o "test_21.FCStd"\
    '
__created__ = "2022"
__updated__ = "2023-03-19"
__version__ = 7

suffix = "_current"
force = False

objectmaps = {
    "PathScripts.PathAdaptive": "Path.Op.Adaptive",
    "PathScripts.PathCustom": "Path.Op.Custom",
    "PathScripts.PathDeburr": "Path.Op.Deburr",
    "PathScripts.PathDressupDogbone": "Path.Dressup.DogboneII",
    "PathScripts.PathDressupHoldingTags": "Path.Dressup.Tags",
    "PathScripts.PathDrilling": "Path.Op.Drilling",
    "PathScripts.PathEngrave": "Path.Op.Engrave",
    "PathScripts.PathHelix": "Path.Op.Helix",
    "PathScripts.PathIconViewProvider": "Path.Base.Gui.IconViewProvider",
    "PathScripts.PathJob": "Path.Main.Job",
    "PathScripts.PathMillFace": "Path.Op.MillFace",
    "PathScripts.PathPocket": "Path.Op.Pocket",
    "PathScripts.PathPocketShape": "Path.Op.Pocket",
    "PathScripts.PathProbe": "Path.Op.Probe",
    "PathScripts.PathProfile": "Path.Op.Profile",
    "PathScripts.PathProfileContour": "Path.Op.Profile",
    "PathScripts.PathSetupSheet": "Path.Base.SetupSheet",
    "PathScripts.PathSlot": "Path.Op.Slot",
    "PathScripts.PathStock": "Path.Main.Stock",
    "PathScripts.PathSurface": "Path.Op.Surface",
    "PathScripts.PathThreadMilling": "Path.Op.ThreadMilling",
    "PathScripts.PathToolBit": "Path.Tool.Bit",
    "PathScripts.PathToolController": "Path.Tool.Controller",
    "PathScripts.PathVcarve": "Path.Op.Vcarve",
    "PathScripts.PathWaterline": "Path.Op.Waterline",
    "PathScripts.PathComment": "Path.Op.Gui.Comment",
}

viewprovidermaps = {
    "PathScripts.PathAdaptiveGui": "Path.Op.Gui.Adaptive",
    "PathScripts.PathCustomGui": "Path.Op.Gui.Custom",
    "PathScripts.PathDeburrGui": "Path.Op.Gui.Deburr",
    "PathScripts.PathDressupTagGui": "Path.Dressup.Gui.Tags",
    "PathScripts.PathDrillingGui": "Path.Op.Gui.Drilling",
    "PathScripts.PathEngraveGui": "Path.Op.Gui.Engrave",
    "PathScripts.PathHelixGui": "Path.Op.Gui.Helix",
    "PathScripts.PathIconViewProvider": "Path.Base.Gui.IconViewProvider",
    "PathScripts.PathJobGui": "Path.Main.Gui.Job",
    "PathScripts.PathMillFaceGui": "Path.Op.Gui.MillFace",
    "PathScripts.PathOpGui": "Path.Op.Gui.Base",
    "PathScripts.PathPocketGui": "Path.Op.Gui.Pocket",
    "PathScripts.PathPocketShapeGui": "Path.Op.Gui.Pocket",
    "PathScripts.PathProbeGui": "Path.Op.Gui.Probe",
    "PathScripts.PathProfileContourGui": "Path.Op.Gui.Profile",
    "PathScripts.PathProfileGui": "Path.Op.Gui.Profile",
    "PathScripts.PathSetupSheetGui": "Path.Base.Gui.SetupSheet",
    "PathScripts.PathSlotGui": "Path.Op.Gui.Slot",
    "PathScripts.PathSurfaceGui": "Path.Op.Gui.Surface",
    "PathScripts.PathToolBitGui": "Path.Tool.Gui.Bit",
    "PathScripts.PathToolControllerGui": "Path.Tool.Gui.Controller",
    "PathScripts.PathVcarveGui": "Path.Op.Gui.Vcarve",
    "PathScripts.PathWaterlineGui": "Path.Op.Gui.Waterline",
    "PathScripts.PathComment": "Path.Op.Gui.Comment",
}


def cleanupBase64String(base64_string, node):
    """cleanupBase64String(base64_string, node) returns modified Base64 string as necessary and able
    Base64 de/encoding code used from https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/
    """
    # print(f"raw value: {base64_string}")
    base64_bytes = base64_string.encode("ascii")
    string_bytes = base64.b64decode(base64_bytes)
    string = string_bytes.decode("ascii")
    # print(f"Decoded string: {string}")
    if not string.startswith("{") or not string.endswith("}"):
        # print(f"original string: {string}")
        return base64_string

    dictStr = eval(string)
    # print(f"dictStr: {dictStr}")
    if "editModule" in dictStr.keys():
        key = "editModule"
    elif "OpPageModule" in dictStr.keys():
        key = "OpPageModule"
    elif "module" in dictStr.keys():
        key = "module"
    else:
        # print(f"original string: {string}")
        return base64_string

    pathmaps = objectmaps if node == "ObjectData" else viewprovidermaps
    module = dictStr[key]
    if module not in pathmaps:
        print(f"module {module} not substituted")
        return base64_string

    mapout = pathmaps[module]
    dictStr[key] = mapout
    # print(f"NEW pair: editModule: {mapout}")
    asciiStr = "{" + ", ".join([f'"{k}": "{v}"' for k, v in dictStr.items()]) + "}"
    # print(asciiStr)
    new_string_bytes = asciiStr.encode("ascii")
    new_base64_bytes = base64.b64encode(new_string_bytes)
    return new_base64_bytes.decode("ascii")


def cleanupDoc(docxml, node):
    print(f"cleaning {node}")
    tree = ET.parse(docxml)
    root = tree.getroot()

    pathmaps = objectmaps if node == "ObjectData" else viewprovidermaps

    objects = root.find(node)
    for child in objects:
        res = child.findall("./Properties/Property[@name='Proxy']/Python")
        for r in res:
            try:
                modstring = r.attrib["module"]
            except:
                pass
                # print(ET.tostring(r))
            else:
                if modstring not in pathmaps:
                    print(f"module {modstring} not substituted")
                else:
                    # if node =="ViewProviderData" and modstring == "PathScripts.PathOpGui":
                    #    opname = child.attrib['name']
                    #    print(f"Operation node: {opname}")
                    #    if opname == "Slot":
                    #        #mapout = pathmaps[modstring]
                    #        #r.attrib["module"] = f"{mapout}.Slot"
                    #        r.attrib["encoded"] = "no"
                    #        r.attrib["value"] = ""

                    mapout = pathmaps[modstring]
                    # print(f"mapping: {modstring}  to  {mapout}")
                    r.attrib["module"] = mapout
                    r.attrib["value"] = cleanupBase64String(r.attrib["value"], node)
                    # print(f"substituted {mapout} for {modstring}")
                # Eif
            # Etry
        # Efor
    # Efor
    newXML = ET.tostring(root)
    return newXML


def fixFile(filename, newfilename):
    print(f"Input file: {filename}")
    print(f"      Output: {newfilename}")
    mode = "w" if force else "x"
    if os.path.exists(newfilename):
        if mode == "x":
            print("      Output file exists!")
            print("      Consider '--f' command-line argument to force overwriting.")
            return
        else:
            print("      Output file exists and will be overwritten!")
    try:
        with zipfile.ZipFile(filename, "r") as zin:
            with zipfile.ZipFile(newfilename, mode) as zout:
                zout.comment = zin.comment
                for item in zin.infolist():
                    if item.filename == "Document.xml":
                        with zin.open(item.filename) as docxml:
                            newdata = cleanupDoc(docxml, "ObjectData")
                            zout.writestr(item.filename, newdata)
                    elif item.filename == "GuiDocument.xml":
                        with zin.open(item.filename) as docxml:
                            newdata = cleanupDoc(docxml, "ViewProviderData")
                            zout.writestr(item.filename, newdata)
                    else:
                        zout.writestr(item, zin.read(item.filename))
        # Ewith
    except FileExistsError as ee:
        print(f"      ERROR: {ee}")
    except Exception as ee:
        print(f"      ERROR: {ee}")


def getNewFileName(c):
    # Add suffix to filename
    cParts = c.split(".")
    cParts[-2] = cParts[-2] + suffix
    new_file = ".".join(cParts)
    return new_file


def processDirectory(wrkDir, directory=""):
    # print("Processing contents of base directory.")
    if directory != "":
        os.chdir(directory)
        cwd = directory
    else:
        cwd = wrkDir
    contents = os.listdir(cwd)
    # print(f"Contents: {contents}")
    candidates = [
        cnt
        for cnt in contents
        if (str(cnt).endswith(".FCStd") or str(cnt).endswith(".fcstd"))
        and not (
            str(cnt).endswith(suffix + ".FCStd")
            or str(cnt).endswith("_current.FCStd")
            or str(cnt).endswith(suffix + ".fcstd")
            or str(cnt).endswith("_current.fcstd")
        )
    ]
    for c in candidates:
        # print(f"\nCandidate: {c}")
        new_file = getNewFileName(c)
        if os.path.isfile(cwd + "\\" + new_file):
            print(f"Skipping {c}. Already fixed.")
            continue
        fixFile(c, new_file)
    if directory != "":
        os.chdir(wrkDir)


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error(f"The file, '{arg}', does not exist!")
    else:
        return open(arg, "r")  # return an open file handle


def is_valid_directory(parser, arg):
    if arg == "":
        return arg
    elif not os.path.exists(arg):
        parser.error(f"The directory, '{arg}', does not exist!")
    else:
        return arg


def is_valid_suffix(parser, arg):
    if not isinstance(arg, str):
        parser.error(f"The suffix provided is not a string.")
    if len(arg) > 25:
        parser.error(f"The suffix length is greater than 25 characters.")
    if len(arg) < 1:
        parser.error(f"The suffix is empty.")
    if re.search("\W", arg):  # search for non-alphanumeric characters
        parser.error(
            f"The suffix contains illegal characters. Only [a-zA-Z0-9_] permitted."
        )
    else:
        return arg


def getPythonVersion():
    v = sys.version
    return v[: v.index(" ")].split(".")


def getCommandLineArgs():
    ver = getPythonVersion()
    pyVersion = int(ver[0]) * 100 + int(ver[1])

    if pyVersion >= 309:
        # 'exit_on_error' introduced in Python 3.9
        parser = argparse.ArgumentParser(
            exit_on_error=False, description="Fixes FreeCAD Path Jobs"
        )
    else:
        # Any argparse error will force exit of script
        parser = argparse.ArgumentParser(description="Fixes FreeCAD Path Jobs")

    parser.add_argument(
        "-i",
        dest="filename",
        # required=True,
        help="input FreeCAD project file, requires -o",
        metavar="FILE",
        type=lambda x: is_valid_file(parser, x),
    )
    parser.add_argument(
        "-o",
        dest="outputfilename",
        # required=True,
        help="output FreeCAD project file, requires -i",
        metavar="FILE",
    )
    parser.add_argument(
        "-d",
        dest="directory",
        help="directory containing one or more FCStd files, use without -i and -o",
        metavar="DIRECTORY",
        type=lambda x: is_valid_directory(parser, x),
    )
    parser.add_argument(
        "--s",
        dest="suffix",
        help="optional custom suffix for directory files, default='_current', [a-zA-Z0-9_]",
        metavar="SUFFIX",
        default="_current",
        type=lambda x: is_valid_suffix(parser, x),
    )
    parser.add_argument(
        "--f",
        dest="force",
        help="optional force flag to overwrite existing files",
        action="store_true",
    )

    args = parser.parse_args()

    return args


def execute():
    global suffix
    global force

    print(f"\n{__title__}, {__updated__} using Python {'.'.join(getPythonVersion())}")

    cwd = os.getcwd()  # save current working directory
    # print(f"CWD:  {cwd}")

    args = getCommandLineArgs()
    if args is None:
        print("Exiting early due to argument error.")

    if args.suffix:
        suffix = args.suffix
    if not args.outputfilename:
        print(f"Using suffix:  {suffix}")
    if args.force:
        force = True
        print("Forcing overwrite of output file if it exists.")

    if args.directory and not args.filename and not args.outputfilename:
        # print(f"Processing directory provided: {args.directory}")
        processDirectory(cwd, directory=args.directory)
    elif not args.directory and args.filename:
        if args.outputfilename:
            outfilename = args.outputfilename
        else:
            outfilename = getNewFileName(args.filename.name)
        # print(f"Converting {args.filename}  to  {outfilename}")
        fixFile(args.filename.name, outfilename)
    elif not args.directory and not args.filename and not args.outputfilename:
        # print("Processing current working directory.")
        processDirectory(cwd)
    else:
        print(f"Arguments error: Check the arguments and syntax.")


execute()
