import discord
import os
import statsapi
import pytz
from datetime import datetime
from dateutil import parser
from dateutil.tz import tzutc, tzlocal
from pybaseball import playerid_lookup, statcast_pitcher, standings, top_prospects
from datetime import date
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

bot = commands.Bot(command_prefix="!")

today = date.today()
todayDate = today.strftime("%m/%d/%Y")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(name='player')
async def player(ctx, firstName, lastName):
    pid = playerid_lookup(lastName, firstName)
    await ctx.send(pid)

@bot.command(name='prospects')
async def prospects(ctx, team):
    data = top_prospects(team)
    rank = data.iloc[0:9,0:1]
    playerName = data.iloc[0:9,1:2]
    age = data.iloc[0:9,2:3]
    rank = rank.to_string(index=False, header=False)
    playerName = playerName.to_string(index=False, header=False)
    age = age.to_string(index = False, header = False)
    embed=discord.Embed(title=team.capitalize() + " Top 10 Prospects")
    embed.add_field(name="Rank", value=rank, inline=True)
    embed.add_field(name="Player", value=playerName, inline=True)
    embed.add_field(name="Age", value=age, inline=True)
    await ctx.send(embed=embed)

@bot.command(name='standings')
async def divisionStandings(ctx, *args):
    year = int(args[0])
    league = args[1]
    div = args[2]
    divDisplay = (league.upper() + " " + div.capitalize())
    if(league.upper() == "AL"):
        if(div.upper() == "EAST"):
            divPass = 0
        elif(div.upper() == "CENTRAL"):
            if(year >= 1994):
                divPass = 1
            else:
                await ctx.send(divDisplay + " does not exist in that year.")
        elif(div.upper() == "WEST"):
            if(year <= 1994):
                divPass = 1
            else:
                divPass = 2
    else:
        if(div.upper() == "EAST"):
            if(year <= 1994):
                divPass = 2
            else:
                divPass = 3
        elif(div.upper() == "CENTRAL"):
            if(year >= 1994):
                divPass = 4
            else:
                await ctx.send(divDisplay + " does not exist in that year.")
        elif(div.upper() == "WEST"):
            if(year >= 1994):
                divPass = 5
            else:
                divPass = 3
    try:
        data = standings(year)[divPass]
        i = 0
        j = 1
        k = data.shape[0]
        winLoss=""
        teamList=""
        for i in range(0,k):
            teams = data.iloc[i:j,0:1]
            wins = data.iloc[i:j,1:2]
            losses = data.iloc[i:j,2:3]
            teams = teams.to_string(index = False, header = False)
            teamList += (teams + "\n")
            wins = wins.to_string(index = False, header = False)
            losses = losses.to_string(index = False, header = False)
            winLoss += wins + "-" + losses + "\n"
            j += 1
        winPct = data.iloc[0:j,3:4]
        winPct = winPct.to_string(index = False, header = False)
        embed=discord.Embed(title=str(year) + " " + divDisplay + " Standings")
        embed.add_field(name="Team", value=teamList, inline=True)
        embed.add_field(name="W-L", value=winLoss, inline=True) 
        embed.add_field(name="Win Percentage", value=winPct, inline=True)
        await ctx.send(embed=embed)
    except UnboundLocalError:
        pass


@bot.command(name='games')
async def dateGames(ctx, *args):
    if (len(args) == 0):
        datePass = today
    else:
        datePass = args[0]
    games = statsapi.schedule(date=datePass)
    timeZone = pytz.timezone("America/Detroit")
    now = datetime.now()
    gameText = ""
    for x in games:
        gameUtc = parser.parse(x['game_datetime'])
        gameLocal = gameUtc.astimezone(timeZone)
        currentTime = now.astimezone(timeZone)
        gameTime = datetime.strftime(gameLocal, '%I:%M %p %Z')
        if (gameLocal > currentTime):
            gameText += (x['away_name'] + " at " + x['home_name'] + " - " + gameTime + "\n")
        else:
            if(x['status'] == "In Progress"):
                gameText += (x['away_name'] + " (" + str(x['away_score']) + ") at " + x['home_name'] + " (" + str(x['home_score']) + ") - " + x['inning_state'].capitalize() + x['current_inning'] + "\n")
            else:
                gameText += (x['away_name'] + " (" + str(x['away_score']) + ") at " + x['home_name'] + " (" + str(x['home_score']) + ") - " + x['status'] + "\n")
    await ctx.send(gameText.rstrip())



bot.run(os.getenv('TOKEN'))