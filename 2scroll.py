import sys


def main():
    argc = len(sys.argv)
    if argc != 2:
        raise Exception("Please provide a single CTS URN.")

    urn = sys.argv[1]
    validate_urn(urn)


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

    
if __name__ == "__main__":
    main()