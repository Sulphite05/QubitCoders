import os
import pickle
import requests
from skfuzzy import control as ctrl
import google.generativeai as genai
from streamlit import cache_resource, secrets


@cache_resource
def load_fuzz_model():
    base_path = os.path.abspath(os.path.dirname(__file__))
    pkl_path = os.path.join(base_path, "fuzzy_system_model.pkl")
    with open(pkl_path, 'rb') as f:
        loaded_system = pickle.load(f)
    return loaded_system

@cache_resource
def load_llm_model():
    os.environ["GEMINI_API_KEY"] = secrets["genai"]["api_key"]
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    return model


def fetch_api_data(username):
    try:
        r = requests.get(f'https://leetcodeapi-v1.vercel.app/{username}')
        data = r.json()[username]['submitStatsGlobal']['acSubmissionNum']

        submission_data = (data[1]['count'], data[2]['count'], data[3]['count'])
    except KeyError:
        submission_data = None

    try:
        r = requests.get(f'https://leetcodeapi-v1.vercel.app/rating/{username}')
        contest_data = (r.json()['rating'],)
    except KeyError:
        contest_data = (0,)

    return [contest_data, submission_data]


def get_user_expertise(contest_data, submission_data):
    loaded_system = load_fuzz_model()
    expertise_sim = ctrl.ControlSystemSimulation(loaded_system)

    expertise_sim.input['contest_rating'] = contest_data[0]
    expertise_sim.input['easies'] = submission_data[0]
    expertise_sim.input['mediums'] = submission_data[1]
    expertise_sim.input['hards'] = submission_data[2]

    expertise_sim.compute()
    expertise_level = round(expertise_sim.output['expertise'], 2)

    if 0 <= expertise_level < 3.5: expertise_name = "beginner"
    elif 3.5 < expertise_level < 6.2: expertise_name = "beginner-intermediate"
    elif 6.2 <= expertise_level < 8.2: expertise_name = "intermediate-advanced"
    else: expertise_name = "advanced"

    return expertise_level, expertise_name


def get_user_analysis(expertise_name, contest_data, submission_data):

    model = load_llm_model()
    contest_rating = contest_data[0]
    easies, mediums, hards = submission_data

    response = model.generate_content([
        f'''You are an expert competitive programmer and problem solver who needs to give advice to a user.
        The user is a competitive programmer providing you with their data as follows:
        \nContest Ranking: {contest_rating} 
        \nHard questions solved: {hards}
        \nMedium questions solved: {mediums}
        \nEasy questions solved: {easies}
        \nThe user's expertise level is: {expertise_name}
        \nBased on this information, give the user a personalized recommendation to help them improve in 
        competitive programming.
        \nFocus on areas they should work on, such as
        \n- Which type of problems (Medium, Hard) they should solve more. Stress more on hards.
        \n- What kind of problems they should solve more based on their expertise level
        (basic DS like arrays, hashmaps, hashsets or advanced ones like linked lists, trees, graphs etc and 
        also algorithms)
        \n- Whether they should participate in more contests.
        \n- Any specific advice to boost their problem-solving skills.
        \n- Any routine habit like sleeping, practice, exercise to enhance their competitive programming skills.
        \nKeep the recommendation as with 250 words. 
        Your recommendation should be fun, engaging, motivational, and actionable. Begin with Assalam u alaikum!''',
        "1400 - Hard questions solved: 10 - Medium questions solved: 200- Easy questions solved: 100",
        "output: ",
    ])
    return response.text


def get_response(username):
    contest_data, submission_data = fetch_api_data(username)
    if not submission_data: return None, None, None, None, None
    expertise_level, expertise_name = get_user_expertise(contest_data, submission_data)
    recom = get_user_analysis(expertise_name, contest_data, submission_data)
    return expertise_level, expertise_name, recom, contest_data, submission_data
