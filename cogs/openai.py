""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import os
from datetime import datetime, timedelta
import openai
import discord
from discord.ext import commands
from discord.ext.commands import Context

# Here we name the cog and create a new class for the cog.
class OpenAI(commands.Cog, name="openai"):
    def __init__(self, bot):
        self.bot = bot
        self.user_history_map = {}
        self.user_history_timestamp = {}
        #print(f'Message History: {self.message_history}')

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.



    @commands.hybrid_command(
        name="ask3",
        description="OpenAI chatbot.",
    )
    async def ask3(self, context: Context, prompt: str):

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
        print(f'Message History: {message_history}')

        openai.api_key = os.environ.get("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message_history, temperature=0, max_tokens=1000)

        print(f'Response: {response}')

        for choice in response['choices']:
            await context.send(choice['message']['content'])
            curr_response = {'role': 'assistant', 'content': choice['message']['content']}
            message_history.append(curr_response)

        self.user_history_map[author] = message_history
        self.user_history_timestamp[author] = datetime.now()
        


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(OpenAI(bot))
