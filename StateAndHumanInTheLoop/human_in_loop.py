import asyncio
from codecs import StreamReader
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
from autogen_agentchat.ui import Console
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Create an instance of the OpenAIChatCompletionClient
model_client = OpenAIChatCompletionClient(api_key=api_key, model="gpt-4o")


assistant = AssistantAgent(
    name='Assistant',
    description='you are a great assistant',
    model_client=model_client,
    system_message='You are a really helpful assistant who help on the task given.'
)


user_agent = UserProxyAgent(
    name="UserProxy",
    description='A proxy agent that represent a user',
    input_func=input
)

termination_condition = TextMentionTermination('APPROVE')

team = RoundRobinGroupChat(
    participants=[assistant, user_agent],
    termination_condition= termination_condition
)

stream = team.run_stream(task="Write a poem in 4 lines about AI")

async def main():
    await Console(stream)
    
    
if __name__ == "__main__":
    asyncio.run(main())