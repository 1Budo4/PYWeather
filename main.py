import requests
import json
import tkinter
import customtkinter as ctk
from urllib.request import urlopen
from PIL import ImageTk

place = "Borovo"
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class Weather:
    #gets all data from api, stores it in variable
    def requestdata(self, place):
        self.LINK = "https://api.openweathermap.org/data/2.5/weather?q=" + place + "&appid=bc571c0c6329a25ccc4bff3b4c07d71d&units=metric"
        print(place)
        try:
            response = requests.get(self.LINK)
            self.data = json.loads(response.text)
            self.maindesc = self.data['weather'][0]['description']
            self.temp = self.data['main']['temp']
            self.feel = self.data['main']['feels_like']
            self.temp_min = self.data['main']['temp_min']
            self.temp_max = self.data['main']['temp_max']
            self.press = self.data['main']['pressure']
            self.country = self.data['sys']['country']
            self.name = self.data['name']
            image_url = "https://openweathermap.org/img/wn/" + self.data["weather"][0]["icon"] +"@4x.png"
            self.image_data = urlopen(image_url)
            app.secondframe()
        except:
            print("Fetching Data From API FAILED!")
            print(response.status_code)

    def __getmaindesc__(self):
        return self.maindesc

    def __gettemp__(self):
        return self.temp

    def __getfeel__(self):
        return self.feel

    def __gettempmin__(self):
        return self.temp_min

    def __gettempmax__(self):
        return self.temp_max

    def __getpress__(self):
        return self.press

    def __getcountry__(self):
        return self.country
    
    def __getname__(self):
        return self.name

    #getter for image
    def __getimage__(self):
        return self.image_data

    #getter for all data
    def __getdata__(self):
        return(self.data)

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Weather")
        self.geometry("400x550")

        global weather
        weather = Weather()
        
        self.cf = CityFrame(self, width=200, height=200, corner_radius=10)
        self.cf.place(relx=0.25, rely=0.25)
        
    def secondframe(self):
        self.cf.forget()

        self.mf = MainFrame(self, width=350, height=460, corner_radius=10)
        
        self.mf.loadtitle(weather.__getname__(), weather.__getcountry__())

        self.mf.loadimage(weather.__getimage__())

        self.mf.loaddesc(weather.__getmaindesc__())

        temp = round(weather.__gettemp__())
        temp = str(temp) + '°C'
        self.mf.loadtemp(temp)

        feel = round(weather.__getfeel__())
        feel = str(feel) + '°C'
        self.mf.loadfeel(feel)

        mintemp = round(weather.__gettempmin__())
        mintemp = str(mintemp) + '°C'
        self.mf.loadtempmin(mintemp)

        maxtemp = round(weather.__gettempmax__())
        maxtemp = str(maxtemp) + '°C'
        self.mf.loadtempmax(maxtemp)

        pressure = str(weather.__getpress__()) + ' bar'
        self.mf.loadpressure(pressure)

        self.mf.place(relx=0.06, rely=0.08)
    

class CityFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pack_propagate(False)

        self.title = ctk.CTkLabel(self, text="Enter a Place", font=('Arial', 25))
        self.title.pack(pady=20)

        self.city = tkinter.StringVar()
        self.search = ctk.CTkEntry(self, textvariable=self.city)
        self.search.pack(pady=10)
    
        self.searchbtn = ctk.CTkButton(self, text="Search", command=self.requestdatafromglobal)
        self.searchbtn.pack()

    def requestdatafromglobal(self):
        weather.requestdata(self.search.get())

class MainFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pack_propagate(False)

        self.placeTitle = ctk.CTkLabel(self, text="Borovo, HR", font=('Arial', 25, 'bold'), text_color="white")
        self.placeTitle.pack(pady=(30, 15))

        self.weather_image = ctk.CTkLabel(self, text='')
        self.weather_image.pack()

        self.desc = ctk.CTkLabel(self, font=('Arial', 20, 'bold'))
        self.desc.pack()

        self.temp = ctk.CTkLabel(self, font=('Arial', 20, 'bold'))
        self.temp.pack()

        self.feel = ctk.CTkLabel(self, font=('Arial', 15), text='Feel: ')
        self.feel.place(x=130, y=340)
        self.feelvalue = ctk.CTkLabel(self, font=('Arial', 15, 'bold'))
        self.feelvalue.place(x=185, y=340)

        self.temp_min = ctk.CTkLabel(self, font=('Arial', 15), text='Min. temp.: ')
        self.temp_min.place(x=91, y=365)
        self.temp_min_value = ctk.CTkLabel(self, font=('Arial', 15, 'bold'))
        self.temp_min_value.place(x=185, y=365)

        self.temp_max = ctk.CTkLabel(self, font=('Arial', 15), text='Max. temp.: ')
        self.temp_max.place(x=87, y=390)
        self.temp_max_value = ctk.CTkLabel(self, font=('Arial', 15, 'bold'))
        self.temp_max_value.place(x=185, y=390)

        self.pressure = ctk.CTkLabel(self, font=('Arial', 15), text='Pressure: ')
        self.pressure.place(x=98, y=415)
        self.pressurevalue = ctk.CTkLabel(self, font=('Arial', 15, 'bold'))
        self.pressurevalue.place(x=185, y=415)

    def loadtitle(self, name, country):
        self.placeTitle.configure(text=(name + ', ' + country)) 

    def loadimage(self, image_data):
        self.weather_image.configure(image=ImageTk.PhotoImage(data=image_data.read()))

    def loaddesc(self, desc):
        self.desc.configure(text=desc.capitalize())

    def loadtemp(self, temp):
        self.temp.configure(text=temp)

    def loadfeel(self, feel):
        self.feelvalue.configure(text=feel)

    def loadtempmin(self, mintemp):
        self.temp_min_value.configure(text=mintemp)
    
    def loadtempmax(self, maxtemp):
        self.temp_max_value.configure(text=maxtemp)

    def loadpressure(self, pressure):
        self.pressurevalue.configure(text=pressure)

def main():
     global app
     app = App()
     app.resizable(False, False)
     app.mainloop()

if __name__ == "__main__":
   main()