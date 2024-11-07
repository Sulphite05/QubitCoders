import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pickle

# input variables
contest_rating = ctrl.Antecedent(np.arange(0, 4000, 0.25), 'contest_rating')
easies = ctrl.Antecedent(np.arange(0, 1000, 1), 'easies')
mediums = ctrl.Antecedent(np.arange(0, 2000, 1), 'mediums')
hards = ctrl.Antecedent(np.arange(0, 1000, 1), 'hards')

# output variable
expertise = ctrl.Consequent(np.arange(0, 10, 0.2), 'expertise')

# membership functions
contest_rating['low'] = fuzz.trapmf(contest_rating.universe, [0, 0, 1200, 1500])
contest_rating['medium'] = fuzz.trimf(contest_rating.universe, [1300, 1550, 1800])
contest_rating['high'] = fuzz.trapmf(contest_rating.universe, [1650, 1900, 4000, 4000])

easies['few'] = fuzz.trapmf(easies.universe, [0, 0, 50, 100])
easies['moderate'] = fuzz.trimf(easies.universe, [80, 150, 300])
easies['many'] = fuzz.trapmf(easies.universe, [120, 250, 1000, 1000])

mediums['few'] = fuzz.trapmf(mediums.universe, [0, 0, 50, 110])
mediums['moderate'] = fuzz.trimf(mediums.universe, [90, 200, 350])
mediums['many'] = fuzz.trapmf(mediums.universe, [220, 400, 2000, 2000])

hards['few'] = fuzz.trapmf(hards.universe, [0, 0, 15, 40])
hards['moderate'] = fuzz.trimf(hards.universe, [30, 60, 100])
hards['many'] = fuzz.trapmf(hards.universe, [70, 100, 1000, 1000])

expertise['beginner'] = fuzz.trapmf(expertise.universe, [0, 0, 2.5, 5])
expertise['beginner-intermediate'] = fuzz.trimf(expertise.universe, [3.2, 4.5, 6.5])
expertise['intermediate-advanced'] = fuzz.trapmf(expertise.universe, [6.2, 7, 8.5, 9])
expertise['advanced'] = fuzz.trapmf(expertise.universe, [8.4, 8.6, 10, 10])

# fuzzy rules
rules = []
for contest_rating_level in ['low', 'medium', 'high']:
    for easy_level in ['few', 'moderate', 'many']:
        for medium_level in ['few', 'moderate', 'many']:
            for hard_level in ['few', 'moderate', 'many']:
                if contest_rating_level == 'high':
                    expertise_level = 'advanced'
                elif ((contest_rating_level == 'medium' and medium_level == 'few') or
                      (contest_rating_level == 'low' and medium_level == 'many') and hard_level == 'few'):
                    expertise_level = 'beginner-intermediate'
                elif contest_rating_level == 'low' and medium_level == 'few' and hard_level == 'few':
                    expertise_level = 'beginner'
                else:
                    expertise_level = 'intermediate-advanced'

                rule = ctrl.Rule(
                    contest_rating[contest_rating_level] & easies[easy_level] & mediums[medium_level] & hards[hard_level],
                    expertise[expertise_level]
                )
                rules.append(rule)


expertise_ctrl = ctrl.ControlSystem(rules)
expertise_sim = ctrl.ControlSystemSimulation(expertise_ctrl)

with open('fuzzy_system_model.pkl', 'wb') as f:
    pickle.dump(expertise_ctrl, f)
