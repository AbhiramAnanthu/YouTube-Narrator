from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate

path = ".env"
load_dotenv(dotenv_path=path)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


def scripting(prompt):
    prompt_template = PromptTemplate.from_template(
        "You are a youtube script writer.{prompt} this is the prompt given by the user about the subject.Make a script with dialogues that are time stamped"
    )

    chain = prompt_template | llm
    result = chain.invoke({"prompt": prompt})
    with open("script.txt", "w") as file:
        file.write(result.content)
    return result.content


def script_refinement(prompt):
    script = scripting(prompt)
    prompt_template = PromptTemplate.from_template(
        "{script}.This is a script of a Youtube vedio.I want to generate a an audio file based on the script. Change this script in the content for narration only.Dont include `narrator: ` only the content"
    )
    chain = prompt_template | llm
    result = chain.invoke({"script": script})
    return result.content
