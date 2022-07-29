import json


def read_json():
    with open("./config.json", "r") as f:
        return json.load(f)


class Utility:
    def ConvertToArrayASCII(content): return[ord(c) for c in content]

    def ConvertToASCII(content): return "".join(str(ord(c)) for c in content)

    def ConvertToString(ary_ASCII): return "".join(chr(i) for i in ary_ASCII)

    def getCacheMaxSize():
        config = read_json()
        return config["cacheMaxSize"]

    def getCacheMode():
        config = read_json()
        return config["cacheMode"]
