import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

class ContentGenerator:

    def __init__(self,title, topic, language, age, gender, extra_info, n_chapters, n_subsections, model="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.title, self.topic, self.language, self.age, self.gender, self.extra_info, self.n_chapters, self.n_subsections = (
            title, topic, language, age, gender, extra_info, n_chapters, n_subsections)
        self.model = model
        self.author_prompt = (
            "Imagine you're a celebrated author and editor with a rich background in a diverse array of fields. "
            "Your writing has earned accolades for its depth, insight, and engaging style. "
            "Your goal is to create engaging and comprehensive ebooks tailored for specific audiences."
        )
        self.book_info = {}
        self.content_array = []


    def _call_openai(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.author_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    def generate_outline(self):
        outline_prompt = (
            f"Write an ebook named '{self.title}' in {self.language}. It is about {self.topic}. "
            f"Our target audience is {self.age}-year-old {self.gender} who {self.extra_info}. "
            f"Create an outline with {self.n_chapters} chapters, each containing {self.n_subsections} subsections. "
            f"Include a 200-word description of the book, a summary, and a 'Sources for Further Reading' page. "
            f"Provide the response in JSON format with the style: "
            '{"ebook_title": "<title>", "target_audience": "<audience>", "description": "<description>", '
            '"chapters": [{"chapter_title": "<chapter_title>", "subsections": ["<subsection_title>", "<subsection_title>"]}], '
            '"summary": "<summary>", "sources": "<sources>"}'
        )

        try:
            self.book_info = self.call_openai(outline_prompt)
        except Exception as e :
            print(f"Error during OpenAI API call: {e}")
            return None

        try:
            return json.loads(self.book_info)
        except json.JSONDecodeError:
            print("Failed to decode JSON for outline. Check the response format.")
            return None

    def generate_chapters_content(self):
        chapters = self.book_info.get("chapters", [])

        for chapter in chapters:
            chapter_title = chapter
            subsections = self.book_info.get("subsections", {}).get(chapter, [])
            subsection_list = "\n".join(f"- {sub}" for sub in subsections)

            prompt = (
                f"Expand on the following subsections of the chapter '{chapter_title}' in {self.language}: \n"
                f"{subsection_list}\n\n"
                f"Incorporate relevant statistics and real-world examples to illustrate key points. "
                f"Use an engaging and informative narrative style tailored for {self.age}-year-old {self.gender} . "
                f"Use clear, accessible language and weave in storytelling elements to captivate the audience. "
                f"Provide the content for all subsections in a single JSON object with the format: "
                '{"chapter_title": "<chapter_title>", "subsections": [{"title": "<subsection_title>", "content": "<subsection_content>"}]}'
            )
            try:
                chapter_content = self._call_openai(prompt)
                self.content_array.append(chapter_content)
            except Exception as e:
                print(f"Error generating content for chapter '{chapter_title}': {e}")



