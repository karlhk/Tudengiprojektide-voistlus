import calendar
from datetime import date
import holidays

from AvailableEmployees import AvailableEmployees
from Employee import Employee


class Schedule:

    def __init__(self, month, year, template, employees):
        """
        Takes data from the excel file and matches the employees into a schedule based on many different criteria.
        Criteria include employees' wishes and the schedule's needs.

        Args: (All taken from the excel file)
            month (int): Given month of the given year.
            year (int): Given year.
            template (dict): A two-element list, which describes what length and how many shifts are needed every day.
            employees (list): A list of the first names of all the employees.
        """
        self.month = month
        self.year = year
        self.first_day_of_month, self.days_in_month = calendar.monthrange(year, month)
        self.holidays = []
        for i in range(1, self.days_in_month + 1):
            if (i - 1 + self.first_day_of_month) % 7 >= 5 or \
                    date(year, month, i) in holidays.Estonia() and i not in self.holidays:
                self.holidays.append(i)
        self.full_time_hours = sum([8 for i in range(1, self.days_in_month + 1) if i not in self.holidays])
        self.template = template
        self.schedule = {}
        self.employees = []
        self.add_employees(employees)
        self.score = 0

    def add_employees(self, employees):
        """
        Adds the given employees to the schedule and sets their busy days.

        Args:
            employees (Employee[]):
        """
        for employees_data in employees:
            employee = Employee(employees_data, self)
            self.employees.append(employee)
            employee.set_up_schedule()
        self.set_up_combo_rules()

    def set_up_combo_rules(self):
        """
        Sets up match rules of which employee should or should not be placed together with whichever other employee.
        """
        for employee in self.employees:
            if "peab koos" in employee.rules:
                for potential_match in self.employees:
                    if employee.rules["peab koos"] == potential_match.name:
                        employee.match = potential_match
                        break
            if "võiks koos" in employee.rules:
                for potential_match in self.employees:
                    if employee.rules["võiks koos"] == potential_match.name:
                        employee.match = potential_match
                        break
            if "ei tohi koos" in employee.rules:
                for dont_match in employee.rules["ei tohi koos"]:
                    for potential_match in self.employees:
                        if dont_match == potential_match.name:
                            employee.dont_match.append(potential_match)
                            break

    def fill_schedule(self):
        """
        Fills the schedule with employees as needed.
        Takes into account if the employee can work overtime.
        """
        for day in range(1, self.days_in_month + 1):
            available = AvailableEmployees(day, self.employees)
            workers = available.get_employees(self.template)
            for shift_length in workers:
                for worker in workers[shift_length]:
                    worker.has_shift(shift_length, day)
        for employee in self.employees:
            if "võib teha ületunde" not in employee.rules:
                self.score -= abs(employee.worked_hours - employee.nominal_hours)
