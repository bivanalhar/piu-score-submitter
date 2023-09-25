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

