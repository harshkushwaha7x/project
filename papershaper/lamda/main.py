import json
import os
import pandas as pd
from filelock import FileLock
from pydantic import BaseModel



# Environment-based configurations
# CSV_CONTENT_PATH = os.getenv("CSV_CONTENT_PATH", "static/text_files_data.csv")
# CSV_PROMPT_PATH = os.getenv("CSV_PROMPT_PATH", "static/prompt_data.csv")

# # Load the CSV file
# csv_file_path = 'text_files_data.csv'  # Replace with your actual CSV file path
# df_content = pd.read_csv(csv_file_path)
# csv_file_path = 'prompt_data.csv'  # Replace with your actual CSV file path
# df_prompt = pd.read_csv(csv_file_path)



def prepare_message(prompt:str, document_content:str,query_type:str) -> list:


    user_prompt = prompt.format(**{'Document_content':document_content,"Mock Paper":query_type})

    msg = []
    msg.append({"role": "user", "content": user_prompt})
    return user_prompt


def generate_response(msg:str):
    # print(model, system_prompt, user_prompt)

    # client = Groq(
    #     api_key="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",
    # )

    # chat_completion = client.chat.completions.create(
    #     messages=prepare_message(system_prompt, user_prompt),
    #     model=model,
    # )

    # return chat_completion.choices[0].message.content
    import google.generativeai as genai
    import os

    genai.configure(api_key="AIzaSyAvcaDhpMQ7XBzl5xO6YXozlIR3wtLNQNw")

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(msg)
    
    return response.text
def get_response(Board, Class, Subject, Chapter, Prompt_Type):
        # Filter the DataFrame based on the dropdown selections
    
    prompt_df  =  df_prompt[
        (df_prompt['Board'] == Board) &
        (df_prompt['Class'] == Class) &
        (df_prompt['Prompt_Type'] == Prompt_Type) 
    ]
    
    document_content_df = df_content[
        (df_content['Board'] == Board) &
        (df_content['Class'] == Class) &
        (df_content['Subject'] == Subject) &
        (df_content['Chapter'] == Chapter)
    ]
    
    query_type_df = df_content[
        (df_content['Board'] == Board) &
        (df_content['Class'] == Class) &
        (df_content['Subject'] == Subject) &
        (df_content['Chapter'] == Chapter)
    ]


    if document_content_df.empty:
        return {
        'statusCode': 404,
        'body': json.dumps('No matching records found document_content_df')
    }
    
    if query_type_df.empty:
        return {
        'statusCode': 404,
        'body': json.dumps('No matching records found query_type_df')
    }
    
    if prompt_df.empty:
        return {
        'statusCode': 404,
        'body': json.dumps('No matching records found prompt_df')
    }
        
    prompt = prompt_df['Prompt_Data'].values[0]
    document_content = document_content_df['File_Data'].tolist()[0]
    query_type = query_type_df['File_Data'].tolist()[0]
    
    msg = prepare_message(prompt,document_content,query_type)
    response = generate_response(msg)
    # Convert the filtered DataFrame to a list of dictionaries
    return response
# Load the CSV file
csv_file_path = 'text_files_data2.csv'  # Replace with your actual CSV file path
df_content = pd.read_csv(csv_file_path)
csv_file_path = 'prompt_data.csv'  # Replace with your actual CSV file path
df_prompt = pd.read_csv(csv_file_path)

 # File path for caching
#cache_file_path = "cache.csv"
#lock_file_path = "cache.lock"

# Sample DataFrame for demonstration
data = {}

# Create a DataFrame with a MultiIndex
index = pd.MultiIndex.from_tuples(data.keys(), names=['Board', 'Class', 'Subject', 'Chapter', 'Prompt_Type'])
df = pd.DataFrame(list(data.values()), index=index, columns=['value'])

# Load cache from file if it exists
# if os.path.exists(cache_file_path):
#     cache_df = pd.read_csv(cache_file_path)
# else:
#     cache_df = pd.DataFrame(columns=['Board', 'Class', 'Subject', 'Chapter', 'Prompt_Type', 'result'])

class InputData(BaseModel):
    id: str
    Board: str
    Class: str
    Subject: str
    Chapter: str
    Prompt_Type: str
    hit_count: int
    is_logedIn: bool
#from filelock import FileLock

# def update_cache(board, class_, subject, chapter, prompt_type, result):
#     with FileLock(lock_file_path):
#         # Check if the entry already exists
#         existing_entry = cache_df[
#             (cache_df['Board'] == board) &
#             (cache_df['Class'] == class_) &
#             (cache_df['Subject'] == subject) &
#             (cache_df['Chapter'] == chapter) &
#             (cache_df['Prompt_Type'] == prompt_type)
#         ]
        
#         if not existing_entry.empty:
#             # Update the existing entry
#             cache_df.loc[existing_entry.index, 'result'] = result
#         else:
#             # Add a new entry
#             cache_df.loc[len(cache_df)] = [board, class_, subject, chapter, prompt_type, result]
        
#         # Save the updated cache to file
#         cache_df.to_csv(cache_file_path, index=False)



def lambda_handler(event, context):
    # # TODO implement
    print(event)
    # event=event['body']
    # print(event)

    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }
    # api_key = request.state.api_key
    try:
        # api_key = request.state.api_key  # Access the current API key
        # print(api_key)
        # if event['hit_count'] < 1:
        #     cached_row = cache_df[
        #         (cache_df['Board'] == event['Board']) &
        #         (cache_df['Class'] == event['Class']) &
        #         (cache_df['Subject'] == event['Subject']) &
        #         (cache_df['Chapter'] == event['Chapter']) &
        #         (cache_df['Prompt_Type'] == event['Prompt_Type'])
        #     ]
            
        #     if not cached_row.empty:
        #         y = cached_row.iloc[0]['result']
        #     elif event['is_logedIn']:
        #         y = get_response(event['Board'], event['Class'], event['Subject'], event['Chapter'], event['Prompt_Type'])
        #         update_cache(event['Board'], event['Class'], event['Subject'], event['Chapter'], event['Prompt_Type'], y)
        # elif event['hit_count'] > 0 and event['is_logedIn']:
        y = get_response(event['Board'], event['Class'], event['Subject'], event['Chapter'], event['Prompt_Type'])
        #     update_cache(event['Board'], event['Class'], event['Subject'], event['Chapter'], event['Prompt_Type'], y)
        
        # else:
        #     y = "Please login to continue"
            
        return {"id": event['id'], "result": y}       
    except Exception as e:
        print(e)
        print(Exception)
        return {
        'statusCode': 404,
        'body': json.dumps('Hello from Lambda!')
    }