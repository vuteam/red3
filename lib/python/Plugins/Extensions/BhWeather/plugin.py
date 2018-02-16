from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.InputBox import InputBox
from Plugins.Plugin import PluginDescriptor
from Components.ActionMap import ActionMap
from Components.Sources.List import List
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.config import config
from Tools.Directories import fileExists
from Tools.LoadPixmap import LoadPixmap
from Blackhole.BhUtils import BhU_check_proc_version
from urllib import quote
from urllib2 import Request, urlopen, URLError, HTTPError
from xml.etree.cElementTree import fromstring
from xml.dom import minidom, Node
from enigma import eTimer
import codecs

class BhMeteoMain(Screen):
    skin = '\n\t<screen position="center,center" size="1280,720" title="Black Hole Weather" flags="wfNoBorder">\n\t\t\n\t\t<ePixmap position="0,0" size="1280,720" pixmap="/usr/share/icons/blackhole/weather/100.png" />\n\t\t<widget source="global.CurrentTime" render="Label" position="1180,5" size="80,22" zPosition="1" font="Regular;16" valign="top" halign="left" foregroundColor="white" backgroundColor="transpBlack" transparent="1">\n\t\t\t<convert type="ClockToText">Default</convert>\n\t\t</widget>\n\t\t<widget name="lab1" position="150,100" halign="right" size="220,20" zPosition="1" font="Regular;16" foregroundColor="#dcdcdc" backgroundColor="transpBlack" valign="top"  transparent="1" />\n\t\t<widget name="lab1b" position="373,100" halign="left" size="210,20" zPosition="1" font="Regular;16" foregroundColor="#ffa500" backgroundColor="transpBlack" valign="top"  transparent="1" />\n\t\t<widget name="lab2" position="140,120" halign="center" size="440,26" zPosition="1" font="Regular;24" valign="top" foregroundColor="white" backgroundColor="transpBlack" transparent="1" />\n\t\t<widget name="lab3" position="140,146" halign="center" size="440,20" zPosition="1" font="Regular;18" valign="top" foregroundColor="#8F8F8F" backgroundColor="transpBlack" transparent="1" />\n\t\t<widget name="lab4" position="140,220" halign="right" size="180,80" zPosition="1" font="Regular;80" foregroundColor="white" backgroundColor="transpBlack" valign="top"  transparent="1" />\n\t\t<widget name="lab4b" position="310,220" halign="right" size="40,30" zPosition="1" font="Regular;24" foregroundColor="white" backgroundColor="transpBlack" valign="top"  transparent="1" />\n\t\t<widget name="lab5" position="350,200" size="250,180" zPosition="1" transparent="1" alphatest="blend" />\n\t\t<widget name="lab6" position="150,350" halign="center" size="440,30" zPosition="1" font="Regular;23" valign="top" foregroundColor="white" backgroundColor="transpBlack" transparent="1" />\n\t\t<widget name="lab7" position="140,420" halign="right" size="150,24" zPosition="1" font="Regular;19" valign="top" foregroundColor="#8F8F8F" backgroundColor="transpBlack" transparent="1" />\n\t\t<widget name="lab7b" position="305,420" halign="left" size="280,24" zPosition="1" font="Regular;19" foregroundColor="white" backgroundColor="transpBlack" valign="top" transparent="1" />\n\t\t<widget name="lab8" position="140,450" halign="right" size="150,24" zPosition="1" font="Regular;19" valign="top" foregroundColor="#8F8F8F" backgroundColor="transpBlack" transparent="1" />\n\t\t<widget name="lab8b" position="305,450" halign="left" size="285,24" zPosition="1" font="Regular;19" foregroundColor="white" backgroundColor="transpBlack" valign="top" transparent="1" />\n\t\t<widget name="lab9" position="140,480" halign="right" size="150,24" zPosition="1" font="Regular;19" valign="top" foregroundColor="#8F8F8F" backgroundColor="transpBlack" transparent="1" />\n\t\t<widget name="lab9b" position="305,480" halign="left" size="285,24" zPosition="1" font="Regular;19" foregroundColor="white" backgroundColor="transpBlack" valign="top" transparent="1" />\n\t\t<widget name="lab10" position="140,510" halign="right" size="150,24" zPosition="1" font="Regular;19" valign="top" foregroundColor="#8F8F8F" backgroundColor="transpBlack" transparent="1" />\n\t\t<widget name="lab10b" position="305,510" halign="left" size="285,24" zPosition="1" font="Regular;19" foregroundColor="white" backgroundColor="transpBlack" valign="top" transparent="1" />\n\t\t<widget name="lab11" position="140,540" halign="right" size="150,24" zPosition="1" font="Regular;19" valign="top" foregroundColor="#8F8F8F" backgroundColor="transpBlack" transparent="1" />\n\t\t<widget name="lab11b" position="305,540" halign="left" size="285,24" zPosition="1" font="Regular;19" foregroundColor="white" backgroundColor="transpBlack" valign="top" transparent="1" />\n\t\t<widget name="lab12" position="140,570" halign="right" size="150,24" zPosition="1" font="Regular;19" valign="top" foregroundColor="#8F8F8F" backgroundColor="transpBlack" transparent="1" />\n\t\t<widget name="lab12b" position="305,570" halign="left" size="285,24" zPosition="1" font="Regular;19" foregroundColor="white" backgroundColor="transpBlack" valign="top" transparent="1" />\n\t\t<widget name="lab13" position="700,120" halign="center" size="430,26" zPosition="1" font="Regular;24" valign="top" foregroundColor="white" backgroundColor="transpBlack" transparent="1"  />\n\t\t<widget name="lab14" position="730,170" halign="left" size="65,24" zPosition="1" font="Regular;19" valign="top" foregroundColor="#8F8F8F" backgroundColor="transpBlack" transparent="1" />\n\t\t<widget name="lab14b" position="795,170" halign="left" size="90,24" zPosition="1" font="Regular;19" foregroundColor="white" backgroundColor="transpBlack" valign="top" transparent="1" />\n\t\t<widget name="lab15" position="895,170" halign="left" size="60,24" zPosition="1" font="Regular;19" valign="top" foregroundColor="#8F8F8F" backgroundColor="transpBlack" transparent="1" />\n\t\t<widget name="lab15b" position="955,170" halign="left" size="60,24" zPosition="1" font="Regular;19" foregroundColor="white" backgroundColor="transpBlack" valign="top" transparent="1" />\n\t\t<widget name="lab16" position="730,200" halign="left" size="220,26" zPosition="1" font="Regular;22" valign="top" foregroundColor="white" backgroundColor="transpBlack" transparent="1"  />\n\t\t<widget name="lab17" position="1010,150" size="100,100" zPosition="1" alphatest="blend" />\n\t\t<widget name="lab18" position="700,300" halign="center" size="430,26" zPosition="1" font="Regular;24" valign="top" foregroundColor="white" backgroundColor="transpBlack" transparent="1"  />\n\t\t<widget name="lab19" position="730,350" halign="left" size="65,24" zPosition="1" font="Regular;19" valign="top" foregroundColor="#8F8F8F" backgroundColor="transpBlack" transparent="1" />\n\t\t<widget name="lab19b" position="795,350" halign="left" size="90,24" zPosition="1" font="Regular;19" foregroundColor="white" backgroundColor="transpBlack" valign="top" transparent="1" />\n\t\t<widget name="lab20" position="895,350" halign="left" size="60,24" zPosition="1" font="Regular;19" valign="top" foregroundColor="#8F8F8F" backgroundColor="transpBlack" transparent="1" />\n\t\t<widget name="lab20b" position="955,350" halign="left" size="60,24" zPosition="1" font="Regular;19" foregroundColor="white" backgroundColor="transpBlack" valign="top" transparent="1" />\n\t\t<widget name="lab21" position="730,380" halign="left" size="220,26" zPosition="1" font="Regular;22" valign="top" foregroundColor="white" backgroundColor="transpBlack" transparent="1"  />\n\t\t<widget name="lab22" position="1010,320" size="100,100" zPosition="1" alphatest="blend" />\n\t\t<widget name="lab23" position="700,470" halign="center" size="430,26" zPosition="1" font="Regular;24" valign="top" foregroundColor="white" backgroundColor="transpBlack" transparent="1" />\n\t\t<widget name="lab24" position="730,510" halign="right" size="110,22" zPosition="1" font="Regular;18" valign="top" foregroundColor="#8F8F8F" backgroundColor="transpBlack" transparent="1" />\n\t\t<widget name="lab24b" position="850,510" halign="left" size="100,22" zPosition="1" font="Regular;18" foregroundColor="white" backgroundColor="transpBlack" valign="top" transparent="1" />\n\t\t<widget name="lab25" position="930,510" halign="left" size="100,22" zPosition="1" font="Regular;18" valign="top" foregroundColor="#8F8F8F" backgroundColor="transpBlack" transparent="1" />\n\t\t<widget name="lab25b" position="1040,510" halign="left" size="115,22" zPosition="1" font="Regular;18" foregroundColor="white" backgroundColor="transpBlack" valign="top" transparent="1" />\n\t\t<widget name="lab26" position="730,535" halign="right" size="110,22" zPosition="1" font="Regular;18" valign="top" foregroundColor="#8F8F8F" backgroundColor="transpBlack" transparent="1" />\n\t\t<widget name="lab26b" position="850,535" halign="left" size="330,22" zPosition="1" font="Regular;18" foregroundColor="white" backgroundColor="transpBlack" valign="top" transparent="1" />\n\t\t<widget name="lab27" position="730,560" halign="right" size="110,22" zPosition="1" font="Regular;18" valign="top" foregroundColor="#8F8F8F" backgroundColor="transpBlack" transparent="1" />\n\t\t<widget name="lab27b" position="850,560" halign="left" size="330,22" zPosition="1" font="Regular;18" foregroundColor="white" backgroundColor="transpBlack" valign="top" transparent="1" />\n\t\t<widget name="lab28" position="790,595" size="16,16" zPosition="1" alphatest="blend" />\n\t\t<widget name="lab28a" position="800,590" halign="right" size="20,20" zPosition="1" font="Regular;18" valign="top" foregroundColor="#8F8F8F" backgroundColor="transpBlack" transparent="1" />\n\t\t<widget name="lab28b" position="830,590" halign="left" size="330,22" zPosition="1" font="Regular;18" foregroundColor="white" backgroundColor="transpBlack" valign="top" transparent="1" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label(_('Retrieving data ...'))
        self['lab1b'] = Label('')
        self['lab2'] = Label('')
        self['lab3'] = Label('')
        self['lab4'] = Label('')
        self['lab4b'] = Label('')
        self['lab5'] = Pixmap()
        self['lab6'] = Label('')
        self['lab7'] = Label('')
        self['lab7b'] = Label('')
        self['lab8'] = Label('')
        self['lab8b'] = Label('')
        self['lab9'] = Label('')
        self['lab9b'] = Label('')
        self['lab10'] = Label('')
        self['lab10b'] = Label('')
        self['lab11'] = Label('')
        self['lab11b'] = Label('')
        self['lab12'] = Label('')
        self['lab12b'] = Label('')
        self['lab13'] = Label('')
        self['lab14'] = Label('')
        self['lab14b'] = Label('')
        self['lab15'] = Label('')
        self['lab15b'] = Label('')
        self['lab16'] = Label('')
        self['lab17'] = Pixmap()
        self['lab18'] = Label('')
        self['lab19'] = Label('')
        self['lab19b'] = Label('')
        self['lab20'] = Label('')
        self['lab20b'] = Label('')
        self['lab21'] = Label('')
        self['lab22'] = Pixmap()
        self['lab23'] = Label('')
        self['lab24'] = Label('')
        self['lab24b'] = Label('')
        self['lab25'] = Label('')
        self['lab25b'] = Label('')
        self['lab26'] = Label('')
        self['lab26b'] = Label('')
        self['lab27'] = Label('')
        self['lab27b'] = Label('')
        self['lab28'] = Pixmap()
        self['lab28a'] = Label('')
        self['lab28b'] = Label('')
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'red': self.key_red,
         'green': self.key_green,
         'back': self.close,
         'ok': self.close})
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.startConnection)
        self.onShow.append(self.startShow)
        self.onClose.append(self.delTimer)
        self.bhv = 0

    def startShow(self):
        if BhU_check_proc_version():
            self.bhv += 1
        if fileExists('/usr/bin/blackholesocker'):
            self.bhv += 2
        self.activityTimer.start(10)

    def startConnection(self):
        self.activityTimer.stop()
        self.updateInfo()

    def updateInfo(self):
        myurl = self.get_Url()
        req = Request(myurl)
        try:
            handler = urlopen(req)
        except HTTPError as e:
            maintext = 'Error: connection failed !'
        except URLError as e:
            maintext = 'Error: Page not available !'
        else:
            page = handler.read()
            handler.close()
            if page.find('forecast') > 1:
                page = page.replace('\n', '')
                page = page.replace('\xc2\x86', '').replace('\xc2\x87', '').decode('utf-8', 'ignore').encode('utf-8') or ''
                page = codecs.decode(page, 'UTF-8')
                dom = minidom.parseString(page)
                Week = []
                for curr in dom.getElementsByTagName('forecast'):
                    High = curr.getAttribute('high')
                    Low = curr.getAttribute('low')
                    Day = curr.getAttribute('day')
                    Icon = curr.getAttribute('skycodeday') + '.png'
                    Cond = curr.getAttribute('skytextday')
                    Regen = curr.getAttribute('precip')
                    Week.append({'High': High,
                     'Low': Low,
                     'Day': Day,
                     'Icon': Icon,
                     'Cond': Cond,
                     'Regen': Regen})

                Today = {}
                curr = dom.getElementsByTagName('weather')
                if len(curr) != 0:
                    Today['Locname'] = curr[0].getAttribute('weatherlocationname')
                    Today['provider'] = curr[0].getAttribute('provider')
                    Today['Latitude'] = curr[0].getAttribute('lat')
                    Today['Longitude'] = curr[0].getAttribute('long')
                    Today['Timezone'] = curr[0].getAttribute('timezone')
                curr = dom.getElementsByTagName('current')
                if len(curr) != 0:
                    Today['Temp_c'] = curr[0].getAttribute('temperature') + '\xc2\xb0'
                    Today['Hum'] = curr[0].getAttribute('humidity') + '%'
                    Today['Wind'] = curr[0].getAttribute('winddisplay')
                    Today['Winds'] = curr[0].getAttribute('windspeed')
                    Today['Cond'] = curr[0].getAttribute('skytext')
                    Today['Icon'] = curr[0].getAttribute('skycode') + '.png'
                    Today['Feel'] = curr[0].getAttribute('feelslike')
                    Today['Wtime'] = curr[0].getAttribute('observationtime')
                    Today['Wpoint'] = curr[0].getAttribute('observationpoint')
                maintext = ''
                tmptext = ''
                maintext = _('Data provider: ')
                self['lab1b'].setText(str(Today['provider']))
                city = '%s' % str(Today['Locname'])
                self['lab2'].setText(city)
                txt = str(Today['Wtime'])
                parts = txt.strip().split(':')
                txt = _('Last Updated: %s:%s') % (parts[0], parts[1])
                self['lab3'].setText(txt)
                txt = str(Today['Temp_c'])
                self['lab4'].setText(txt)
                icon = '/usr/share/icons/blackhole/weather/%s' % str(Today['Icon'])
                myicon = self.checkIcon(icon)
                png = LoadPixmap(myicon)
                self['lab5'].instance.setPixmap(png)
                txt = str(Today['Cond'])
                self['lab6'].setText(txt)
                self['lab7'].setText(_('Humidity :'))
                txt = str(Today['Hum'])
                self['lab7b'].setText(txt)
                self['lab8'].setText(_('FeelsLike :'))
                txt = str(Today['Feel']) + '\xc2\xb0'
                self['lab8b'].setText(txt)
                self['lab9'].setText(_('Precip :'))
                txt = str(Week[0]['Regen'])
                self['lab9b'].setText(txt)
                self['lab10'].setText(_('Wind display :'))
                txt = str(Today['Wind'])
                self['lab10b'].setText(txt)
                self['lab11'].setText(_('Wind speed :'))
                txt = str(Today['Winds'])
                self['lab11b'].setText(txt)
                self['lab12'].setText(_('Ob. point :'))
                txt = str(Today['Wpoint'])
                self['lab12b'].setText(txt)
                txt = str(Week[1]['Day'])
                self['lab13'].setText(txt)
                self['lab14'].setText(_('High :'))
                txt = str(Week[1]['High']) + '\xc2\xb0'
                self['lab14b'].setText(txt)
                self['lab15'].setText(_('Low :'))
                txt = str(Week[1]['Low']) + '\xc2\xb0'
                self['lab15b'].setText(txt)
                txt = str(Week[1]['Cond'])
                self['lab16'].setText(txt)
                icon = '/usr/share/icons/blackhole/weather/small/%s' % str(Week[1]['Icon'])
                myicon = self.checkIcon(icon)
                png = LoadPixmap(myicon)
                self['lab17'].instance.setPixmap(png)
                txt = txt = str(Week[2]['Day'])
                self['lab18'].setText(txt)
                self['lab19'].setText(_('High :'))
                txt = str(Week[2]['High']) + '\xc2\xb0'
                self['lab19b'].setText(txt)
                self['lab20'].setText(_('Low :'))
                txt = str(Week[2]['Low']) + '\xc2\xb0'
                self['lab20b'].setText(txt)
                txt = str(Week[2]['Cond'])
                self['lab21'].setText(txt)
                icon = '/usr/share/icons/blackhole/weather/small/%s' % str(Week[2]['Icon'])
                myicon = self.checkIcon(icon)
                png = LoadPixmap(myicon)
                self['lab22'].instance.setPixmap(png)
                self['lab23'].setText(str(Today['Locname']))
                self['lab24'].setText(_('Latitude :'))
                txt = str(Today['Latitude'])
                self['lab24b'].setText(txt)
                self['lab26'].setText(_('Longitude :'))
                txt = str(Today['Longitude'])
                self['lab26b'].setText(txt)
                self['lab27'].setText(_('Timezone :'))
                txt = txt = str(Today['Timezone'])
                self['lab27b'].setText(txt)
                myicon = '/usr/share/icons/blackhole/weather/red.png'
                png = LoadPixmap(myicon)
                self['lab28'].instance.setPixmap(png)
                self['lab28a'].setText(':')
                self['lab28b'].setText(_('Change city'))
            else:
                maintext = 'Error getting XML document!'

        self['lab1'].setText(maintext)

    def checkIcon(self, localfile):
        if fileExists(localfile):
            pass
        else:
            url = localfile.replace('/usr/share/icons/blackhole', 'http://www.vuplus-community.net/bhaddons')
            handler = urlopen(url)
            if handler:
                content = handler.read()
                fileout = open(localfile, 'wb')
                fileout.write(content)
                handler.close()
                fileout.close()
        return localfile

    def get_Url(self):
        url = 'http://weather.service.msn.com/data.aspx?weadegreetype=C&culture=it-IT&wealocations=wc:ITXX0067'
        cfgfile = '/etc/bhwheater2.cfg'
        if fileExists(cfgfile):
            f = open(cfgfile, 'r')
            line = f.readline()
            url = line.strip()
            f.close()
        if url.find('src=outlook') == -1:
            url = url + '&src=outlook'
        return url

    def delTimer(self):
        del self.activityTimer

    def key_green(self):
        txt = 'Black Hole Weather v 0.2\n\nAuthor: meo\nWeather data: msn\nGraphics idea by: XBMC'
        box = self.session.open(MessageBox, txt, MessageBox.TYPE_INFO)
        box.setTitle(_('About'))

    def key_red(self):
        msg = _('Enter the city name:')
        self.session.openWithCallback(self.goSelect, InputBox, title=msg, windowTitle=_('Change city'), text='Roma')

    def goSelect(self, city):
        if city is not None:
            self.session.openWithCallback(self.updateInfo, BhMeteoSelectCity, city)


