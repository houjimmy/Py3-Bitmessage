"""Helper Start performs all the startup operations."""

import ConfigParser
from bmconfigparser import BMConfigParser
import defaults
import sys
import os
import platform
from distutils.version import StrictVersion

import paths
import state
import helper_random

# The user may de-select Portable Mode in the settings if they want
# the config files to stay in the application data folder.
StoreConfigFilesInSameDirectoryAsProgramByDefault = False


def _loadTrustedPeer():
    try:
        trustedPeer = BMConfigParser().get('bitmessagesettings', 'trustedpeer')
    except ConfigParser.Error:
        # This probably means the trusted peer wasn't specified so we
        # can just leave it as None
        return

    host, port = trustedPeer.split(':')
    state.trustedPeer = state.Peer(host, int(port))


def loadConfig():
    if state.appdata:
        BMConfigParser().read(state.appdata + 'keys.dat')
        # state.appdata must have been specified as a startup option.
        needToCreateKeysFile = BMConfigParser().safeGet(
            'bitmessagesettings', 'settingsversion') is None
        if not needToCreateKeysFile:
            print(
                'Loading config files from directory specified'
                ' on startup: %s' % state.appdata)
    else:
        BMConfigParser().read(paths.lookupExeFolder() + 'keys.dat')
        try:
            BMConfigParser().get('bitmessagesettings', 'settingsversion')
            print 'Loading config files from same directory as program.'
            needToCreateKeysFile = False
            state.appdata = paths.lookupExeFolder()
        except:
            # Could not load the keys.dat file in the program directory.
            # Perhaps it is in the appdata directory.
            state.appdata = paths.lookupAppdataFolder()
            BMConfigParser().read(state.appdata + 'keys.dat')
            needToCreateKeysFile = BMConfigParser().safeGet(
                'bitmessagesettings', 'settingsversion') is None
            if not needToCreateKeysFile:
                print 'Loading existing config files from', state.appdata

    if needToCreateKeysFile:

        # This appears to be the first time running the program; there is
        # no config file (or it cannot be accessed). Create config file.
        BMConfigParser().add_section('bitmessagesettings')
        BMConfigParser().set('bitmessagesettings', 'settingsversion', '10')
        BMConfigParser().set('bitmessagesettings', 'port', '8444')
        BMConfigParser().set(
            'bitmessagesettings', 'timeformat', '%%c')
        BMConfigParser().set('bitmessagesettings', 'blackwhitelist', 'black')
        BMConfigParser().set('bitmessagesettings', 'startonlogon', 'false')
        if 'linux' in sys.platform:
            BMConfigParser().set(
                'bitmessagesettings', 'minimizetotray', 'false')
        # This isn't implimented yet and when True on
        # Ubuntu causes Bitmessage to disappear while
        # running when minimized.
        else:
            BMConfigParser().set(
                'bitmessagesettings', 'minimizetotray', 'true')
        BMConfigParser().set(
            'bitmessagesettings', 'showtraynotifications', 'true')
        BMConfigParser().set('bitmessagesettings', 'startintray', 'false')
        BMConfigParser().set('bitmessagesettings', 'socksproxytype', 'none')
        BMConfigParser().set(
            'bitmessagesettings', 'sockshostname', 'localhost')
        BMConfigParser().set('bitmessagesettings', 'socksport', '9050')
        BMConfigParser().set(
            'bitmessagesettings', 'socksauthentication', 'false')
        # BMConfigParser().set(
        #     'bitmessagesettings', 'sockslisten', 'false')
        BMConfigParser().set('bitmessagesettings', 'socksusername', '')
        BMConfigParser().set('bitmessagesettings', 'sockspassword', '')
        BMConfigParser().set('bitmessagesettings', 'keysencrypted', 'false')
        BMConfigParser().set(
            'bitmessagesettings', 'messagesencrypted', 'false')
        BMConfigParser().set(
            'bitmessagesettings', 'defaultnoncetrialsperbyte',
            str(defaults.networkDefaultProofOfWorkNonceTrialsPerByte))
        BMConfigParser().set(
            'bitmessagesettings', 'defaultpayloadlengthextrabytes',
            str(defaults.networkDefaultPayloadLengthExtraBytes))
        BMConfigParser().set('bitmessagesettings', 'minimizeonclose', 'false')
        # BMConfigParser().set(
        #     'bitmessagesettings', 'maxacceptablenoncetrialsperbyte', '0')
        # BMConfigParser().set(
        #     'bitmessagesettings', 'maxacceptablepayloadlengthextrabytes',
        #     '0')
        BMConfigParser().set('bitmessagesettings', 'dontconnect', 'true')
        # BMConfigParser().set('bitmessagesettings', 'userlocale', 'system')
        # BMConfigParser().set('bitmessagesettings', 'useidenticons', 'True')
        # BMConfigParser().set(
        #     'bitmessagesettings', 'identiconsuffix',
        #     ''.join(helper_random.randomchoice(
        #         "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        #         ) for x in range(12)
        #     ))  # a twelve character pseudo-password to salt the identicons
        BMConfigParser().set('bitmessagesettings', 'replybelow', 'False')
        BMConfigParser().set('bitmessagesettings', 'maxdownloadrate', '0')
        BMConfigParser().set('bitmessagesettings', 'maxuploadrate', '0')
        # BMConfigParser().set(
        #     'bitmessagesettings', 'maxoutboundconnections', '8')
        # BMConfigParser().set('bitmessagesettings', 'ttl', '367200')

        # UI setting to stop trying to send messages after X days/months
        BMConfigParser().set(
            'bitmessagesettings', 'stopresendingafterxdays', '')
        BMConfigParser().set(
            'bitmessagesettings', 'stopresendingafterxmonths', '')
        # BMConfigParser().set(
        #    'bitmessagesettings', 'timeperiod', '-1')

        # Are you hoping to add a new option to the keys.dat file? You're in
        # the right place for adding it to users who install the software for
        # the first time. But you must also add it to the keys.dat file of
        # existing users. To do that, search the class_sqlThread.py file
        # for the text: "right above this line!"

        if StoreConfigFilesInSameDirectoryAsProgramByDefault:
            # Just use the same directory as the program and forget about
            # the appdata folder
            state.appdata = ''
            print 'Creating new config files in same directory as program.'
        else:
            print 'Creating new config files in', state.appdata
            if not os.path.exists(state.appdata):
                os.makedirs(state.appdata)
        if not sys.platform.startswith('win'):
            os.umask(0o077)
        BMConfigParser().save()
    else:
        updateConfig()

    _loadTrustedPeer()


