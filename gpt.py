from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
#from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field
import json
import os



# For normal output
def unique_result():
    template = """You are an Ai data analyst , your job is to find dublicate data from this given data
    {data}
      """
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(temperature=1.0 ,model="gpt-4o-2024-05-13",api_key="")
    chain = (
    prompt
    | llm
    | StrOutputParser()
    )
    return chain


# To get json fromated response
def formated_response():
    template="""You are a data analyst at a company ,
    after given some json data your job is to remove the duplicates form the data , and return the data in json format,dont write extra text just the data in its format
    \n{format_instructions}\n{data}\n
    """
    class Random_object(BaseModel):
         id:str=Field(description="The user id")
         name:str=Field(description="The users's name")
         email:str=Field(description="The users email")
    parser = JsonOutputParser(pydantic_object=Random_object)
    prompt = PromptTemplate(
        template=template,
        input_variables=["data"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    llm = ChatOpenAI(temperature=1.0 ,model="gpt-4o-2024-05-13",api_key="")
    chain = (
    prompt
    | llm
    | parser
    )
    return chain


def execute():
    with open('data.json','r') as file:
        data=json.load(file)
    llm_chain = unique_result()
    json_chain = formated_response()
    #result = llm_chain.invoke({"data":data})
    result = json_chain.invoke({"data":data})
    print(result)

execute()

     
