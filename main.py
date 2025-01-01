#  Importing Modules
import sys
import requests
#Imports several classes from PyQt5
from PyQt5.QtWidgets import (QApplication , QWidget, QLabel, 
                            QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

#Class Weather App
class WeatherApp(QWidget):
    # Create the user interface(UI) elements
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter your city name : ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather ⛅" , self)
        self.temputature_label = QLabel(self)
        self.emoji_label = QLabel( self)
        self.description_label = QLabel(self)
        self.initUI()

    # Set up the user interface
    def initUI(self):

        self.setWindowTitle("Weather App")
        # Create a vertical layout to organize widgets
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temputature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)
        # Align UI elements to the center
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temputature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        # Set object names (id) for styling
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temputature_label.setObjectName("temputature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        # Apply the stylesheet for styling the application
        self.setStyleSheet("""
            QLabel, QPushButton{
                        font-family: calibri;
                        color :white;                      
                       }
            QWidget{
                         background-color: rgb(95, 188, 255);  
                    }
            QLabel#city_label{
                           font-size: 40px;
                           font-style : italic;
                           padding: 20px;
                           }

            QLineEdit#city_input{
                           padding: 10px;
                           font-size:40px;
                           background-color: rgb(44, 148, 222);
                           margin:0 20px;
                           border: none;
                           }

            QPushButton#get_weather_button{
                           margin:20px;
                           padding: 5px;
                           border: none;
                           border : 2px solid black;
                           font-size : 30px;
                           font-weight : bold;
                           }
            QPushButton#get_weather_button:hover{
                           background-color: black;
                           }

            QLabel#temputature_label{
                           font-size: 75px
                           }

            QLabel#emoji_label{
                           font-size: 100px;
                           font-family: segoe UI emoji;
                           }

            QLabel#description_label{
                           font-size: 50px;
                           padding: 20px;
                           }
                    

        """)
        # Connect the button click event to the get_weather function
        self.get_weather_button.clicked.connect(self.get_weather)


    #  weather data using the OpenWeather API
    def get_weather(self):
        # Replace with your API key
        api_key = "1b5d057ef71d2fa7be39903dd6b3d9c2" 
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        # control specific HTTP errors
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code :
                case 400:
                    self.display_error("Bad requst: \nPlease check your input!")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key!")
                case 403:
                    self.display_error("Forbidden \nAccess is denied!")
                case 404:
                    self.display_error("Not found: \nCity not found!")
                case 500:
                    self.display_error("Internal Server Error: \nplease try again later!")
                case 501:
                    self.display_error("Bad Gateway: \nInvald response from the server!")
                case 503:
                    self.display_error("Service Unavailable: \nServer is down!")
                case 504:
                    self.display_error("Gateway Timeout: \nNo response from the server!")
                case _:
                    self.display_error(f"HTTP error occured: \n {http_error}")

        except requests.exceptions.ConnectionError:
            print("Connection Error: \nChick your internet connection")
        except requests.exceptions.Timeout:
            print("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            print("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error :
            print(f"Request Error:\n{req_error}")

    # Display error messages on the temperature label
    def display_error(self, message):
        self.temputature_label.setStyleSheet("font-size:30px;")
        self.temputature_label.setText(message)
        self.description_label.clear()
        self.emoji_label.clear()

    # Display weather data in the UI
    def display_weather(self, data):
        self.temputature_label.setStyleSheet("font-size:75px;")
        # Convert temperature from Kelvin to Celsius and Fahrenheit
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5)-459.67
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]
        # Update UI elements with weather data
        self.temputature_label.setText(f"{temperature_c:.0f}℃")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    # Return emoji based on weather condition ID
    @staticmethod
    def get_weather_emoji(weather_id):
        if weather_id >= 200 and weather_id <=232:
            return "⛈"
        elif weather_id >=300 and weather_id <=321:
            return "🌦"
        elif weather_id >=500 and weather_id <=531:
            return "🌧"
        elif weather_id >=600 and weather_id <=622:
            return "❄"
        elif weather_id >=701 and weather_id <=741:
            return "🌫"
        elif weather_id ==762:
            return "🌋"
        elif weather_id ==771:
            return "☄"
        elif weather_id ==781:
            return "🌪"
        elif weather_id ==800:
            return "☀"
        elif weather_id>=801 and weather_id <=804:
            return "☁"
        else:
            return ""

        

        

# Create and run the PyQt application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())