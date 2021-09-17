# mlb-discord-bot
## About
mlb-discord-bot is a Discord bot created in Python for displaying Major League Baseball stats and other information in Discord.
# Current Commands
```
!standings [year] league division
```

If no year supplied, displays current standings for the given league and division in an embed. If `year` is provided, displays the year's final standings for the supplied division.

![Standings](/.github/images/standings.png)

```
!games [date]
```

Displays current day's games if `date` not given, otherwise displays games for supplied date.
![Standings](/.github/images/games-with-date.png)

```
!prospects team
```

Displays a list of the supplied team's top 10 prospects in an embed. Does not work for all teams due to some teams having a different URL for the data.

![Standings](/.github/images/prospects.png)

```
!player firstName lastName
```

Displays player's id numbers for MLB.com, Baseball-Reference, and Fangraphs, as well as the first and last years of Major League play.
![Standings](/.github/images/player.png)

# Credit
This project was created by Tanner Johnston.

Tools used to retrieve data are [pybaseball](https://github.com/jldbc/pybaseball), created by James LeDoux; and [MLB-StatsAPI](https://github.com/toddrob99/MLB-StatsAPI), created by Todd Roberts.

Communication with Discord is handled by the [discord.py](https://github.com/Rapptz/discord.py) API wrapper created by Rapptz.