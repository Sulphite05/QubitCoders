import os
import pickle
import requests
from streamlit import cache_resource, secrets
from skfuzzy import control as ctrl
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint

prompt_template = PromptTemplate(
    input_variables=['expertise_name', 'contest_rating', 'hards', 'mediums', 'easies'],
    template="""
    You are an expert competitive programmer and problem solver who needs to give advice to a user.
    The user is a competitive programmer with the following data:
    Contest Ranking: {contest_rating}
    Hard questions solved: {hards}
    Medium questions solved: {mediums}
    Easy questions solved: {easies}
    
    The user's expertise level is: {expertise_name}.

    Based on this information, give them a fun, personalized recommendation to help them improve in competitive 
    programming.
    Keep it under 150 words and focus on areas they should work on, such as:
    - Which type of problems (Medium, Hard) they should solve more. Stress more on hards.
    - What kind of problems they should solve more based on their expertise level(basic DS like arrays, hashmaps, 
    hashsets or advanced ones like linked lists, trees, graphs etc and also algorithms)
    - Whether they should participate in more contests.
    - Any specific advice to boost their problem-solving skills.
    - Any routine habit like sleeping, practice, exercise to enhance their competitive programming skills.
    Your recommendation should be fun, engaging, motivational, and actionable. Directly give the advice without telling 
    that you are about to give a recommendation. Don't write in inverted commas. Don't ask for feedback.
    """
)


@cache_resource
def load_fuzz_model():
    base_path = os.path.abspath(os.path.dirname(__file__))
    pkl_path = os.path.join(base_path, "fuzzy_system_model.pkl")
    with open(pkl_path, 'rb') as f:
        loaded_system = pickle.load(f)
    return loaded_system

@cache_resource
def load_llm_model():
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = secrets["huggingface"]["api_key"]
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
        token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
        temperature=0.7,
        max_new_tokens=512,
        top_k=50,
        top_p=0.95,
        typical_p=0.95,
        repetition_penalty=1.03,
    )
    return llm

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
    elif 6.2 <= expertise_level < 8.2: expertise_name = "bntermediate-advanced"
    else: expertise_name = "Advanced"

    return expertise_level, expertise_name


def get_user_analysis(expertise_name, contest_data, submission_data):
    llm = load_llm_model()
    chain = prompt_template | llm
    user_analysis = chain.invoke({
        'expertise_name': expertise_name,
        'contest_rating': round(contest_data[0], 2),
        'hards': submission_data[2],
        'mediums': submission_data[1],
        'easies': submission_data[0],
    })
    return user_analysis


def get_response(username):
    contest_data, submission_data = fetch_api_data(username)
    expertise_level, expertise_name = get_user_expertise(contest_data, submission_data)
    recom = get_user_analysis(expertise_name, contest_data, submission_data)
    return expertise_level, expertise_name, recom, contest_data, submission_data
