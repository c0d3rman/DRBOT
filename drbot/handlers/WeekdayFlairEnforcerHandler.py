from __future__ import annotations
from typing import Optional
from praw.models import Submission
from datetime import datetime
from drbot import settings, log
from drbot.agents import Agent
from drbot.util import is_mod, send_modmail
from drbot.handlers import Handler


class WeekdayFlairEnforcerHandler(Handler[Submission]):
    """On a given day of the week, removes posts without a given flair template and replies to them."""

    def __init__(self, flair_id: str, weekday: int, name: Optional[str] = None, ):
        super().__init__(name=name)
        assert 0 <= weekday and weekday <= 6

        self.flair_id = flair_id
        self.weekday = weekday

    def setup(self, agent: Agent[Submission]) -> None:
        super().setup(agent)

        # Get the text of the allowed flair
        flair_text = [x for x in self.reddit.subreddit(settings.subreddit).flair.link_templates.__iter__() if x['id'] == self.flair_id]
        if len(flair_text) == 0:
            raise Exception(f"Flair template ID {self.flair_id} doesn't exist on your sub.")
        self.flair_text = flair_text[0]['text']

    def handle(self, item: Submission) -> None:
        # Check it's the weekday and the post was made on the weekday
        if datetime.now().weekday() != self.weekday or datetime.fromtimestamp(item.created_utc).weekday() != self.weekday:
            return

        # Check that the post doesn't the flair template ID
        flair_id = None
        if not item.link_flair_text is None:  # Posts with no flair have no link_flair_template_id property
            flair_id = item.link_flair_template_id
        if flair_id == self.flair_id:
            return

        # Ignore mod posts
        if is_mod(self.reddit, item.author):
            return

        log.info(f"Illegal weekday flair detected on post {item.fullname}")

        # Remove the post
        post = self.reddit.submission(item.id)
        if settings.dry_run:
            log.info(f"[DRY RUN: would have removed post {post.fullname}]")
        else:
            post.remove(mod_note="DRBOT: removed for weekday flair restriction", reason_id=None)  # TBD reason ID

        # Modmail the user
        send_modmail(self.reddit, add_common=False,
                     subject=f"Your post was removed due to Rule 8: Fresh Friday",
                     body=f"""Hi u/{post.author}, your [post](https://reddit.com{post.permalink}) was removed because of Rule 8: Fresh Friday.

On Fridays, all posts must discuss fresh topics. We encourage posts about religions other than Christianity/Islam/atheism. Banned topics include: problem of evil, Kalam, fine tuning, disciple martyrdom, Quranic miracles, classical theism.

To make a post on Friday, you must flair your post with “Fresh Friday.” If your post was on a fresh topic, please post it again with the correct flair.""")

        # print(f"Your post has forbidden flair: {item.link_flair_text}.\nIt must have this flair: {self.flair_text}")