import collections
import re
import zipfile

for f in ("submission/buicongdat-front.zip", "submission/buicongdat-fisheye.zip"):
    text = zipfile.ZipFile(f).read("annotations.xml").decode()
    blocks = re.findall(r"<image\b.*?</image>", text, re.S)
    core, extra = [], []
    for b in blocks:
        slot = re.search(r'name="data/([AB]\d\d)', b).group(1)
        n = int(slot[1:])
        is_core = (slot[0] == "A" and n <= 12) or (slot[0] == "B" and n <= 8)
        (core if is_core else extra).append(b)
    for label, group in (("core", core), ("extra", extra)):
        joined = "".join(group)
        c = collections.Counter(re.findall(r'<(?:polyline|polygon|box) label="(\w+)"', joined))
        tags = len(re.findall(r"<tag\b", joined))
        print(f, label, "| anh:", len(group), "| nhan:", dict(c), "| tags:", tags, "| tong:", sum(c.values()) + tags)
