from os import popen
"""this script outputs an emacs-org table (simple ascii table with '-' and '|'),
    which is programmatically aggregated.
    Since this is meant to be used in an org-file,
    there is a return statement in the global scope"""

src = "./src/"              # src directory from where files are grabbed
url = "192.168.43.31:/"     # ws domain where files are transferred [col 'esp']
files = popen(f"ls {src}").read().split("\n")[:-1]

webrepl_cli_bin = "/home/$USER/py/esp/webrepl/webrepl_cli.py" # [col 'esp']
# because it sucks to always read, especially with the last '\n'
pop = lambda c: popen(c).read()[:-1].split()
tab = lambda l: "|" + "|".join(l) + "|"   # outputs the table rows -> |x|y|z|
emacs_link = lambda t,l,n: f"[[{t}:{l}][{n}]]"
f_link = lambda l,n: emacs_link("file", l, n)
s_link = lambda l,n: emacs_link("shell", l.split("&")[0] + " &", n)

loc = lambda f: " / ".join([
    pop(f"cat {f} | sed '/^\s*#/d;/^\s*$/d' | wc -l")[0],
    pop(f"cat {f} | wc -w")[0]]).replace(", ", "")

rows = (
    {"head": "files",
     "body": lambda f: f_link(src + f, f),
     "tail": f"[[file:{src}][{src}]]"},
    {"head": "esp",
     "body": lambda f: s_link(f"{webrepl_cli_bin} {src}{f} {url}{f}", "->"),
     "tail": "[[shell:sudo rshell -p /dev/ttyUSB0 -b 115200 &][$]]"},


    {"head": "loc / wc",
     "body": lambda f: loc(src + f),
     "tail": loc(f"{src}*")},
    {"head": "du",
     "body": lambda f: pop(f"du -h {src}{f}")[0],
     "tail": ":=vsum(@2..@-1)"})

def table_as_string():
    return "\n".join(
        (tab(c["head"] for c in rows),
        "|-",
        "\n".join(tab([c["body"](f) for c in rows]) for f in files),
        tab(c["tail"] for c in rows)))

# if __name__ == "__main__":
#     # for emacs-org src_blocks
#     return table_as_string()  +"\n#+TBLFM: @12$3=vsum(@2..@-1)"
#     # to not get en error otherwise
#     # print(table_as_string()
