import feedparser, re
import settings

class ParserTask():
    
    def __init__(self, plugin):
        self.plugin = plugin
        self.feed = feedparser.parse(settings.FEED)
        plugin.start_poller(settings.DELAY, self.run)

    def run(self):
        appeals = self.get_new_appeals()
        if len(appeals) > 0:
            self.send_alerts(appeals)

    def get_new_appeals(self):
        new = []
        current = []
        for entry in reversed(self.feed.entries):
            if entry.link == self.plugin['BOOKMARK']:
                break
            else:
                if entry.link not in settings.BLACKLIST:
                    new.append(entry)
                    self.plugin['BOOKMARK'] = entry.link
        for entry in self.feed.entries:
            if entry.link not in settings.BLACKLIST:
                current.append((entry.link, entry.title))
        self.plugin['APPEALS'] = current
        return new

    def send_alerts(self, appeals):
        channel = self.plugin.build_identifier(settings.CHANNEL)
        for appeal in appeals:
            msg = "New ban appeal: _" + appeal.title + "_ " + appeal.link
            self.plugin.send(channel, msg)

    def get_name_in_title(self, title):
        regex = r"^.*\[(.*)\].*$"
        match = re.search(regex, title)
        if match:
            return match.group(1).lower()
        else:
            return None
