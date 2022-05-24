import xlrd
import xlsxwriter as xlwt


def list_dates(s):
    dates = []
    date_strings = s.split(",")
    for date_s in date_strings:
        if date_s != "":
            if "-" in date_s:
                date_bounds = date_s.split("-")
                for i in range(int(date_bounds[0]), int(date_bounds[1]) + 1):
                    dates.append(i)
            else:
                dates.append(int(date_s))
    return dates


def read_from_excel(filename: str) -> list:
    """
    Reads data from the excel file and divides it up into their respective categories.

    Args:
        filename (str): Given filename. Must end in ".xlsx".

    Returns:
        sheets (list): A 2D list of data aggregated from the excel sheet.
    """
    sheets = []
    wb = xlrd.open_workbook(filename)
    for sheet_name in wb.sheet_names():
        data = {}
        sheet = wb.sheet_by_name(sheet_name)
        if sheet.cell_value(0, 0) == "Kuu (numbriga)":
            data["month"] = int(sheet.row_values(0)[1])
            data["year"] = int(sheet.row_values(1)[1])
            data["template"] = {24: int(sheet.row_values(2)[1]), 12: int(sheet.row_values(3)[1])}
            data["employees"] = []
            for i in range(6, sheet.nrows):
                if sheet.row_values(i)[0] != "":
                    data["employees"].append(sheet.row_values(i))
            sheets.append(data)
    return sheets


