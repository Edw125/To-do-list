
def parse_str(text: str) -> None | dict:
    try:
        split = text.split(";")
        if len(split) < 1:
            return
        res = {}
        for i in split:
            i = i.strip().split(":")
            res.update({i[0].strip(): i[1].strip()})
        return res
    except Exception:
        pass
