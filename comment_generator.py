import os
from openai import OpenAI
from dotenv import load_dotenv
from search_agent import run_search_agent

load_dotenv(override=True)

class CommentGenerator:
    def __init__(self):
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_client = OpenAI(api_key=self.openai_api_key)

    def generate_comment(self, post_title, post_content, url_content, image_description):
        in_context_training = self.open_file("context.txt")
        important_rules = self.open_file("rules.txt")

        relevant_info = run_search_agent(post_title)
        relevant_info += run_search_agent(post_content)

        if image_description:
            url_content = ""  # Exclude url_content if the post contains an image

        prompt = f"""
        <context>
            <example_comments>
            {in_context_training}
            </example_comments>
            <important_rules>
            {important_rules}
            </important_rules>
            <relevant_information>
            {relevant_info}
            </relevant_information>
        </context>
        <task>
            <post_title>{post_title}</post_title>
            <post_content>{post_content}</post_content>
            <url_content>{url_content}</url_content>
            <image_description>{image_description}</image_description>
        </task>
        <instructions>
            <main_task>Write a comment in ONLY lower case letters to the Reddit post from the <task> section</main_task>
            <style>Use the same length (ish) and style as the <example comments></style>
            <length>Provide a brief answer, limiting your response to 3-8 sentences.</length>
            <rules>Strictly adhere to the <important_rules></rules>
            <goal>Answer or comment on the post in a very human like way while steering clear of repeating the content of the post in the comments.</goal>
            <value_addition>Bring value by providing insights from the <relevant_information>, asking questions, or sharing your own experiences if any.</value_addition>
            <use_context>Use the <relevant_information> to enhance your response and make it more informative and contextually appropriate to bring value to the discussion.</use_context>
        </instructions>
        """

        response = self.openai_client.chat.completions.create(
           model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

        if response.choices and len(response.choices) > 0:
            answer_content = response.choices[0].message.content
            return answer_content.strip()
        else:
            return ""

    def open_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as infile:
            return infile.read()