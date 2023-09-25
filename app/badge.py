# TODO: it might be more maintainable to keep this in a table
#   as such we do not need code change to add a new badge requirement
import app.badge_list as bl


class Badge:
    def __init__(self, name, css_class, cond):
        self.name = name
        self.css_class = css_class
        self.cond = cond

    def is_fulfilled(self, score):
        return self.cond(score)


available_badges = [
    Badge("Papa Driller", "label label-warning", bl.papa_driller),
    Badge("I passed IPPT!", "label label-success", bl.pass_ippt),
    Badge("Phoenix Euphoria", "label label-primary", bl.phoenix_euphoria),
]


def get_user_badges(all_scores):
    user_badges = []
    unique_badge = set()

    # TODO: the performance for this might degrade fast if there are too many scores
    #   consider saving this data instead of calculating it on the fly
    for score in all_scores:
        for badge in available_badges:
            if badge in unique_badge:  # prevent duplicate badges
                continue

            if badge.is_fulfilled(score):
                user_badges.append(badge)
                unique_badge.add(badge)

    return user_badges
