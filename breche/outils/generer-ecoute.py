#!/usr/bin/env python3
"""Brèche · génère la capture du lab « L'écoute » (module 2), sans dépendance.
Usage : python3 generer-ecoute.py ../plateforme/fichiers/ecoute.pcap"""
import struct, sys

DRAPEAU = "BRECHE{http_3n_cl41r_c_3st_un3_c4rt3_p0st4l3}"
MAC_PC, MAC_IMP, MAC_GW = bytes.fromhex("3c5282a1b2c3"), bytes.fromhex("0017c8445566"), bytes.fromhex("f4ca e5 00 11 22".replace(" ", ""))
IP_PC, IP_IMP, IP_DNS = "10.20.0.42", "10.20.0.15", "10.20.0.1"

def ip4(a): return bytes(int(x) for x in a.split("."))
def somme(b):
    if len(b) % 2: b += b"\0"
    s = sum(struct.unpack(f"!{len(b)//2}H", b))
    while s >> 16: s = (s & 0xFFFF) + (s >> 16)
    return ~s & 0xFFFF

def ip(src, dst, proto, charge, ident):
    h = struct.pack("!BBHHHBBH4s4s", 0x45, 0, 20 + len(charge), ident, 0x4000, 64, proto, 0, ip4(src), ip4(dst))
    h = h[:10] + struct.pack("!H", somme(h)) + h[12:]
    return h + charge

def tcp(src, dst, sp, dp, seq, ack, drapeaux, donnees=b""):
    h = struct.pack("!HHIIBBHHH", sp, dp, seq, ack, 5 << 4, drapeaux, 64240, 0, 0)
    pseudo = ip4(src) + ip4(dst) + struct.pack("!BBH", 0, 6, len(h) + len(donnees))
    c = somme(pseudo + h + donnees)
    return h[:16] + struct.pack("!H", c) + h[18:] + donnees

def udp(src, dst, sp, dp, donnees):
    h = struct.pack("!HHHH", sp, dp, 8 + len(donnees), 0)
    pseudo = ip4(src) + ip4(dst) + struct.pack("!BBH", 0, 17, len(h) + len(donnees))
    return h[:6] + struct.pack("!H", somme(pseudo + h + donnees)) + donnees

def dns_requete(ident, nom):
    q = b"".join(bytes([len(p)]) + p.encode() for p in nom.split(".")) + b"\0"
    return struct.pack("!HHHHHH", ident, 0x0100, 1, 0, 0, 0) + q + struct.pack("!HH", 1, 1)

def dns_reponse(ident, nom, a):
    q = b"".join(bytes([len(p)]) + p.encode() for p in nom.split(".")) + b"\0"
    return struct.pack("!HHHHHH", ident, 0x8180, 1, 1, 0, 0) + q + struct.pack("!HH", 1, 1) + struct.pack("!HHHIH", 0xC00C, 1, 1, 300, 4) + ip4(a)

def eth(dst, src, charge): return dst + src + b"\x08\x00" + charge

paquets, t = [], 1763031600.0
def ajoute(trame, dt=0.004):
    global t
    t += dt
    paquets.append((t, trame))

ajoute(eth(MAC_GW, MAC_PC, ip(IP_PC, IP_DNS, 17, udp(IP_PC, IP_DNS, 51515, 53, dns_requete(0x1a2b, "imprimante-atelier.morel.lan")), 1)))
ajoute(eth(MAC_PC, MAC_GW, ip(IP_DNS, IP_PC, 17, udp(IP_DNS, IP_PC, 53, 51515, dns_reponse(0x1a2b, "imprimante-atelier.morel.lan", IP_IMP)), 2)))
cs, ss, sp = 1000, 50000, 49822
ajoute(eth(MAC_IMP, MAC_PC, ip(IP_PC, IP_IMP, 6, tcp(IP_PC, IP_IMP, sp, 80, cs, 0, 0x02), 3)))
ajoute(eth(MAC_PC, MAC_IMP, ip(IP_IMP, IP_PC, 6, tcp(IP_IMP, IP_PC, 80, sp, ss, cs + 1, 0x12), 4)))
ajoute(eth(MAC_IMP, MAC_PC, ip(IP_PC, IP_IMP, 6, tcp(IP_PC, IP_IMP, sp, 80, cs + 1, ss + 1, 0x10), 5)))
corps = f"utilisateur=admin&mot_de_passe={DRAPEAU}&valider=Connexion".encode()
req = (b"POST /admin/connexion HTTP/1.1\r\nHost: imprimante-atelier.morel.lan\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/128.0\r\n"
       b"Content-Type: application/x-www-form-urlencoded\r\nContent-Length: " + str(len(corps)).encode() + b"\r\nConnection: close\r\n\r\n" + corps)
ajoute(eth(MAC_IMP, MAC_PC, ip(IP_PC, IP_IMP, 6, tcp(IP_PC, IP_IMP, sp, 80, cs + 1, ss + 1, 0x18, req), 6)))
rep = b"HTTP/1.1 302 Found\r\nServer: PrinterWeb/2.1\r\nLocation: /admin/tableau\r\nSet-Cookie: SID=7f3a91c0; path=/\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
ajoute(eth(MAC_PC, MAC_IMP, ip(IP_IMP, IP_PC, 6, tcp(IP_IMP, IP_PC, 80, sp, ss + 1, cs + 1 + len(req), 0x18, rep), 7)))
ajoute(eth(MAC_IMP, MAC_PC, ip(IP_PC, IP_IMP, 6, tcp(IP_PC, IP_IMP, sp, 80, cs + 1 + len(req), ss + 1 + len(rep), 0x11), 8)))
ajoute(eth(MAC_PC, MAC_IMP, ip(IP_IMP, IP_PC, 6, tcp(IP_IMP, IP_PC, 80, sp, ss + 1 + len(rep), cs + 2 + len(req), 0x11), 9)))
ajoute(eth(MAC_IMP, MAC_PC, ip(IP_PC, IP_IMP, 6, tcp(IP_PC, IP_IMP, sp, 80, cs + 2 + len(req), ss + 2 + len(rep), 0x10), 10)))

with open(sys.argv[1] if len(sys.argv) > 1 else "ecoute.pcap", "wb") as f:
    f.write(struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1))
    for ts, tr in paquets:
        f.write(struct.pack("<IIII", int(ts), int((ts % 1) * 1e6), len(tr), len(tr)) + tr)
print(f"{len(paquets)} paquets écrits")
