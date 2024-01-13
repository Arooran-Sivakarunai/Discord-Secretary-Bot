import discord
from discord.ext import commands
import scheduler
from datetime import datetime, timedelta
import gpt_connecter
import os

#Initialize scheduler object
schedule = scheduler.Scheduler()

#send message 
async def send_message(message, user_message):
    try:
        await message.channel.send(user_message)
    except Exception as e:
        return "UH OH" + str(e)

#function controls discord bot
def run_discord_bot():
    #Initialize Intents
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guild_scheduled_events = True
    client = commands.Bot(command_prefix='!', intents=intents)
    
    #Runs on bot startup
    @client.event
    async def on_ready():
        print(f'`{client.user} is now ready to rumble!`')

    #Captures every message, and parses for commands 
    @client.event
    async def on_message(message):
        #Prevents Infinite loop
        if message.author == client.user:
            return
        #Checks if message invokes a command
        if message.content.startswith('!'):
            await client.process_commands(message)   
    
    #!addweekly command
    @client.command(name='addweekly')
    async def add_weekly(ctx, *args):
        try:    
            #Add event to schedule instance
            schedule.add_weekly_event(scheduler.Weekly_Event(int(args[0]),args[1],args[2]," ".join(args[3:])))
            temp = f"```Added \"{' '.join(args[3:])}\" to {scheduler.Weekly_Event.get_weekday(int(args[0]))}```"         
            #send confirmation message
            await send_message(ctx, temp)
        except scheduler.InvalidArgumentsException as e:
            #send denial message
            await send_message(ctx, '```Unable to create that event```')
    
    #!addreminder command
    @client.command(name='addreminder')
    async def add_reminder(ctx, *args):
        try:
            #Add reminder to schedule instance
            schedule.add_one_time_event(scheduler.One_Time_Event(args[0], args[1], args[2], args[3:]))
            temp = f"```Added \"{' '.join(args[3:])}\" on {args[0]} {args[1]} @ {args[2]} to the reminders!```"         
            #Send confirmation message
            await send_message(ctx, temp)
        except scheduler.InvalidArgumentsException as e:
            #Send denial message
            await send_message(ctx, '```Unable to create that event```')
    
    #!delweekly command
    @client.command(name='delweekly')
    async def del_weekly(ctx, *args):
        #Delete Event
        if schedule.del_weekly_event(scheduler.Weekly_Event(int(args[0]), "", "", ' '.join(args[1:]))):
            temp = f"Removed {args[1:]}"
            #Send Confirmation Message
            await send_message(ctx, temp)
        else:
            #Send Denial Message
            await send_message(ctx, "```Failed to delete event```")
    
    #!delreminder command
    @client.command(name='delreminder')
    async def del_reminder(ctx, *args):
        #Delete Reminder
        if schedule.del_weekly_event(scheduler.One_Time_Event(0, 0, "", ' '.join(args))):
            temp = f"Removed {args[1:]}"
            #Send Confirmation Message
            await send_message(ctx, temp)
        else:
            #Send Denial Message
            await send_message(ctx, "```Failed to delete reminder```")
    
    #!today command
    @client.command(name="today")
    async def today(ctx, *args):
        #Grabs all of today's events
        events = schedule.get_dates_events(datetime.today())
        temp = "```"
        for event in events:
            temp += str(event) + "\n------\n"
        temp += "```"
        #Send Confirmation Message
        await send_message(ctx, temp)
    
    #!tommorow command
    @client.command(name="tommorow")
    async def tommorow(ctx, *args):
        #Grabs all of Tommorow's events
        events = schedule.get_dates_events(datetime.today() + timedelta(days=1))
        temp = "```"
        for event in events:
            temp += str(event) + "\n------\n"
        temp += "```"
        #Send Confirmation Message
        await send_message(ctx, temp)
    
    #!q command
    @client.command(name='q')
    async def get_LLM_response(ctx, *args):
        #Get Response from LLM
        temp = "```" + gpt_connecter.get_response(" ".join(args)) + "```"
        #Sends Confirmation Message
        await send_message(ctx, temp)
    
    #!resetweekly command
    @client.command(name='resetweekly')
    async def reset_weekly(ctx, *args):
        schedule.reset_weekly_events()
        #Confirmation Message
        await send_message(ctx, "```Your weekly events have been reset!```")
    
    #!resetreminders command
    @client.command(name='resetreminders')
    async def reset_daily(ctx, *args):
        schedule.reset_one_time_events()
        #Confirmation Message
        await send_message(ctx, "```Your one-time reminders have been reset!```")
