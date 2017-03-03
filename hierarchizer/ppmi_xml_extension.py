from defusedxml import ElementTree
from os import path
from glob import iglob

MAPPING = {"StudyID": "./study", "SeriesNumber": "./series"}


def find(file_path, attribute):
    xml_file = find_xml(path.dirname(file_path))
    if xml_file:
        tree = ElementTree.parse(xml_file)
        try:
            return tree.find(MAPPING[attribute]).attrib['uid']
        except (KeyError, AttributeError):
            return None


def find_xml(folder):
    for file_path in iglob(path.join(folder, "**/*.xml"), recursive=True):
        return file_path
