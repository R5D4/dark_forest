"""
This module contains attack descriptions.
"""

# array of attack descriptions as a dict
ATTACKS = [
    # New attack template
    # {
    #   'name': string - attack name
    #   'prep_msg': string - msg printed when attack begins
    #       e.g. 'You attack with %s'. %s will be replaced with weapon
    #   'hit_crit_msg': string - msg printed when critical is rolled
    #   'hit_success_msg': string - msg printed when successful attack
    #   'hit_fail_msg': string - msg when attack fails
    #   'hit_attr': character attribute to add to hit chance e.g. 'str'
    #   'hit_roll': dice roll format e.g. '1d10'
    #   'hit_against': enemy attribute to hit against e.g. 'AC'
    #   'dmg_roll': dice roll format e.g. '2d6'
    #   'dmg_base': integer - min damage if successful hit
    # }
    {
        'name': 'slash',
        'prep_msg': "You slash with your %s!",
        'hit_crit_msg': "The attack opens up a gushing wound!",
        'hit_success_msg': "The slash cuts through!",
        'hit_fail_msg': "Your weapon bounces off!",
        'hit_attr': 'str',
        'hit_roll': '1d20',
        'hit_against': 'AC',
        'dmg_roll': '1d8',
        'dmg_base': 3
    }


]
