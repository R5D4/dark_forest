"""
This module contains data about attacks.
"""

# attack types
#'slash'
#'pierce'
#'blunt'
#'charge'

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
            'prep_msg': "The %s slashes the %s with the %s!",
            'hit_crit_msg': "The slash opens up a gushing wound!",
            'hit_success_msg': "The slash cuts through the defences!",
            'hit_fail_msg': "The slash misses!",
            },
    'pierce': {
            'prep_msg': "The %s pierces the %s with its %s!",
            'hit_crit_msg': "The attack sinks in deeply!",
            'hit_success_msg': "The attack connects!",
            'hit_fail_msg': "The attack misses!",
            },
    'blunt': {
            'prep_msg': "The %s smashes the %s with its %s!",
            'hit_crit_msg': "The attack shatters the defences!",
            'hit_success_msg': "The smash connects!",
            'hit_fail_msg': "The attack misses!",
            },
    'charge': {
            'prep_msg': "The %s charges the %s leading with its %s!",
            'hit_crit_msg': "The charge hits square on!",
            'hit_success_msg': "The charge connects!",
            'hit_fail_msg': "The charge misses!",
            }
}
