import swisseph as swe
from datetime import datetime, timedelta
import pytz

IST = pytz.timezone("Asia/Kolkata")


class EkadashiCalculator:

    def __init__(self):
        self.tz = IST

    # --------------------------------------------------
    # Core tithi calculation
    # --------------------------------------------------

    def get_tithi(self, dt):

        utc = dt.astimezone(pytz.UTC)

        jd = swe.julday(
            utc.year,
            utc.month,
            utc.day,
            utc.hour + utc.minute / 60 + utc.second / 3600,
        )

        sun = swe.calc_ut(jd, swe.SUN)[0][0]
        moon = swe.calc_ut(jd, swe.MOON)[0][0]

        angle = (moon - sun) % 360

        return int(angle / 12) + 1

    # --------------------------------------------------
    # Sunrise approximation (6 AM IST)
    # --------------------------------------------------

    def sunrise(self, date):

        return self.tz.localize(
            datetime(date.year, date.month, date.day, 6, 0, 0)
        )

    # --------------------------------------------------
    # Find intervals where tithi == 11 or 26
    # --------------------------------------------------

    def find_ekadashi_intervals(self, year):

        start = self.tz.localize(datetime(year, 1, 1))
        end = self.tz.localize(datetime(year, 12, 31, 23, 59))

        current = start

        prev_tithi = self.get_tithi(current)

        intervals = []

        while current < end:

            current += timedelta(hours=1)

            tithi = self.get_tithi(current)

            # detect start of ekadashi tithi
            if (tithi in [11, 26]) and (prev_tithi not in [11, 26]):

                start_time = current
                current_tithi = tithi

                # find when it ends
                search = current

                while self.get_tithi(search) == current_tithi:
                    search += timedelta(minutes=30)

                end_time = search

                intervals.append((start_time, end_time, current_tithi))

                current = end_time

            prev_tithi = tithi

        return intervals

    # --------------------------------------------------
    # Convert intervals to observance dates
    # --------------------------------------------------

    def get_ekadashi_dates(self, year):

        intervals = self.find_ekadashi_intervals(year)

        results = []

        for start, end, tithi in intervals:

            d1 = start.date()
            d2 = (start + timedelta(days=1)).date()

            sunrise1 = self.sunrise(start)
            sunrise2 = self.sunrise(start + timedelta(days=1))

            t1 = self.get_tithi(sunrise1)
            t2 = self.get_tithi(sunrise2)

            if t1 == tithi:
                obs = d1
            elif t2 == tithi:
                obs = d2
            else:
                obs = d1

            paksha = "Shukla" if tithi == 11 else "Krishna"

            results.append(
                {
                    "date": obs,
                    "paksha": paksha
                }
            )

        return results

    # --------------------------------------------------
    # Helper functions for API
    # --------------------------------------------------

    def is_ekadashi(self, date):

        if isinstance(date, datetime):
            date = date.date()

        year = date.year

        ek = self.get_ekadashi_dates(year)

        return any(x["date"] == date for x in ek)

    def next_ekadashi(self):

        today = datetime.now(self.tz).date()

        for i in range(60):

            check = today + timedelta(days=i)

            year = check.year

            ek = self.get_ekadashi_dates(year)

            for e in ek:

                if e["date"] >= check:

                    return {
                        "date": e["date"],
                        "paksha": e["paksha"],
                        "days_until": (e["date"] - today).days
                    }

        return None


# -------------------------------------------
# Global instance for FastAPI
# -------------------------------------------

calculator = EkadashiCalculator()


def is_ekadashi(date):
    return calculator.is_ekadashi(date)


def get_ekadashi_dates(year):
    return calculator.get_ekadashi_dates(year)


def next_ekadashi():
    return calculator.next_ekadashi()