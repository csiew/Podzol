# Podzol
Another podcast app?! Yeah, I sometimes just want a podcast app that's barebones in both its feature-set and in storage use (that means streaming only, no downloading of MP3 files... for now).

Podzol is written in Python and uses JSON as a 'medium of storage' rather than a database (e.g. SQLite). The CLI client uses [pygame](https://www.pygame.org/news) for audio playback functionality, and uses [a class written by *sloth* (sic)](https://stackoverflow.com/a/58763348) to handle audio streaming.

## User Guide
Podzol is navigable through a rudimentary CLI interface. This requires you to use the commands listed below. The selection of a podcast or episode requires you to use flags (`-f [number]` for the podcast; `-e [number]` for the episode). You can refer to the numbers needed to select a podcast or episode using the `list`.

## Commands
- `help`: Shows a list of commands
- `search [keywords]`: Search for podcasts or episodes (doesn't do much at the moment... to be fixed)
- `list -f`: List all podcasts
- `list -f [key1]`: List all episodes of a podcast
- `list -f [key1] -e [key2]`: Display info about a specific episode
- `play -f [key1] -e [key2]`: Play a podcast episode
- `delete -f [key1]`: Remove a podcast from your library
- `reload`: Reload the data from the JSON indexes
- `exit`: Exit Podzol

## Future changes
1. Podzol will store its JSON files in ~/.local/share/ in Linux and macOS.
2. Explore Ncurses to replace the shell-like interface (akin to [Castero](https://github.com/xgi/castero)).
3. Use backend for more sophisticated frontend clients like GNOME/GTK or even a SwiftUI Mac app.
