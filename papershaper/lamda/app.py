import os
import pandas as pd
from fastapi import FastAPI, HTTPException, Request, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from filelock import FileLock
import aiofiles

# Initialize FastAPI app
app = FastAPI()

# CORS Configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],  # Restrict origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# # Define your API keys and their usage limits
# API_KEYS = {
#     "key1": 0,
#     "key2": 0,
#     "key3": 0,
#     # Add more keys as needed
# }

# # Define the maximum number of hits per key
# MAX_HITS = 4
# SWITCH_THRESHOLD = 3


# @app.middleware("http")
# async def api_key_rotation_middleware(request: Request, call_next):
#     current_key = None
#     for key, hits in API_KEYS.items():
#         if hits < SWITCH_THRESHOLD:
#             current_key = key
#             break

#     if current_key is None:
#         return JSONResponse(
#             status_code=429,
#             content={"error": "All API keys have exceeded their usage limits."}
#         )

#     # Increment hit count and set state
#     API_KEYS[current_key] += 1
#     request.state.api_key = current_key  # Set the API key

#     response = await call_next(request)
#     return response


# # Environment-based configurations
# CSV_CONTENT_PATH = os.getenv("CSV_CONTENT_PATH", "static/text_files_data2.csv")
# CSV_PROMPT_PATH = os.getenv("CSV_PROMPT_PATH", "static/prompt_data.csv")

# Load the CSV file
csv_file_path = 'text_files_data2.csv'  # Replace with your actual CSV file path
df_content = pd.read_csv(csv_file_path)
csv_file_path = 'prompt_data.csv'  # Replace with your actual CSV file path
df_prompt = pd.read_csv(csv_file_path)


def prepare_message(prompt:str, document_content:str,query_type:str) -> list:

    print("**********", prompt)
    user_prompt = prompt.format(**{'Document_content':document_content,"Mock Paper":query_type})
    #user_prompt = prompt.format({'Document_content':document_content})

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
    
    # return response.text
    return "YOYYYYOoOOOOoooo"
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
        raise HTTPException(status_code=404, detail="No matching records found document_content_df")
    
    if query_type_df.empty:
        raise HTTPException(status_code=404, detail="No matching records found query_type_df")
    
    if prompt_df.empty:
        raise HTTPException(status_code=404, detail="No matching records found prompt_df")
    
    
    
    prompt = prompt_df['Prompt_Data'].values[0]
    document_content = document_content_df['File_Data'].tolist()[0]
    query_type = query_type_df['File_Data'].tolist()[0]
    
#    print("***********************",prompt)
#    print("***********************",document_content)
    #print("***********************",query_type)
    print(prompt_df)

    msg = prepare_message(prompt,document_content,query_type)
    response = generate_response(msg)
    # Convert the filtered DataFrame to a list of dictionaries
    return response

# Load CSVs lazily
def load_csv(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path)

# # Cache
# cache_file_path = "cache.csv"
# lock_file_path = "cache.lock"

# Load cache if exists
# def load_cache():
#     if os.path.exists(cache_file_path):
#         return pd.read_csv(cache_file_path)
 
#     return pd.DataFrame(columns=['Board', 'Class', 'Subject', 'Chapter', 'Prompt_Type', 'result'])

#cache_df = load_cache()




# #def update_cache(board, class_, subject, chapter, prompt_type, result):
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
        
# @app.options("/get-value")
# async def options_get_value():
#     return JSONResponse(
#         content={"message": "CORS preflight response"},
#         headers={
#             "Allow": "OPTIONS, POST",  # Specify allowed methods
#             "Access-Control-Allow-Origin": "*",  # Allow all origins
#             "Access-Control-Allow-Methods": "OPTIONS, POST",
#             "Access-Control-Allow-Headers": "Content-Type, Authorization",
#         },
#     )

class InputData(BaseModel):
    id: str
    Board: str
    Class: str
    Subject: str
    Chapter: str
    Prompt_Type: str
    hit_count: int
    is_logedIn: bool
    
@app.post("/get-value")
async def get_value(input_data: InputData, request: Request):
    try:
        api_key = ""  # Access the current API key
        print(api_key)
    except AttributeError:
        raise HTTPException(status_code=500, detail="API key not set in middleware")

    # Your existing logic...
    # if input_data.hit_count < 1:
    #     cached_row = cache_df[
    #         (cache_df['Board'] == input_data.Board) &
    #         (cache_df['Class'] == input_data.Class) &
    #         (cache_df['Subject'] == input_data.Subject) &
    #         (cache_df['Chapter'] == input_data.Chapter) &
    #         (cache_df['Prompt_Type'] == input_data.Prompt_Type)
    #     ]

    #     if not cached_row.empty:
    #         y = cached_row.iloc[0]['result']
    #     elif input_data.is_logedIn:
    #         y = get_response(input_data.Board, input_data.Class, input_data.Subject, input_data.Chapter, input_data.Prompt_Type)
    #         update_cache(input_data.Board, input_data.Class, input_data.Subject, input_data.Chapter, input_data.Prompt_Type, y)
    # elif input_data.hit_count > 0 and input_data.is_logedIn:
    y = get_response(input_data.Board, input_data.Class, input_data.Subject, input_data.Chapter, input_data.Prompt_Type)
        #update_cache(input_data.Board, input_data.Class, input_data.Subject, input_data.Chapter, input_data.Prompt_Type, y)
    # else:
    #     y = "Please login to continue"

    return {"id": input_data.id, "result": y}