import discord
from datetime import datetime

client = discord.Client()

birthdays = {}  # dictionary to store user IDs and birthdays

@client.event
async def on_message(message):
    if message.content.startswith("!register"):
        # extract the user's birthday from the command
        try:
            birthday = message.content.split(" ")[1]
            birthday_date = datetime.strptime(birthday, "%m-%d").date()
        except (ValueError, IndexError):
            await message.channel.send("Invalid birthday format. Please use MM-DD.")
            return
        
        # store the user's ID and birthday in the dictionary
        birthdays[message.author.id] = birthday_date
        await message.channel.send("Birthday successfully registered!")
    
@client.event
async def on_ready():
    print("Bot is ready.")
    
    # check every hour if it is someone's birthday
    while True:
        await client.wait_until_ready()
        
        # get the current date
        today = datetime.now().date()
        
        # check if any registered users have a birthday today
        for user_id, birthday in birthdays.items():
            if birthday.month == today.month and birthday.day == today.day:
                user = client.get_user(user_id)
                await user.send(f"Happy birthday, {user.name}!")
                channel = client.get_channel(CHANNEL_ID)  # replace CHANNEL_ID with the ID of the channel you want to send the message to
                await channel.send(f"Happy birthday, {user.mention}!")
        
        # wait an hour before checking again
        await asyncio.sleep(21600)
        
        '''
        # check if it is midnight
        if today.hour == 0 and today.minute == 0:
            await check_birthdays()
        
        # wait 60 seconds before checking the time again
        await asyncio.sleep(60)
        '''

client.run("TOKEN")  # replace TOKEN with your bot's token
