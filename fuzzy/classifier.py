import os
import pickle
import requests
from streamlit import cache_resource
from skfuzzy import control as ctrl


@cache_resource
def load_model():
    base_path = os.path.abspath(os.path.dirname(__file__))
    pkl_path = os.path.join(base_path, "fuzzy_system_model.pkl")
    with open(pkl_path, 'rb') as f:
        loaded_system = pickle.load(f)
    return loaded_system


def fetch_api_data(username):
    try:
        r = requests.get(f'https://leetcodeapi-v1.vercel.app/rating/{username}')
        contest_data = (r.json()['rating'],)
    except KeyError:
        contest_data = (0,)

    try:
        r = requests.get(f'https://leetcodeapi-v1.vercel.app/questions/{username}')
        data = r.json()
        submission_data = (data['Easy'], data['Medium'], data['Hard'])
    except KeyError:
        submission_data = (0, 0, 0)

    return [contest_data, submission_data]


def get_user_expertise(username):
    loaded_system = load_model()
    expertise_sim = ctrl.ControlSystemSimulation(loaded_system)

    contest_data, submission_data = fetch_api_data(username)
    expertise_sim.input['contest_rating'] = contest_data[0]
    expertise_sim.input['easies'] = submission_data[0]
    expertise_sim.input['mediums'] = submission_data[1]
    expertise_sim.input['hards'] = submission_data[2]

    expertise_sim.compute()
    expertise_level = round(expertise_sim.output['expertise'], 2)

    if 0 <= expertise_level < 3.5: expertise_name = "Beginner"
    elif 3.5 < expertise_level < 6.2: expertise_name = "Beginner-intermediate"
    elif 6.2 <= expertise_level < 8.2: expertise_name = "Intermediate-advanced"
    else: expertise_name = "Advanced"

    return expertise_level, expertise_name

def get_user_analysis(expertise, data):


