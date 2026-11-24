"""Map suspicious strings to CyberChef recipes + build shareable CyberChef URLs."""
import base64, json, urllib.parse

RECIPES = {
  "powershell-base64": [{"op":"From Base64","args":["A-Za-z0-9+/=","false"]},{"op":"Decode text","args":["UTF-16LE (1200)"]}],
  "base64": [{"op":"From Base64","args":["A-Za-z0-9+/=","false"]},{"op":"Decode text","args":["UTF-8"]}],
  "hex": [{"op":"From Hex","args":["Auto"]}],
  "url-decode": [{"op":"URL Decode","args":[]}],
  "rot13": [{"op":"ROT13","args":[True,True,False,13]}],
  "reverse": [{"op":"Reverse","args":["Character"]}],
  "xor-brute": [{"op":"XOR Brute Force","args":[1,{"option":"Printable","string":""},True,True,False,"",False]}],
  "jwt": [{"op":"JWT Decode","args":[]}],
  "unix-timestamp": [{"op":"From UNIX Timestamp","args":["Seconds"]}],
}

def suggest_recipe(s: str) -> str:
    low=s.lower()
    if "-enc" in low or "frombase64string" in low: return "powershell-base64"
    if "jwt" in low or s.count(".")==2: return "jwt"
    if "%" in s and ("http" in low or "%3" in low): return "url-decode"
    if re_hex(s): return "hex"
    if len(s)>40: return "base64"
    return "base64"

def re_hex(s: str):
    import re
    return bool(re.search(r"\b[0-9a-fA-F]{32,}\b", s))

def build_cyberchef_url(recipe_name: str, input_text: str) -> str:
    recipe=RECIPES.get(recipe_name, RECIPES["base64"])
    payload={"recipe":json.dumps(recipe),"input":base64.b64encode(input_text.encode()).decode(),"inputType":"base64"}
    frag=base64.b64encode(json.dumps(payload).encode()).decode()
    return f"https://gchq.github.io/CyberChef/#{frag}"
