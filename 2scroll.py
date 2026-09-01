import sys
import requests

def main():
    argc = len(sys.argv)
    if argc != 2:
        raise Exception("Please provide a single CTS URN.")

    work_urn = sys.argv[1]
    namespace, text_group, work, version = validate_urn(work_urn)

    work_url = f"https://raw.githubusercontent.com/PerseusDL/canonical-{namespace}/refs/heads/master/data/{text_group}/{work}/{text_group}.{work}.{version}.xml"

    fetch_work_xml(work_url, f"{text_group}.{work}.{version}.xml")

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

def fetch_work_xml(url, filename):

    response = requests.get(url)
    response.raise_for_status()

    with open(filename, "wb") as f:
        f.write(response.content)

if __name__ == "__main__":
    main()