# DRBOT - a points-to-ban Reddit moderation bot


DRBOT (Do Really Boring Overhead Tasks) is a reddit bot that automatically monitors a subreddit and tracks removals. Each removal of a user's submission gives that user a certain number of points, and once their points hit some threshold, the bot takes action, either by notifying the mods or automatically banning the user.

## Setup

1. Clone this repo and cd inside.
2. `pip install -r requirements.txt`
3. Run first-time setup: `python first_time_setup.py`. This will also create a settings file for you.
4. Change any other settings you want in `data/settings.toml`.
5. Run the bot: `python main.py`

## Caveats

Re-approving and then re-deleting a comment deletes the removal reason on reddit's side, so if you do this, be aware that DRBOT will treat the removal as having no reason as well.

&nbsp;

<p xmlns:dct="http://purl.org/dc/terms/" xmlns:vcard="http://www.w3.org/2001/vcard-rdf/3.0#">
  <a rel="license"
     href="http://creativecommons.org/publicdomain/zero/1.0/">
    <img src="http://i.creativecommons.org/p/zero/1.0/88x31.png" style="border-style: none;" alt="CC0" />
  </a>
</p>