import swisseph as swe
from datetime import datetime, timedelta
import pytz

IST = pytz.timezone("Asia/Kolkata")


class EkadashiCalculator:
    """
    ISKCON / Vaishnava Ekadashi Calculator

    Rules:
    1. Dashami must end before Arunodaya (96 mins before sunrise)
    2. Ekadashi must be present at Arunodaya
    3. If Ekadashi on two consecutive days → observe second day
    """

    def __init__(self):
        self.tz = IST
        self.ARUNODAYA_MINUTES = 96

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

    def get_sunrise(self, date):

        return self.tz.localize(
            datetime(date.year, date.month, date.day, 6, 0, 0)
        )

    def get_arunodaya(self, date):

        sunrise = self.get_sunrise(date)
        return sunrise - timedelta(minutes=self.ARUNODAYA_MINUTES)

    def is_dashami_pure(self, date):

        arunodaya = self.get_arunodaya(date)

        tithi_at_arunodaya = self.get_tithi(arunodaya)

        if tithi_at_arunodaya in [10, 25]:
            return False

        check_before = arunodaya - timedelta(minutes=30)
        tithi_before = self.get_tithi(check_before)

        if (tithi_before in [10, 25]) and (tithi_at_arunodaya in [11, 26]):
            return True

        return tithi_at_arunodaya not in [10, 25]

    def get_ekadashi_dates(self, year):

        results = []

        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)

        current = start_date

        candidates = []

        while current <= end_date:

            sunrise = self.get_sunrise(current)
            arunodaya = self.get_arunodaya(current)

            tithi_sunrise = self.get_tithi(sunrise)
            tithi_arunodaya = self.get_tithi(arunodaya)

            if tithi_sunrise in [11, 26] or tithi_arunodaya in [11, 26]:

                is_pure = self.is_dashami_pure(current)

                candidates.append({
                    "date": current.date(),
                    "tithi_sunrise": tithi_sunrise,
                    "tithi_arunodaya": tithi_arunodaya,
                    "is_pure": is_pure
                })

            current += timedelta(days=1)

        i = 0

        while i < len(candidates):

            cand = candidates[i]

            if i + 1 < len(candidates):

                next_cand = candidates[i + 1]

                if (next_cand["date"] - cand["date"]).days == 1:

                    if next_cand["is_pure"]:
                        chosen = next_cand
                    elif cand["is_pure"] and not next_cand["is_pure"]:
                        chosen = cand
                    else:
                        chosen = next_cand

                    if chosen["is_pure"]:

                        sunrise = self.get_sunrise(chosen["date"])
                        tithi = self.get_tithi(sunrise)

                        paksha = "Shukla" if tithi == 11 else "Krishna"

                        results.append({
                            "date": chosen["date"],
                            "paksha": paksha
                        })

                    i += 2
                    continue

            if cand["is_pure"]:

                sunrise = self.get_sunrise(cand["date"])
                tithi = self.get_tithi(sunrise)

                paksha = "Shukla" if tithi == 11 else "Krishna"

                results.append({
                    "date": cand["date"],
                    "paksha": paksha
                })

            i += 1

        return results

    def is_ekadashi(self, date):

        if isinstance(date, datetime):
            date = date.date()

        year = date.year

        ek_dates = self.get_ekadashi_dates(year)

        return any(e["date"] == date for e in ek_dates)

    def next_ekadashi(self):

        today = datetime.now(self.tz).date()

        for year in [today.year, today.year + 1]:

            ek_dates = self.get_ekadashi_dates(year)

            for ek in ek_dates:

                if ek["date"] > today:

                    return {
                        "date": ek["date"],
                        "paksha": ek["paksha"],
                        "days_until": (ek["date"] - today).days
                    }

        return None


calculator = EkadashiCalculator()


def is_ekadashi(date):
    return calculator.is_ekadashi(date)


def get_ekadashi_dates(year):
    return calculator.get_ekadashi_dates(year)


def next_ekadashi():
    return calculator.next_ekadashi()


if __name__ == "__main__":

    print("Testing Ekadashi Calculator")

    calc = EkadashiCalculator()

    ek_2026 = calc.get_ekadashi_dates(2026)

    print("\nTotal Ekadashis:", len(ek_2026))

    for e in ek_2026:
        print(e["date"], "-", e["paksha"])