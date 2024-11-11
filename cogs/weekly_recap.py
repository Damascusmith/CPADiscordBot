# Weekly recap written and developed by Hannah Alkenbrack <3
# and William Wickenden

# Import the disnake library to interact with the Discord API.
# disnake is a Python library that allows us to create Discord bots.
import disnake, json
# Import necessary modules from disnake for commands and scheduled tasks.
from disnake.ext import commands, tasks
#used to show users options they can select for courses
from typing import Literal

with open('data/courses.json', 'r') as file:
    data = json.load(file)

# Import the datetime module to handle dates and times (for scheduling weekly tasks).
import datetime

# Define a class to handle all the weekly recap-related commands and actions.
class weeklyRecapCommand(commands.Cog):
    """
    This class contains all the commands and tasks related to weekly recaps.
    It will allow users to update recaps for specific courses and will send
    weekly updates automatically.
    """

    def __init__(self, bot):
        """
        Initializes the cog (module) for managing weekly recaps.
        
        Parameters:
        - bot: This is the bot instance that this cog is attached to. It allows the cog 
          to interact with the bot and the Discord API.
        """
        self.bot = bot  # Store the bot instance to be able to interact with Discord later.
        
        # List to store weekly update contributions.
        # Will need to link to database
        self.weekly_contributions = []

        # Start the background task that will send weekly recaps at the scheduled time.
        # This task will run automatically when the cog is loaded.
        self.weekly_recap_task.start()

    @commands.slash_command(description="Add or update the weekly recap for a course.")
    async def add_recap(self, 
                        inter: disnake.ApplicationCommandInteraction, 
                        action: Literal['COMP206', 'COMP333', 'COMP1081', 'COMP220']): # type: ignore
        """
        This is a slash command that allows users to add or update the recap for a given course.
        
        Parameters:
        - inter: The interaction that triggered this command, used to send a response back to the user.
        - course: The name of the course for which the recap should be added or updated.
        - recap: The new recap message to be stored for the specified course.
        """
            
        #William Wickenden - Nov 10, 2024
        #Added an append to the weekly contributions
        #so it actually gets added to the array
        self.weekly_contributions.append(f"{course}: {recap}")
        
        await inter.response.send_message(f"Weekly recap for {course} updated!")
    
    #testing -- Delete later
    @commands.slash_command(description="Lists Courses Json")
    async def list_json(self, inter: disnake.ApplicationCommandInteraction):

        json_list_msg = ""
        for course in course_list:
            json_list_msg += course + "\n"
        
        await inter.response.send_message("json list test:\n\n" + json_list_msg)

    @commands.slash_command(description="Lists Courses Json")
    async def json_test(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message(course_list)
   
    @tasks.loop(hours=168)  # This task runs every 168 hours, which is equivalent to one week.
    async def weekly_recap_task(self):
        """
        This task sends out the weekly recap every Sunday at a specific time (9 AM in this case).
        It will iterate through the courses and send the recap for each one.
        """
        # Get the current time in UTC
        now = datetime.datetime.utcnow()

        # Check if it's Sunday at 9 AM (or any other time you want to send weekly recaps)
        if now.weekday() == 6 and now.hour == 9:  # Weekday 6 is Sunday, and 9 is 9 AM.
            channel = self.bot.get_channel(1304148534114914364)  # hardcoded channel ID  for channel ID (NEED TO CHANGE LATER MAYBE TO MANUALLY ENTER INSTEAD OF HARDCODED).
            recap_message = "Here are the weekly recaps:\n"
            
            # Iterate over all courses and their recaps, appending them to the message.
            for course, recap in self.recap_data.items():
                recap_message += f"\n{course}: {recap}"
            
            # Send the message to the specified channel
            await channel.send(recap_message)
            
            print("Weekly recap sent!")
    
    

    #William Wickenden - Nov 10, 2024
    #Wrote a list function for all current contributions
    #to the weekly recap

    @commands.slash_command(description="lists all current recap content")
    async def weekly_recap_list(self, inter: disnake.ApplicationCommandInteraction):
        """
        This slash command prints all of the currently loaded
        tasks for the recap
        """
        recap_list_msg = ""
        for contribution in self.weekly_contributions:
            recap_list_msg += contribution + "\n"
        
        await inter.response.send_message("Here is the weekly recap list:\n\n" + recap_list_msg)

        
def setup(bot):
    bot.add_cog(weeklyRecapCommand(bot))


