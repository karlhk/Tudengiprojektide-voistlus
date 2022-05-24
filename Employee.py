import IOHandler as io
import random


class Employee:

    def __init__(self, data: list, schedule):
        """
        Initializes the employee based on the given data from the excel file and

        Args:
            data (list): Data taken from the excel file.
            schedule:
        """

        self.schedule = schedule
        self.data = {
            "Eesnimi": data[0],
            "Perenimi": data[1],
            "Telefon": data[2],
            "Email": data[3],
            "Aadress": data[4],
            "Koormus": data[5]
        }
        self.name = self.data["Eesnimi"] + " " + self.data["Perenimi"]
        self.nominal_load = float(data[5])

        self.request_days = io.list_dates(data[6])
        self.vacation_days = io.list_dates(data[7])

        self.shift_lengths = [int(shift_length) for shift_length in data[8].split(",")]
        self.rules = {}
        for rule in data[10].split(";"):
            if rule != "":
                key, value = rule.split(":")
                if key.strip() not in self.rules:
                    if key.strip() in ["koolitus", "ei tohi koos"]:
                        self.rules[key.strip()] = [value.strip()]
                    else:
                        self.rules[key.strip()] = value.strip()
                else:
                    self.rules[key.strip()].append(value.strip())
        self.training_days = []
        self.training_hours = 0
        self.sick_days = []
        self.non_employee = []
        self.only24 = []
        self.only12 = []
        self.unpack_rules()
        if data[9] == "":
            data[9] = 0
        self.nominal_hours = -data[9] - self.training_hours
        if min(self.shift_lengths) < 12:
            self.shift_lengths.append(12)
            self.rules["shortershift"] = min(self.shift_lengths)
        else:
            self.rules["shortershift"] = False
        for day in range(1, schedule.days_in_month + 1):
            if day not in schedule.holidays + self.vacation_days + self.sick_days + self.non_employee:
                self.nominal_hours += 8 * self.nominal_load
        self.worked_hours = 0
        self.match = None
        self.dont_match = []
        self.priority_score = 0

    def unpack_rules(self):
        """
        Sets the Employee's rules according to the data in the excel file.
        """

        if "võiks paus" not in self.rules:
            self.rules["võiks paus"] = 2
        if "peab paus" not in self.rules:
            self.rules["peab paus"] = 1
        if "nädala kaupa" in self.rules:
            self.rules["paus"] = int(self.rules["nädala kaupa"])
        else:
            self.rules["paus"] = 3
        if "koolitus" in self.rules:
            for session in self.rules["koolitus"]:
                dates, hours = session.split("/")
                self.training_days += io.list_dates(dates)
                self.training_hours += int(hours) * len(self.training_days)
        if "haigusleht" in self.rules:
            dates = self.rules["haigusleht"]
            self.sick_days = io.list_dates(dates)
        if "alustab" in self.rules:
            date = self.rules["alustab"]
            self.non_employee = io.list_dates("1-" + str(int(date) - 1))
        if "lõpetab" in self.rules:
            date = self.rules["lõpetab"]
            self.non_employee += io.list_dates(str(date) + "-" + self.schedule.days_in_month)
        if "ainult 24" in self.rules:
            dates = self.rules["ainult 24"]
            self.only24 += io.list_dates(dates)
        if "ainult 12" in self.rules:
            dates = self.rules["ainult 12"]
            self.only12 += io.list_dates(dates)

    def set_up_schedule(self):
        """
        Sets certain days as busy so the employee won't be put to work on those days.
        """

        self.schedule.schedule[self] = [0] * self.schedule.days_in_month
        for day in self.request_days:
            self.schedule.schedule[self][day - 1] = "day_off"
        for day in self.vacation_days:
            self.schedule.schedule[self][day - 1] = "vacation"
        for day in self.training_days:
            if day >= 2 and self.schedule.schedule[self][day - 2] == 0:
                self.schedule.schedule[self][day - 2] = 3
            self.schedule.schedule[self][day - 1] = "training"
        for day in self.sick_days:
            self.schedule.schedule[self][day - 1] = "sick_leave"
        for day in self.non_employee:
            self.schedule.schedule[self][day - 1] = "non_employee"
        if "argipäeviti" in self.rules:
            for day in range(1, self.schedule.days_in_month + 1):
                if day not in self.schedule.holidays and self.schedule.schedule[self][day - 1] == 0:
                    self.schedule.schedule[self][day - 1] = int(self.rules["argipäeviti"])
                else:
                    self.schedule.schedule[self][day - 1] = 1

    def is_available(self, date: int) -> bool:
        """
        Checks if the employee is available on a specific date.

        Args:
            date (int): An int that represents the day part (1-30/31) of the date.

        Returns:
            True if they are available.
            False if they are not.
        """

        if self.schedule.schedule[self][date - 1] in [0, 2, 3, 4, 5]:
            return True
        else:
            return False

    def has_shift(self, shift_length: int, shift_date: int):
        """
        Checks if the employee needs a break for having too many consecutive days at work
        and gives them a break that abides by the employee's break rules.

        Args:
            shift_length (int): Given shift length.
            shift_date (int): Given day of shift.
        """

        if shift_length == 12 and self.rules["shortershift"]:
            shift_length = min(self.shift_lengths)

        self.schedule.schedule[self][shift_date - 1] = shift_length

        if shift_length == 24:
            consequtive = 0
            for i in range(shift_date - 7, shift_date):
                if i >= 0 and self.schedule.schedule[self][i] == 24:
                    consequtive += 1

            # Checks if the employee has had exactly 4 days of 24h shifts in a row and gives them a break if so.
            if consequtive == 4:
                for i in range(shift_date, shift_date + self.rules["paus"]):
                    if i < self.schedule.days_in_month and self.schedule.schedule[self][i] in [0, 2]:
                        self.schedule.schedule[self][i] = 1
            for i in range(shift_date, shift_date + int(self.rules["peab paus"])):
                if i < self.schedule.days_in_month and self.schedule.schedule[self][i] in [0, 2]:
                    self.schedule.schedule[self][i] = 1
            for i in range(shift_date, shift_date + int(self.rules["võiks paus"])):
                if i < self.schedule.days_in_month and self.schedule.schedule[self][i] == 0:
                    self.schedule.schedule[self][i] = 2

        if shift_length in [8, 10, 12]:
            consecutive = 0
            for i in range(shift_date - 5, shift_date):
                if i >= 0 and self.schedule.schedule[self][i] in [8, 10, 12]:
                    consecutive += 1
            if consecutive == 5:
                for i in range(shift_date, shift_date + 2):
                    if i < self.schedule.days_in_month and self.schedule.schedule[self][i] in [0, 2, 4, 5]:
                        self.schedule.schedule[self][i] = 1

        self.worked_hours += shift_length

    def get_priority(self, day, shift_length):
        if shift_length == 24 and day in self.only12 or shift_length == 12 and day in self.only24:
            return -100000000000
        possible = 0
        for i in range(day, self.schedule.days_in_month + 1):
            if i not in self.request_days + self.vacation_days + self.training_days + self.sick_days + self.non_employee:
                possible += 1
                if shift_length == 24:
                    i += 1
        priority = (self.nominal_hours - self.worked_hours) * 100 / (
                shift_length * (self.nominal_hours / self.schedule.full_time_hours))
        if shift_length == 24 and day in self.only24 or shift_length == 12 and day in self.only12:
            priority += 1000000
        if "võib teha ületunde" not in self.rules and priority <= 0.5:
            priority -= 80
        if "eelistab" in self.rules:
            if shift_length != self.rules["eelistab"]:
                priority -= 5
            else:
                priority += 5
        if "nädala kaupa" in self.rules:
            count24 = 0
            for i in range(max(0, day - 7), day):
                if self.schedule.schedule[self][i] == 24:
                    count24 += 1
            if count24 in [1, 2, 3]:
                priority += 10000000
            if count24 == 0 and self.worked_hours > self.nominal_hours:
                return -1000000
        if self.schedule.schedule[self][day - 1] == 2 and not (
                (shift_length == 24 and day in self.only24) or (shift_length == 12 and day in self.only12)):
            priority -= 1000
        if self.schedule.schedule[self][day - 1] == 3:
            priority -= 1000000
        if self.schedule.schedule[self][day - 2] in [8, 10, 12]:
            priority += 40
        priority = priority / possible + random.randint(-10, 10) / random.randint(1, 10)
        return priority

    def __str__(self):
        return self.name
