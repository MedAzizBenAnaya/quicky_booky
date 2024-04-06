import os
import json
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
from generator import create_ebook

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

client = AsyncOpenAI(api_key=api_key)


async def make_ebook_outline(title, topic, language, age, gender, extra_info, n_chapters, n_subsections):
    print(f"Starting to generate outline for ebook titled '{title}'...")
    ebook_author = (
        "Envision yourself as an acclaimed author renowned for your insightful, captivating, and meticulously researched works. "
        "Your narratives are celebrated for weaving intricate knowledge from various domains into engaging stories that resonate deeply with readers.")

    ebook_prompt = (f"Craft an outline for an ebook titled '{title}', written in {language} about '{topic}'. "
                    f"This ebook is intended for {age}-year-old {gender}s, specifically focusing on those who {extra_info}. "
                    "Please structure the outline to include {n_chapters} chapters, each with {n_subsections} subsections. "
                    "Provide a 200-word description for the ebook, a brief summary for each chapter, and suggest sources for further exploration. "
                    "Format the outline in JSON, resembling this template: "
                    '{"ebook_title": "", "target_audience": "", "description": "", "chapters": [{"chapter_title": "Chapter N: Title", "subsections": ["Subsection"]}], "summary": "", "sources": ""}')

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": ebook_author},
            {"role": "user", "content": ebook_prompt}
        ],
    )

    try:
        table_of_contents = json.loads(response.choices[0].message.content)
        print("Outline generated successfully.")
    except json.JSONDecodeError:
        print("Failed to decode JSON. Check the response format.")
        table_of_contents = {}

    return table_of_contents


async def expand_subsection(ebook_author, subsection_title, language, age, gender, extra_info):
    print(f"Expanding subsection: {subsection_title}")
    response = await client.chat.completions.create(
        model="gpt-4",
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

    print(f"Subsection '{subsection_title}' expanded.")
    return response.choices[0].message.content


async def make_ebook(title, topic, language, age, gender, extra_info, n_chapters, n_subsections):
    table_of_contents = await make_ebook_outline(title, topic, language, age, gender, extra_info, n_chapters,
                                                 n_subsections)

    ebook_author = (
        "Imagine you're a celebrated author and editor with a rich background in a diverse array of fields.")

    tasks = []
    for chapter in table_of_contents.get("chapters", []):
        chapter_title = chapter.get("chapter_title")
        print(f"Processing chapter: {chapter_title}")
        for subsection_title in chapter.get("subsections", []):
            task = expand_subsection(ebook_author, subsection_title, language, age, gender, extra_info)
            tasks.append(task)

    chapters_contents = await asyncio.gather(*tasks)

    print("All subsections expanded. Finished with the book.")
    return create_ebook("ebook", title, table_of_contents, chapters_contents, gender)


