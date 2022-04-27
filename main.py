import discord
import os
import statsapi
import pytz
from datetime import datetime
from dateutil import parser
from pybaseball import standings
from datetime import date
from dotenv import load_dotenv
from teamInfo import teamList
from divInfo import divList

load_dotenv()

bot = discord.Bot()

today = date.today()
todayDate = today.strftime("%m/%d/%Y")


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(name='player', description="Display's a player's current season or career stats. Defaults to current season.")
async def player(ctx, playername: discord.Option(str, required=True), scope: discord.Option(str, choices=["season"], default="season", required=False)):
    statType=scope
    player = statsapi.lookup_player(playername)
    pid = player[0]['id']
    playerName = player[0]['fullName']
    position = player[0]['primaryPosition']['abbreviation']
    
    if position == "TWP":
        twpData = statsapi.player_stat_data(pid, group="[hitting,pitching]", type=statType)
        season = twpData['stats'][0]['season']
        batting = twpData['stats'][0]['stats']
        pitching = twpData['stats'][1]['stats']

        battingStats = playerName + " " + season + " Batting Stats\n"  + str(batting['atBats']) + " AB\t" + str(batting['avg']) + " AVG\t" + str(batting['homeRuns']) + " HR\t" \
        + str(batting['rbi']) + " RBI\n\n"

        pitchingStats = playername + " " + season + " Pitching Stats\n"  + str(pitching['wins']) + "-" + str(pitching['losses']) + " W/L\t" + str(pitching['era']) + " ERA\t" \
        + str(pitching['inningsPitched']) + " IP\t" + str(pitching['gamesPlayed']) +" GP\t"

        stats = battingStats + pitchingStats

        await ctx.respond(stats)
    elif position == "P":
        statData = statsapi.player_stat_data(pid, group="[pitching]", type=statType)
        pitching = statData['stats'][0]['stats']
        season = statData['stats'][0]['season']

        stats = playerName + " " + season + " Pitching Stats\n\n"  + str(pitching['wins']) + "-" + str(pitching['losses']) + " W/L\t" + str(pitching['era']) + " ERA\t" \
        + str(pitching['inningsPitched']) + " IP\t" + str(pitching['gamesPlayed']) +" GP\t"

        await ctx.respond(stats)
    else:
        statData = statsapi.player_stat_data(pid, group="[hitting]", type=statType)
        batting = statData['stats'][0]['stats']
        season = statData['stats'][0]['season']

        stats = playerName + " " + season + " Batting Stats\n"  + str(batting['atBats']) + " AB\t" + str(batting['avg']) + " AVG\t" + str(batting['homeRuns']) + " HR\t" \
        + str(batting['rbi']) + " RBI\n\n"
        await ctx.respond(stats)
        

@bot.command(name='standings', description="Displays division standings for specified year. Defaults to current year.")
async def divisionStandings(ctx, league: discord.Option(str), div: discord.Option(str), year: discord.Option(str, required=False, default = date.today().year)):
    await ctx.defer()
    divDisplay = (league.upper() + " " + div.capitalize())
    for i in divList:
        if (divDisplay == i['name']):
            if year >= 1994:
                divPass = i['postRealignmentID']
            else:
                divPass = i['preRealignmentID']
    try:
        data = standings(year)[divPass]
        i = 0
        j = 1
        k = data.shape[0]
        winLoss = ""
        teamList = ""
        for i in range(0, k):
            teams = data.iloc[i:j, 0:1]
            wins = data.iloc[i:j, 1:2]
            losses = data.iloc[i:j, 2:3]
            teams = teams.to_string(index=False, header=False)
            teamList += (teams + "\n")
            wins = wins.to_string(index=False, header=False)
            losses = losses.to_string(index=False, header=False)
            winLoss += wins + "-" + losses + "\n"
            j += 1
        winPct = data.iloc[0:j, 3:4]
        winPct = winPct.to_string(index=False, header=False)
        embed = discord.Embed(title=str(year) + " " + divDisplay + " Standings")
        embed.add_field(name="Team", value=teamList, inline=True)
        embed.add_field(name="W-L", value=winLoss, inline=True)
        embed.add_field(name="Win Percentage", value=winPct, inline=True)
        await ctx.respond(embed=embed)
    except UnboundLocalError:
        await ctx.respond("You have entered an invalid division.")
    except TypeError:
        await ctx.respond("You have entered a division that does not exist in " + str(year) + ".")


@bot.command(name='games', description="Displays all games for a specified date. Defaults to current day.")
async def dateGames(ctx, date: discord.Option(str, required=False, default=today)):
    await ctx.defer()
    games = statsapi.schedule(date=date)
    timeZone = pytz.timezone("America/Detroit")
    now = datetime.now()
    gameText = ""
    for x in games:
        gameUtc = parser.parse(x['game_datetime'])
        gameLocal = gameUtc.astimezone(timeZone)
        currentTime = now.astimezone(timeZone)
        gameTime = datetime.strftime(gameLocal, '%I:%M %p %Z')
        for y in teamList:
            if (x['away_name'] == y['name']):
                awayTeam = y['fileCode'].upper()
            if (x['home_name'] == y['name']):
                homeTeam = y['fileCode'].upper()
        if (gameLocal > currentTime):
            gameText += (awayTeam + " at " +
                         homeTeam + " - " + gameTime + "\n")
        else:
            if(x['status'] == "In Progress"):
                gameText += (awayTeam + " (" + str(x['away_score']) + ") at " + homeTeam + " (" + str(x['home_score']) + ") - " + x['inning_state'].capitalize() + " " + str(x['current_inning']) + "\n")
            else:
                gameText += (awayTeam + " (" + str(x['away_score']) + ") at " +
                             homeTeam + " (" + str(x['home_score']) + ") - " + x['status'] + "\n")
    await ctx.respond(gameText.rstrip())


@bot.command(name='lastgame', description="Displays the line score from the specified team's last game.")
async def lastGame(ctx, team: discord.Option(str, required=True)):
    for y in teamList:
        if (team.casefold() == y['teamName'].casefold()):
            teamID = y['id']
    lastGame = statsapi.last_game(teamID)
    await ctx.respond("```"+ statsapi.linescore(lastGame) + "```")

bot.run(os.getenv('TOKEN'))