import tkinter as tk
from tkinter import messagebox
import requests

def read_api_key(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError("API key file not found.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the API key: {e}")

API_KEY_FILE = 'api.txt'
GEOLOCATION_API_URL = 'http://ipinfo.io/json'

try:
    API_KEY = read_api_key(API_KEY_FILE)
except Exception as e:
    print(e)
    exit(1)

def fetch_weather_data(location):
    url = f"https://api.weatherbit.io/v2.0/current"
    params = {
        'city': location,
        'key': API_KEY,
        'units': 'I'  # 'I' = Fahrenheit | 'M' = Celsius
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_current_location():
    try:
        response = requests.get(GEOLOCATION_API_URL)
        response.raise_for_status()
        data = response.json()
        return data.get('city', 'Unknown')
    except Exception as e:
        print(f"An error occurred while fetching the location: {e}")
        return 'Unknown'

def display_weather():
    location = get_current_location()
    if location:
        weather_data = fetch_weather_data(location)
        if weather_data and 'data' in weather_data:
            data = weather_data['data'][0]
            description = data['weather']['description']
            temp = data['temp']
            humidity = data['rh']
            message = (f"Weather in {location}:\n"
                       f"Description: {description}\n"
                       f"Temperature: {temp}°F\n"
                       f"Humidity: {humidity}%")
        else:
            message = "Failed to retrieve weather data."
        
        messagebox.showinfo("Weather Information", message)
    else:
        messagebox.showwarning("Location Error", "Failed to determine location.")

def main():
    root = tk.Tk()
    root.title("ClearCast")
    root.geometry("500x500")
    root.configure(bg='#87CEEB')

    frame = tk.Frame(root, bg='white', padx=20, pady=20, relief=tk.RAISED, borderwidth=2)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    title = tk.Label(frame, text="ClearCast Dashboard", font=('Helvetica', 24, 'bold'), bg='white', fg='#333')
    title.pack(pady=20)

    button = tk.Button(frame, text="Get Weather", command=display_weather, font=('Helvetica', 16), bg='#007BFF', fg='white', relief=tk.RAISED, width=15, height=2)
    button.pack(pady=20)

    root.iconbitmap('ClearCast.ico')

    root.mainloop()

if __name__ == "__main__":
    main()