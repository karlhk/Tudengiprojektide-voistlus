class AvailableEmployees:
    """
    A class representing all of the available employees and their shift lengths on a given day.

    Attributes
    ----------
    day : int
        An integer representing the specific day that these employees are available.
    available : set
        A set containing all of the shift lengths and the lists of employees that can perform them.

    Methods
    -------
    get_employees(template)

    """

    def __init__(self, day: int, employees: list):
        """
        Establishes what shifts each of the employees can do on a specific day.

        Args:
            day (int): An integer representing the specific day (1-31) that these employees are available.
            employees (list): A list of employees that are given to the method (usually all of the employees).
        """
        self.available = {}
        self.day = day
        for employee in employees:
            if employee.is_available(day):
                for shift_length in employee.shift_lengths:
                    if shift_length not in self.available:
                        self.available[shift_length] = []
                    self.available[shift_length].append(employee)

    def get_employees(self, template: dict) -> dict:
        """
        Goes through every shift length in the template and assigns the required amount of employees to every day.
        
        Args:
            template (dict): A dict representing how many and what length of shifts are needed in a single day.

        Returns:
            employees_dict (dict): A dict of the chosen employees and their chosen shift lengths.
        """
        employees_dict = {}
        for shift_length in sorted(self.available, key=lambda x: len(self.available[x])):
            if shift_length in template:
                employees_dict[shift_length] = self.get_best(shift_length, template[shift_length])
        return employees_dict

    def get_best(self, shift_length: int, number: int) -> list:
        """
        Chooses a @number amount of employees to fill the chosen shift length.

        Args:
            shift_length (int): An int representing how long (in hours) the given shift is.
            number (int): An int representing how many of these types of shifts there should be in a day.

        Returns:
            best (list): A list of employees that were chosen for the given shift length.

        """
        all_available = sorted(self.available[shift_length], key=lambda x: x.get_priority(self.day, shift_length))
        best = []
        for i in range(number):
            if len(all_available) > 0:
                best.append(all_available.pop())
        self.fix_collisions(best, all_available, shift_length)

        # Removes all selected employees from the pool of available employees.
        for employee in best:
            for shift_length in self.available:
                if employee in self.available[shift_length]:
                    self.available[shift_length].remove(employee)
        return best

    def fix_collisions(self, best: list, all_available: list, shift_length: int):
        """

        Args:
            best (list): A list of the employees that have been selected for the shift.
            all_available (list): A list of the day's available employees of the given shift length.
            shift_length (int): An int representing the length of the given shift.

        Returns:

        """
        i = 0
        while i < len(best):
            change = False
            current = best[i]
            if current.match is not None and current.match not in best:
                change = True
                if current.match in all_available and (
                        (
                                (current.worked_hours < current.nominal_hours and
                                 current.match.worked_hours < current.match.nominal_hours) or
                                (current.worked_hours >= current.nominal_hours and
                                 current.match.worked_hours >= current.match.nominal_hours)
                        ) or
                        "peab koos" in current.rules):
                    alt1 = None
                    for i in range(len(best) - 1, -1, -1):
                        if best[i] != current:
                            alt1 = best[i]
                            break
                    alt2 = None
                    for emp in all_available:
                        if emp.match is None:
                            alt2 = emp
                    if alt1 is not None and alt2 is not None:
                        match_priority = current.get_priority(self.day, shift_length) + current.match.get_priority(
                            self.day, shift_length)
                        alt_priority = alt1.get_priority(self.day, shift_length) + alt2.get_priority(self.day,
                                                                                                     shift_length)
                        if match_priority > alt_priority:
                            best.remove(alt1)
                            all_available.remove(current.match)
                            best.append(current.match)
                        else:
                            best.remove(current)
                            all_available.remove(alt2)
                            best.append(alt2)
                    else:
                        if alt1 is not None:
                            best.remove(alt1)
                        all_available.remove(current.match)
                        best.append(current.match)
                else:
                    if "peab koos" in current.rules:
                        best.remove(current)
                        if len(all_available) > 0:
                            best.append(all_available.pop())
                            i = 0
                    else:
                        change = False
            if len(current.dont_match) > 0:
                for dont_match in current.dont_match:
                    if dont_match in best:
                        change = True
                        if best.index(current) < best.index(dont_match):
                            best.remove(dont_match)
                            if len(all_available) > 0:
                                best.append(all_available.pop())
                        else:
                            best.remove(current)
                            if len(all_available) > 0:
                                best.append(all_available.pop())
                            break
            if change:
                i = 0
            else:
                i += 1