def write_to_excel(bests, filename):
    wb = xlwt.Workbook(filename)
    hgs = 1
    print(len(bests))
    for schedule in bests:
        sheet = wb.add_worksheet("Graafik " + str(hgs))
        hgs += 1
        month_format = wb.add_format({"bold": True, "font_size": 20, "align": "center"})
        heading_format = wb.add_format(
            {"bold": True, "align": "center", "bg_color": "#F9F0DB", "border": 1, "bottom": 1})
        date_format = wb.add_format({"align": "center", "bg_color": "#F9F0DB", "border": 1})
        personal_data_format = wb.add_format({"bg_color": "#F9F0DB", "border": 1})
        stats_format = wb.add_format({"align": "center", "bg_color": "#F9F0DB", "border": 1})
        decimal_stats_format = wb.add_format({"align": "center", "bg_color": "#F9F0DB", "border": 1})
        decimal_stats_format.set_num_format("0.00")
        bottom_stats_format = wb.add_format({"bg_color": "#F9F0DB", "border": 1})
        weekday_format = wb.add_format({"align": "center", "bg_color": "#F9F0DB", "border": 1, "bottom": 1})
        weekend_format = wb.add_format({"align": "center", "bg_color": "#DE222F", "border": 1, "bottom": 1})
        day_off_format = wb.add_format({"align": "center", "bg_color": "#4BACC6", "border": 1})
        non_employee_format = wb.add_format({"bg_color": "#CDCDCD", "border": 1})
        empty_format = wb.add_format({"border": 1})

        months = ["Jaanuar", "Veebruar", "Märts", "Aprill", "Mai", "Juuni", "Juuli", "August", "September", "Oktoober",
                  "November", "Detsember"]
        month_string = months[schedule.month - 1] + " " + str(schedule.year)
        sheet.set_row(0, 30)
        sheet.merge_range(0, 0, 0, 1, month_string, month_format)

        left_side_columns = ["Eesnimi", "Perenimi", "Telefon", "Email", "Aadress", "Koormus"]
        left_side_widths = [14, 14, 0, 0, 0, 0]
        left_side_formats = [personal_data_format, personal_data_format, personal_data_format, personal_data_format,
                             personal_data_format, decimal_stats_format]
        for i in range(len(left_side_columns)):
            sheet.set_column(i, i, left_side_widths[i])
            sheet.write(1, i, left_side_columns[i], heading_format)

        sheet.set_column(len(left_side_columns), schedule.days_in_month + len(left_side_columns) - 1, 3)
        days = ["E", "T", "K", "N", "R", "L", "P"]
        for i in range(1, schedule.days_in_month + 1):
            sheet.write(0, i + len(left_side_columns) - 1, i, date_format)
            if i in schedule.holidays:
                sheet.write(1, i + len(left_side_columns) - 1, days[(i - 1 + schedule.first_day_of_month) % 7],
                            weekend_format)
            else:
                sheet.write(1, i + len(left_side_columns) - 1, days[(i - 1 + schedule.first_day_of_month) % 7],
                            weekday_format)

        right_side_columns = ["Tehtud tunnid", "Normtunnid", "Teha veel", "Kordi"]
        right_side_widths = [14, 12, 10, 8]
        for i in range(len(right_side_columns)):
            sheet.set_column(len(left_side_columns) + schedule.days_in_month + i,
                             len(left_side_columns) + schedule.days_in_month + i, right_side_widths[i])
            sheet.write(1, len(left_side_columns) + schedule.days_in_month + i, right_side_columns[i], heading_format)

        schedule_markings = {
            "day_off": ("", day_off_format),
            "vacation": ("P", day_off_format),
            "sick_leave": ("H", day_off_format),
            "training": ("K", day_off_format),
            "non_employee": ("", non_employee_format),
            24: (24, empty_format),
            12: (12, empty_format),
            10: (10, empty_format),
            8: (8, empty_format),
            0: ("", empty_format),
            1: ("", empty_format),
            2: ("", empty_format),
            3: ("", empty_format),
            4: ("", empty_format),
            5: ("", empty_format)
        }
        j = 2
        for employee in schedule.employees:
            data = employee.data
            for i in range(len(left_side_columns)):
                sheet.write(j, i, data[left_side_columns[i]], left_side_formats[i])
            for date in range(schedule.days_in_month):
                day = schedule.schedule[employee][date]
                if day in schedule_markings:
                    sheet.write(j, len(left_side_columns) + date, schedule_markings[day][0], schedule_markings[day][1])
                else:
                    sheet.write(j, len(left_side_columns) + date, day)
            stats = [
                "=SUM(INDIRECT(ADDRESS(" + str(j + 1) + ", " + str(len(left_side_columns) + 1) + ")):INDEX(" + str(
                    j + 1) + ":" + str(j + 1) + ", COLUMN() - 1))",
                employee.nominal_hours,
                "=INDEX(" + str(j + 1) + ":" + str(j + 1) + ", COLUMN() - 2) - INDEX(" + str(j + 1) + ":" + str(
                    j + 1) + ", COLUMN() - 1)",
                "=COUNT(INDIRECT(ADDRESS(" + str(j + 1) + ", " + str(len(left_side_columns) + 1) + ")):INDEX(" + str(
                    j + 1) + ":" + str(j + 1) + ", COLUMN() - 4))"
            ]
            for i in range(len(stats)):
                sheet.write(j, len(left_side_columns) + schedule.days_in_month + i, stats[i], stats_format)

            j += 1

        bottom_stats = ["24h vahetusi: ", "12h vahetusi: ", "10h vahetusi: ", "8h vahetusi", "Kokku: "]
        for i in range(len(bottom_stats)):
            sheet.write(j + i, len(left_side_columns) - 5, bottom_stats[i], bottom_stats_format)

        for i in range(len(left_side_columns), len(left_side_columns) + schedule.days_in_month):
            sheet.write(j, i, "=COUNTIF(INDIRECT(_xlfn.CONCAT(ADDRESS(3, " +
                        str(i + 1) + "), \":\", ADDRESS(" + str(j) + ", " + str(i + 1) + "))), \"=24\")",
                        bottom_stats_format)
            sheet.write(j + 1, i, "=COUNTIF(INDIRECT(_xlfn.CONCAT(ADDRESS(3, " +
                        str(i + 1) + "), \":\", ADDRESS(" + str(j) + ", " + str(i + 1) + "))), \"=12\")",
                        bottom_stats_format)
            sheet.write(j + 2, i, "=COUNTIF(INDIRECT(_xlfn.CONCAT(ADDRESS(3, " +
                        str(i + 1) + "), \":\", ADDRESS(" + str(j) + ", " + str(i + 1) + "))), \"=10\")",
                        bottom_stats_format)
            sheet.write(j + 3, i, "=COUNTIF(INDIRECT(_xlfn.CONCAT(ADDRESS(3, " +
                        str(i + 1) + "), \":\", ADDRESS(" + str(j) + ", " + str(i + 1) + "))), \"=8\")",
                        bottom_stats_format)
            sheet.write(j + 4, i, "=SUM(INDIRECT(_xlfn.CONCAT(ADDRESS(" +
                        str(j + 1) + ", " + str(i + 1) + "), \":\", ADDRESS(" + str(j + 4) + ", " + str(i + 1) + "))))",
                        bottom_stats_format)
    wb.close()
