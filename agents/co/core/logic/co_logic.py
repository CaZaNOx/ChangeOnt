from enum import IntEnum

class TV(IntEnum):
    BOT = 0
    UNK = 1
    TOP = 2

def lnot(a: TV) -> TV:
    return {TV.TOP: TV.BOT, TV.BOT: TV.TOP, TV.UNK: TV.UNK}[a]

def land(a: TV, b: TV) -> TV:
    if a == TV.BOT or b == TV.BOT: return TV.BOT
    if a == TV.TOP and b == TV.TOP: return TV.TOP
    return TV.UNK

def lor(a: TV, b: TV) -> TV:
    if a == TV.TOP or b == TV.TOP: return TV.TOP
    if a == TV.BOT and b == TV.BOT: return TV.BOT
    return TV.UNK

def limp(a: TV, b: TV) -> TV:
    return lor(lnot(a), b)
