# mlb-discord-bot

## About

mlb-discord-bot is a Discord bot written in Python for displaying Major League Baseball stats and other information. It's kind of jank and should probably not be used in production. To be honest, it's mainly a way for me to learn more about and tinker with APIs.

# Quick Start

1. Clone the repository:
   
   ```
   git clone https://github.com/nitrowv/mlb-discord-bot.git
   ```
2. Create a virtual environment (optional):
   ```
   python3 -m venv <NAME OF YOUR VENV>
   ```

   and activate it:
   ```
   Windows: <NAME OF YOUR VENV>\Scripts\Activate.ps1

   Linux:   source <NAME OF YOUR VENV>/bin/activate
   ```

3. Install required libraries:
   ```
   pip3 install -r requirements.txt
   ```

4. Obtain your Bot token from the Discord developer portal and place it in a ```.env``` file in the root directory in the format of:

    ```
    TOKEN=INSERT_YOUR_TOKEN_HERE
    ```
    Take care to ensure that you have generated an OAuth URL with the ```applications.commands``` permission.

5. Run the script!

# Current Commands

As of April 26, 2022, the commands have been updated to use Discord's slash command notation.

```
/standings league division [year]
```

If no year provided, displays current standings for the given league and division in an embed. If `year` is provided, displays the year's final standings for the division.

![Standings](/.github/images/standings.png)

```
/games [date]
```

Displays current day's games if `date` not given, otherwise displays games for supplied date.

![Games](/.github/images/games-with-date.png)

```
/player playerName
```

Displays player's statistics for the current season. Functionality to output career or individual other seasons are in development.

![Standings](/.github/images/player.png)

```
/lastgame teamName
```

Displays the last line score for the given team.

![Last Game](/.github/images/lastgame.png)

# Credit
This project was created by Tanner Johnston.

Tools used to retrieve data are [pybaseball](https://github.com/jldbc/pybaseball), created by James LeDoux; and [MLB-StatsAPI](https://github.com/toddrob99/MLB-StatsAPI), created by Todd Roberts.

Communication with Discord is handled by the [Pycord](https://github.com/Pycord-Development/pycord) API wrapper.