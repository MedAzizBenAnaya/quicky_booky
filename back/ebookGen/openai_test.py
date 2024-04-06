import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from generator import *

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

language = "English"
title = " "
topic = ""
extra_info = ""
n_chapters = 5
n_subsections = 3


def make_ebook(title, topic, language, age, gender, extra_info):
    ebook_author = (
        "Imagine you're a celebrated author and editor with a rich background in a diverse array of fields. "
        "Your writing has earned accolades for its depth, insight, and engaging style. With your vast "
        "expertise, you've contributed significantly to literature, seamlessly blending your knowledge across "
        "various disciplines into compelling narratives. As a book writer renowned for your ability to "
        "enlighten and entertain, your work is a testament to the power of multidisciplinary knowledge in "
        "creating transformative reading experiences.")

    ebook_prompt = (f"write an ebook named {title} in {language} language, it is about {topic}. "
                    f"Our target audience are {age} year old {gender} who {extra_info}. "
                    f"Create a comprehensive outline that has the number of Chapters and subsections with for this ebook, "
                    f"which will have {n_chapters} chapters with {n_subsections} subsections each. with a full 200 words description of the book and a summery at the end"
                    "Please provide it in JSON format that follows this style: "
                    '{"ebook_title": "","target_audience": "","description": "","chapters": [ {"chapter_title": "chapter n : tile","subsections": [ "subsection" ]}], "summary": " "}'"")

    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": ebook_author},
            {"role": "user", "content": ebook_prompt + 'give it in json'},
        ]
    )
    reply_json = response.choices[0].message.content

    try:
        table_of_contents = json.loads(reply_json)
    except json.JSONDecodeError:
        print("Failed to decode JSON. Check the response format.")
        table_of_contents = {}

    chapters_contents = []

    for chapter in table_of_contents.get("chapters", []):

        chapter_title = chapter.get("chapter_title")
        print( chapter_title )

        for subsection_title in chapter.get("subsections", []):  # Changed this line
            print(subsection_title)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": ebook_author},
                    {"role": "user",
                     "content": f"Please expand on subsection '{subsection_title}' in {language} . Incorporate relevant "
                                f"statistics and real-world examples to illustrate key points. Aim for a "
                                f"narrative style that is engaging and informative, designed to captivate "
                                f"our target audience, which are {age} year old {gender} who {extra_info}'."
                                f" Use clear, accessible "
                                f"language to make complex ideas understandable, and weave in "
                                f"storytelling elements where possible to enhance the reader's connection "
                                f"to the material. Your goal is to enrich this section with depth and "
                                f"insight, making it not only informative but also a pleasure to read. "
                                f"make sure text doesn't have any '#' in it"}
                ]
            )

            subsection_content = response.choices[0].message.content
            chapters_contents.append(subsection_content)
            print('   finished with the current chapter')

        print('   finished with the subsection', '\n')

    print('\n', 'finished with the book')

    return create_ebook("ebook", title, table_of_contents, chapters_contents, gender)

