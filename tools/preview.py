"""Gera a versão de prévia (artifact do Claude) a partir do index.html.
Uso: python3 tools/preview.py index.html preview.html
A prévia não leva <!doctype>, <html>, <head>, <body> nem o script do AdSense (bloqueado no Claude)."""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
s = re.sub(r"<!-- ADSENSE -->.*?<!-- /ADSENSE -->\n?", "", s, flags=re.S)
s = re.sub(r"^<!doctype html>\s*<html[^>]*>\s*<head>\s*", "", s, flags=re.I)
s = re.sub(r'<meta charset="utf-8">\s*<meta name="viewport"[^>]*>\s*', "", s)
s = s.replace("</head>\n<body>\n", "\n", 1)
s = re.sub(r"</body>\s*</html>\s*$", "", s)
open(dst, "w", encoding="utf-8").write(s)
print("prévia gerada:", dst)