class BhMeteoSelectCity(Screen):
    skin = '\n\t<screen position="center,center" size="620,500" title="Select city">\n\t\t<widget source="list" render="Listbox" position="10,20" zPosition="1" size="580,430" scrollbarMode="showOnDemand" transparent="1" >\n\t\t\t<convert type="StringList" />\n\t\t</widget>\n\t\t<widget name="lab1" position="10,470" halign="center" size="580,30" zPosition="1" font="Regular;24" valign="top" transparent="1" />\n\t</screen>'

    def __init__(self, session, city):
        Screen.__init__(self, session)
        self.city = quote(city)
        self.flist = []
        self['list'] = List(self.flist)
        self['lab1'] = Label(_('Sorry no matches found'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'ok': self.saveCfg})
        self.onLayoutFinish.append(self.queryStart)

    def queryStart(self):
        self.lang = config.osd.language.value.replace('_', '-')
        if self.lang == 'en-EN':
            self.lang = 'en-US'
        url = 'http://weather.service.msn.com/find.aspx?outputview=search&weasearchstr=%s&culture=%s&src=outlook' % (quote(self.city), self.lang)
        try:
            file = urlopen(url)
        except:
            return

        html = file.read()
        file.close()
        if html.find('Unable to configure weather') != -1:
            self.lang = 'en-US'
            url = 'http://weather.service.msn.com/find.aspx?outputview=search&weasearchstr=%s&culture=%s&src=outlook' % (quote(self.city), self.lang)
            file = urlopen(url)
            html = file.read()
            file.close()
        root = fromstring(html)
        searchlocation = ''
        searchresult = ''
        weatherlocationcode = ''
        list = []
        for childs in root:
            if childs.tag == 'weather':
                searchresult = childs.attrib.get('weatherlocationname').encode('utf-8', 'ignore')
                woeid = childs.attrib.get('weatherlocationcode').encode('utf-8', 'ignore')
                res = (searchresult, woeid)
                self.flist.append(res)

        if len(self.flist) > 0:
            self['lab1'].setText(_('Press ok to confirm'))
        self['list'].list = self.flist

    def saveCfg(self):
        mysel = self['list'].getCurrent()
        if mysel:
            city = mysel[0]
            pin = mysel[1]
            url = 'http://weather.service.msn.com/data.aspx?weadegreetype=C&culture=%s&wealocations=%s\n' % (self.lang, pin)
            cfgfile = '/etc/bhwheater2.cfg'
            out = open(cfgfile, 'w')
            out.write(url)
            out.write('city=%s\n' % city)
            out.write('code=%s\n' % pin)
            out.write('lang=%s\n' % self.lang)
            out.close()
            self.close()


def main(session, **kwargs):
    session.open(BhMeteoMain)


def menu(menuid, **kwargs):
    if menuid == 'mainmenu':
        return [(_('Weather forecast'),
          main,
          'BlackHoleWeather',
          46)]
    return []


def Plugins(path, **kwargs):
    global pluginpath
    pluginpath = path
    return PluginDescriptor(name='BlackHoleWeather', description=_('World Weather Forecast'), where=PluginDescriptor.WHERE_MENU, fnc=menu)
