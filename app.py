import panel as pn
import requests
import pandas as pd
pn.extension()

def get_data(num_questions, difficulty, category):
    #url = f"https://opentdb.com/api.php?amount={num_questions}&category={category_match[category]}&difficulty={difficulty}&type=boolean"
    url = f"https://opentdb.com/api.php?amount={num_questions}&category={category_match[category]}&difficulty={difficulty}"
    df = pd.DataFrame(
        requests.get(url).json()['results']
    )
    return df 

category = pn.widgets.Select(
    name='Category',
    options=[
        'General Knowledge',
        'Film',
        'Music',
        'Video Games',
        'Science & Nature',
        'Computers',
        'Geography',
        'History',
        'Politics',
        'Animals',
        'Japanese Anime & Manga'
    ], 
    value='General Knowledge'
)
category

category_match = {
    'General Knowledge': 9,
    'Books': 10,
    'Film': 11,
    'Music': 12,
    'Musicals & Theatres': 13,
    'Television': 14,
    'Video Games': 15,
    'Board Games': 16,
    'Science & Nature': 17,
    'Computers': 18,
    'Mathematics': 19,
    'Mythology': 20,
    'Sports': 21,
    'Geography': 22,
    'History': 23,
    'Politics': 24,
    'Art': 25,
    'Celebrities': 26,
    'Animals': 27,
    'Vehicles': 28,
    'Comics': 29,
    'Gadgets': 30,
    'Japanese Anime & Manga': 31,
    'Cartoon & Animations': 32
 }

difficulty = pn.widgets.Select(
    name='Difficulty',
    options=['easy', 'medium', 'hard'], 
    value='easy'
)
difficulty

num_questions = pn.widgets.DiscreteSlider(
    name='Number of Questions', 
    options=[5, 10, 15, 20], value=5
)
num_questions

def question_list(i, df):

	
	    button_true = pn.widgets.Button(name='True')
	    button_false = pn.widgets.Button(name='False')
	 
	    text = pn.widgets.StaticText(value='')

	    def processing_button_true(event):
	        if df.correct_answer[i] == 'True': 
	            text.value = 'Correct!'
	        else:
	            text.value = 'Incorrect!'

	    def processing_button_false(event):
	        if df.correct_answer[i] == 'False': 
	            text.value = 'Correct!'
	        else:
	            text.value = 'Incorrect!'

	    button_true.on_click(processing_button_true)
	    button_false.on_click(processing_button_false)
	    return pn.Column(
	        pn.pane.Markdown(f"""
	         
	        #Question {i+1}:
	        ### {df.question[i]}
	        """),

	        pn.Row(button_true,button_false), 
	        text)


def get_data_and_questions(num_questions, difficulty, category):
    df = get_data(num_questions, difficulty, category)
    question_pane = [question_list(i, df) for i in range(len(df))]
    trivia_pane = pn.Column(*question_pane)
    return trivia_pane 


interactive = pn.bind(get_data_and_questions, num_questions, difficulty, category)


# Layout using Template
template = pn.template.FastListTemplate(
    title='Trivia Game', 
    sidebar=[num_questions, difficulty, category],
    main=[interactive],
    accent_base_color="#88d8b0",
    header_background="#88d8b0",
)
template.servable()