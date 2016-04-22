from errbot import BotPlugin, botcmd
from parser_task import ParserTask
import settings

class Appeals(BotPlugin):
    """ Ban appeal alerts """

    def activate(self):
        super().activate()
        task = ParserTask(self)

    @botcmd
    def appeals(self, msg, args):
        """ Open ban appeals """
        appeals = self['APPEALS']
        if len(appeals) > 0:
            msg = "There are " + str(len(appeals)) + " open ban appeals.\n\n"
            for a in appeals:
                msg = msg + "• _" + a[1] + "_ " + a[0] + "\n\n"
            return msg
        else:
            return "There are no open appeals."

    @botcmd(admin_only=True)
    def clearappeals(self, msg, args):
        """ Clear cached data """
        self['BOOKMARK'] = ""
        self['APPEALS'] = ""
        return "Appeal cache reset."
