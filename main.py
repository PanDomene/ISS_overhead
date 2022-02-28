import requests
from datetime import datetime
import smtplib
import time
import passw as pw

MY_LAT = 20.670349
MY_LONG = -103.374870
EMAIL = pw.email
PW = pw.password
EMAIL2 = pw.recipient

delta = 10

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

while True:
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if abs(iss_latitude-MY_LAT) < delta and abs(iss_longitude - MY_LONG) < delta:
        if not (sunrise < time_now < sunset):
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=EMAIL, password=PW)
                connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL2,
                                    msg="Subject:ISS Station\n\nLook up")

    time.sleep(60)
