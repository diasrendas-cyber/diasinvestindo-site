"""Gera uma versão autocontida de uma página (para a prévia no Claude e para os testes).
Uso: python3 tools/preview.py index.html preview.html
Embute /assets/*.css e *.js, remove o script do AdSense e, por padrão, o esqueleto <html>/<head>/<body>
(o artifact do Claude cria o próprio). Com --completo mantém o documento inteiro."""
import os, re, sys
raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src, dst = sys.argv[1], sys.argv[2]
completo = "--completo" in sys.argv
s = open(src, encoding="utf-8").read()
s = re.sub(r"<!-- ADSENSE -->.*?<!-- /ADSENSE -->\n?", "", s, flags=re.S)
def css(m):
    return "<style>\n" + open(os.path.join(raiz, m.group(1).lstrip("/")), encoding="utf-8").read() + "</style>"
def js(m):
    return "<script>\n" + open(os.path.join(raiz, m.group(1).lstrip("/")), encoding="utf-8").read() + "</script>"
s = re.sub(r'<link rel="stylesheet" href="(/assets/[^"]+\.css)">', css, s)
s = re.sub(r'<script src="(/assets/[^"]+\.js)"></script>', js, s)
if not completo:
    s = re.sub(r"^<!doctype html>\s*<html[^>]*>\s*<head>\s*", "", s, flags=re.I)
    s = re.sub(r'<meta charset="utf-8">\s*<meta name="viewport"[^>]*>\s*', "", s)
    s = s.replace("</head>\n<body>\n", "\n", 1)
    s = re.sub(r"</body>\s*</html>\s*$", "", s)
open(dst, "w", encoding="utf-8").write(s)
print("prévia gerada:", dst)
