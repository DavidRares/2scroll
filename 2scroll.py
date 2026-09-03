import os
import sys
import requests
from lxml import etree

def main():
    argc = len(sys.argv)
    if argc != 2:
        raise Exception("Please provide a single CTS URN.")

    work_urn = sys.argv[1]
    namespace, text_group, work, version = validate_urn(work_urn)

    work_url = f"https://raw.githubusercontent.com/PerseusDL/canonical-{namespace}/refs/heads/master/data/{text_group}/{work}/{text_group}.{work}.{version}.xml"
    work_path = f"works/{text_group}.{work}.{version}.xml"

    if not os.path.exists(work_path):
        print("fetching...")
        fetch_work_xml(work_url, work_path)

    xml_parser = etree.XMLParser(remove_comments = True, ns_clean = True, remove_blank_text = True, remove_pis = True)
    xml_tree = etree.parse(work_path, xml_parser)

    root = xml_tree.getroot()
    ns_uri = etree.QName(root).namespace
    ns = {"tei": ns_uri}

    title_data = fetch_title_stmt_data(xml_tree, ns)
    print(title_data["title"])

def validate_urn(urn):
    #valid example urn:cts:greekLit:tlg0007.tlg097.perseus-eng1

    if not urn.startswith("urn:cts:"):
        raise Exception(f"CTS URN does not start with \"urn:cts:\".")

    urn_arr = urn.split(":")

    if len(urn_arr) != 4:
        raise Exception("CTS URN either too short or too long.")
    
    CANONICAL_LIT = ["greekLit", "latinLit"]
    if urn_arr[2] not in CANONICAL_LIT:
        raise Exception("CTS URN not in canonical literatures.")

    work_id_arr = urn_arr[3].split(".")

    if len(work_id_arr) != 3:
        raise Exception("work_id improperly formatted.")
    
    WORK_PREFIX = ["phi", "tlg"]
    if not work_id_arr[0].startswith(tuple(WORK_PREFIX)) or not work_id_arr[1].startswith(tuple(WORK_PREFIX)) or not work_id_arr[2].startswith("perseus-"):
        raise Exception("work_id not valid.")

    return urn_arr[2], work_id_arr[0], work_id_arr[1], work_id_arr[2]

def fetch_work_xml(url, path):
    response = requests.get(url)
    response.raise_for_status()

    os.makedirs("works", exist_ok = True)

    with open(path, "wb") as f:
        f.write(response.content)

def fetch_title_stmt_data(xml_tree, ns):
    title_stmt = xml_tree.find(".//tei:titleStmt", namespaces=ns)

    if title_stmt is None:
        raise Exception("No title statement found.")

    return {
        child.tag.split("}")[-1]: " ".join(child.itertext()).strip()
        for child in title_stmt
    }

if __name__ == "__main__":
    main()