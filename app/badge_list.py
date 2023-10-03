def papa_driller(score):
    # check if user scores at least 90% for Papa Gonzales D18 in 18 Again
    if score.event == "E1" and score.chart == "Papa Gonzales" and score.finalScore > 90:
        return True
    return False


def pass_ippt(score):
    # check if user attempts the IPPT event
    if score.event == "E3":
        return True
    return False


def phoenix_euphoria(score):
    # check if user scores at least 97% in the Euphorianic UCS
    if score.chart == "Euphorianic D!!" and score.finalScore >= 97:
        return True
    return False


def badge_e7_airplane(score):
    if score.chart == "Airplane D18" and score.maxCombo >= 200:
        return True
    return False


def badge_e7_rip(score):
    if score.chart == "RIP D18" and score.maxCombo >= 925:
        return True
    return False


def badge_e7_pirate(score):
    if score.chart == "Pirate D19" and score.finalScore >= 95:
        return True
    return False


def badge_e7_teddy_bear(score):
    if score.chart == "Teddy Bear D19" and score.maxCombo >= 300:
        return True
    return False


def badge_e7_storm(score):
    if score.chart == "Storm D20" and score.finalScore >= 95:
        return True
    return False


def badge_e7_nxde(score):
    if score.chart == "Nxde D21" and score.finalScore >= 92:
        return True
    return False


def badge_e7_beautiful_liar(score):
    if score.chart == "Beautiful Liar D22" and score.finalScore >= 92:
        return True
    return False
