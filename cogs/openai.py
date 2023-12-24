""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import os
from datetime import datetime, timedelta
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
import discord
from discord.ext import commands
from discord.ext.commands import Context

# Here we name the cog and create a new class for the cog.
class OpenAI(commands.Cog, name="openai"):
    def __init__(self, bot):
        self.bot = bot
        self.user_history_map = {}
        self.user_history_timestamp = {}
        #print(f'Message History: {self.user_history_map}')

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.


    @commands.hybrid_command(
        name="askgpt",
        description="OpenAI chatbot.",
    )
    async def askgpt(self, context: Context, prompt: str):

        await context.send(f'Prompt: {prompt}')
        
        author = context.author.name
        if author in self.user_history_map:
            message_history = self.user_history_map[author]            
        else:
            message_history = []

        #only allow 10 messages in history
        if len(message_history) > 10:
            message_history.pop(0)
            print(f'POPPED A MESSAGE FROM HISTORY!')

        #clear message history if 10 minutes have passed
        if author in self.user_history_map:
            last_message_timestamp = self.user_history_timestamp[author]
            ten_minutes_ago = datetime.now() - timedelta(minutes=10)
            
            print(f'Last Message Timestamp = {last_message_timestamp}')
            print(f'Ten minutes ago = {ten_minutes_ago}')
            
            if last_message_timestamp < ten_minutes_ago:
                message_history = []
                print(f'MESSAGE HISTORY CLEARED!')        


        curr_prompt = {'role': 'user', 'content': prompt}
        message_history.append(curr_prompt)
        #print(f'Message History PRE: {message_history}')

        response = client.chat.completions.create(model="gpt-4", messages=message_history, temperature=0, max_tokens=1000)

        response_message = response.choices[0].message.content
        print(f'Response Message: {response_message}')
        response_message_length = len(response_message)
        print(f'Message Length: {response_message_length}')

        if response_message_length > 2000:
            response_message_chunks = chunkstring(response_message, 1500)
            for chunk in response_message_chunks:
                print(f'Chunk Length: {len(chunk)}')
                await context.send(f'```{chunk}```')
        else:
            await context.send(f'```{response_message}```')
        
        curr_response = {'role': 'system', 'content': response_message}
        message_history.append(curr_response)
        print(f'Message History: {message_history}')

        self.user_history_map[author] = message_history
        self.user_history_timestamp[author] = datetime.now()
        

def chunkstring(string, length):    
    return (string[0+i:length+i] for i in range(0, len(string), length))


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(OpenAI(bot))
