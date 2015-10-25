"""
This module contains data about attacks.
"""

ATTACKS = { 
    # New attack template
    #   string - attack name:  
    #   {
    #   'prep_msg': string - msg printed when attack begins
    #       e.g. 'You attack with %s'. %s will be replaced with weapon
    #   'hit_crit_msg': string - msg printed when critical is rolled
    #   'hit_success_msg': string - msg printed when successful attack
    #   'hit_fail_msg': string - msg when attack fails
    # }
    'slash': {
            'prep_msg': "You slash with your %s!",
            'hit_crit_msg': "The attack opens up a gushing wound!",
            'hit_success_msg': "The slash cuts through!",
            'hit_fail_msg': "Your weapon bounces off!",
            }
}
