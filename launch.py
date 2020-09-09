from emoji import emojize

rocket = emojize(":rocket:", use_aliases=True)

class Launch():
    def __init__(self, mission_name, provider, vehicle, padname, padloc, description, launch_date, livestream):
        self.gmpas_baseurl = "https://www.google.com/maps/search/?api=1&query="
        self.mission_name = mission_name
        self.provider = provider
        self.vehicle = vehicle
        self.padname = padname
        self.padloc = padloc
        self.description = description
        #self.livestream = livestream
        
        self.date = "TBD"
        print("Date parameter: " + launch_date + '\n')
        if launch_date != "None":
            if launch_date[-1:] == 'Z':
                parts = launch_date.split('T')
                day = parts[0].split('-')
                print('Parts: ' + str(len(parts)) + '\nDay: ' + str(len(day)))
                self.date = day[1] + '-' + day[2] + '-' + day[0] + ' ' + parts[1][0:-1] + '(UTC)'
            else:
                self.date = launch_date

        self.text = self.createDisplayText()
        if self.description == "nodescforlist":
            self.text = self.createListText()

    def createDisplayText(self):
        print(self.date)
        gmaps_querykey = self.padname.replace(' ', '+')
        text = '<b>Mission:</b> ' + self.mission_name + '\n' \
                '<b>Provider:</b> ' + self.provider + '\n' \
                '<b>Vehicle:</b> ' + self.vehicle + '\n' \
                '<b>Launching from</b> <a href="' + self.gmpas_baseurl + gmaps_querykey + '">' + self.padname + ' (' + self.padloc + ')</a>\n' \
                '<b>Date:</b> <i>' + self.date + '</i>\n\n' \
        
        if self.description != "nodescforlist":
            text = text + '' + self.description
        
        #if self.livestream != "":
            #text = text + '\n<b>Follow the <a href="' + self.livestream + '">Livestream</a> <i>(if available)</i></b>'

        return text

    def createListText(self):
        print(self.date)
        #gmaps_querykey = self.padname.replace(' ', '+')
        text = '<b>Provider:</b> ' + self.provider + '\n' \
                '<b>Vehicle:</b> ' + self.vehicle + '\n' \
                '<b>Date:</b> <i>' + self.date + '</i>\n\n' \
        
        return text
    
    def getFormattedText(self):
        return self.text