###
# Copyright (c) 2016, kongr45gpen
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircmsgs as ircmsgs
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('TheNap')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x
from datetime import datetime, time

class TheNap(callbacks.Plugin):
    """Tells the_map to go to sleep"""

    lastWarning = None

    def do_privmsg_notice(self, irc, msg):
        channel = msg.args[0]
        if not irc.isChannel(channel):
            return

    def doPrivmsg(self, irc, msg):
        #if not callbacks.addressed(irc.nick, msg): #message is not direct command
        self.do_privmsg_notice(irc, msg)

        timestamp = getattr(msg, 'receivedAt', None)

        if self.lastWarning is not None and timestamp - self.lastWarning < 22*60:
            return

        prefix = msg.prefix
        prefixen = [ "themap", "the_map", "the-map", "xdotool" ]
        found = False
        for word in prefixen:
            if word in prefix:
                found = True

        if found == False:
            return

        msgtime = datetime.fromtimestamp(timestamp - 10*60*60).time()
        if msgtime >= time(05,00) or msgtime < time(01,10):
            # not sleeping time for the map
            return

        channel = "##alezakos"

        msgChannel = msg.args[0]
        if msgChannel == "#sujevo" or msgChannel == "#sujevo-dev":
            channel = msgChannel

        message = "%s: it is too late, you shall go to bed!" % (msg.nick)
        irc.queueMsg(ircmsgs.privmsg(channel, message))

        self.lastWarning = timestamp


Class = TheNap


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