def updateConfig():
    settingsversion = BMConfigParser().getint(
        'bitmessagesettings', 'settingsversion')
    if settingsversion == 1:
        BMConfigParser().set('bitmessagesettings', 'socksproxytype', 'none')
        BMConfigParser().set(
            'bitmessagesettings', 'sockshostname', 'localhost')
        BMConfigParser().set('bitmessagesettings', 'socksport', '9050')
        BMConfigParser().set(
            'bitmessagesettings', 'socksauthentication', 'false')
        BMConfigParser().set('bitmessagesettings', 'socksusername', '')
        BMConfigParser().set('bitmessagesettings', 'sockspassword', '')
        BMConfigParser().set('bitmessagesettings', 'sockslisten', 'false')
        BMConfigParser().set('bitmessagesettings', 'keysencrypted', 'false')
        BMConfigParser().set(
            'bitmessagesettings', 'messagesencrypted', 'false')
        settingsversion = 2
    # let class_sqlThread update SQL and continue
    elif settingsversion == 4:
        BMConfigParser().set(
            'bitmessagesettings', 'defaultnoncetrialsperbyte',
            str(defaults.networkDefaultProofOfWorkNonceTrialsPerByte))
        BMConfigParser().set(
            'bitmessagesettings', 'defaultpayloadlengthextrabytes',
            str(defaults.networkDefaultPayloadLengthExtraBytes))
        settingsversion = 5

    if settingsversion == 5:
        BMConfigParser().set(
            'bitmessagesettings', 'maxacceptablenoncetrialsperbyte', '0')
        BMConfigParser().set(
            'bitmessagesettings', 'maxacceptablepayloadlengthextrabytes', '0')
        settingsversion = 7

    # Raise the default required difficulty from 1 to 2
    # With the change to protocol v3, this is obsolete.
    # if settingsversion == 6:
    #     if int(shared.config.get(
    #             'bitmessagesettings', 'defaultnoncetrialsperbyte'
    #     )) == defaults.networkDefaultProofOfWorkNonceTrialsPerByte:
    #         shared.config.set(
    #             'bitmessagesettings', 'defaultnoncetrialsperbyte',
    #             str(
    #                 defaults.networkDefaultProofOfWorkNonceTrialsPerByte
    #                 * 2)
    #         )
    #     settingsversion = 7

    if not BMConfigParser().has_option('bitmessagesettings', 'sockslisten'):
        BMConfigParser().set('bitmessagesettings', 'sockslisten', 'false')

    if not BMConfigParser().has_option('bitmessagesettings', 'userlocale'):
        BMConfigParser().set('bitmessagesettings', 'userlocale', 'system')

    if not BMConfigParser().has_option(
            'bitmessagesettings', 'sendoutgoingconnections'):
        BMConfigParser().set(
            'bitmessagesettings', 'sendoutgoingconnections', 'True')

    if not BMConfigParser().has_option(
                'bitmessagesettings', 'useidenticons'):
        BMConfigParser().set('bitmessagesettings', 'useidenticons', 'True')
    if not BMConfigParser().has_option(
            'bitmessagesettings', 'identiconsuffix'):
        # acts as a salt
        BMConfigParser().set(
            'bitmessagesettings', 'identiconsuffix',
            ''.join(helper_random.randomchoice(
                "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
                ) for x in range(12)
            ))  # a twelve character pseudo-password to salt the identicons

    # Add settings to support no longer resending messages after
    # a certain period of time even if we never get an ack
    if settingsversion == 7:
        BMConfigParser().set(
            'bitmessagesettings', 'stopresendingafterxdays', '')
        BMConfigParser().set(
            'bitmessagesettings', 'stopresendingafterxmonths', '')
        settingsversion = 8

    # With the change to protocol version 3, reset the user-settable
    # difficulties to 1
    if settingsversion == 8:
        BMConfigParser().set(
            'bitmessagesettings', 'defaultnoncetrialsperbyte',
            str(defaults.networkDefaultProofOfWorkNonceTrialsPerByte))
        BMConfigParser().set(
            'bitmessagesettings', 'defaultpayloadlengthextrabytes',
            str(defaults.networkDefaultPayloadLengthExtraBytes))
        previousTotalDifficulty = int(
            BMConfigParser().getint(
                'bitmessagesettings', 'maxacceptablenoncetrialsperbyte')
        ) / 320
        previousSmallMessageDifficulty = int(
            BMConfigParser().getint(
                'bitmessagesettings', 'maxacceptablepayloadlengthextrabytes')
        ) / 14000
        BMConfigParser().set(
            'bitmessagesettings', 'maxacceptablenoncetrialsperbyte',
            str(previousTotalDifficulty * 1000))
        BMConfigParser().set(
            'bitmessagesettings', 'maxacceptablepayloadlengthextrabytes',
            str(previousSmallMessageDifficulty * 1000))
        settingsversion = 9

    # Adjust the required POW values for each of this user's addresses
    # to conform to protocol v3 norms.
    if settingsversion == 9:
        for addressInKeysFile in BMConfigParser().addresses():
            try:
                previousTotalDifficulty = float(
                    BMConfigParser().getint(
                        addressInKeysFile, 'noncetrialsperbyte')) / 320
                previousSmallMessageDifficulty = float(
                    BMConfigParser().getint(
                        addressInKeysFile, 'payloadlengthextrabytes')) / 14000
                if previousTotalDifficulty <= 2:
                    previousTotalDifficulty = 1
                if previousSmallMessageDifficulty < 1:
                    previousSmallMessageDifficulty = 1
                BMConfigParser().set(
                    addressInKeysFile, 'noncetrialsperbyte',
                    str(int(previousTotalDifficulty * 1000)))
                BMConfigParser().set(
                    addressInKeysFile, 'payloadlengthextrabytes',
                    str(int(previousSmallMessageDifficulty * 1000)))
            except Exception:
                continue
        BMConfigParser().set('bitmessagesettings', 'maxdownloadrate', '0')
        BMConfigParser().set('bitmessagesettings', 'maxuploadrate', '0')
        settingsversion = 10

    # sanity check
    if BMConfigParser().safeGetInt(
            'bitmessagesettings', 'maxacceptablenoncetrialsperbyte') == 0:
        BMConfigParser().set(
            'bitmessagesettings', 'maxacceptablenoncetrialsperbyte',
            str(
                defaults.ridiculousDifficulty
                * defaults.networkDefaultProofOfWorkNonceTrialsPerByte)
        )
    if BMConfigParser().safeGetInt(
        'bitmessagesettings', 'maxacceptablepayloadlengthextrabytes'
    ) == 0:
        BMConfigParser().set(
            'bitmessagesettings', 'maxacceptablepayloadlengthextrabytes',
            str(
                defaults.ridiculousDifficulty
                * defaults.networkDefaultPayloadLengthExtraBytes)
        )

    if not BMConfigParser().has_option('bitmessagesettings', 'onionhostname'):
        BMConfigParser().set('bitmessagesettings', 'onionhostname', '')
    if not BMConfigParser().has_option('bitmessagesettings', 'onionport'):
        BMConfigParser().set('bitmessagesettings', 'onionport', '8444')
    if not BMConfigParser().has_option('bitmessagesettings', 'onionbindip'):
        BMConfigParser().set('bitmessagesettings', 'onionbindip', '127.0.0.1')
    if not BMConfigParser().has_option('bitmessagesettings', 'smtpdeliver'):
        BMConfigParser().set('bitmessagesettings', 'smtpdeliver', '')
    if not BMConfigParser().has_option(
            'bitmessagesettings', 'hidetrayconnectionnotifications'):
        BMConfigParser().set(
            'bitmessagesettings', 'hidetrayconnectionnotifications', 'false')
    if BMConfigParser().safeGetInt(
            'bitmessagesettings', 'maxoutboundconnections') < 1:
        BMConfigParser().set(
            'bitmessagesettings', 'maxoutboundconnections', '8')
        print('WARNING: your maximum outbound connections must be a number.')

    # TTL is now user-specifiable. Let's add an option to save
    # whatever the user selects.
    if not BMConfigParser().has_option('bitmessagesettings', 'ttl'):
        BMConfigParser().set('bitmessagesettings', 'ttl', '367200')

    BMConfigParser().set(
        'bitmessagesettings', 'settingsversion', str(settingsversion))
    BMConfigParser().save()


def isOurOperatingSystemLimitedToHavingVeryFewHalfOpenConnections():
    try:
        if sys.platform[0:3] == "win":
            VER_THIS = StrictVersion(platform.version())
            return (
                StrictVersion("5.1.2600") <= VER_THIS and
                StrictVersion("6.0.6000") >= VER_THIS
            )
        return False
    except Exception:
        pass
