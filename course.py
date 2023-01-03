from datetime import datetime


class Course:
    bin_prefix = ("https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1?ModuleName="
                  "univschr.pl&SearchOptionDesc=Class+Number&SearchOptionCd=S")
    reg_prefix = ("https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1?ModuleName="
                  "reg%2Fadd%2Fbrowse_schedule.pl&SearchOptionDesc=Class+Number&SearchOptionCd=S")

    now = datetime.now()
    semester = "Fall" if 4 <= now.month < 10 else "Spring"
    year = now.year + 1 if (semester == "Spring" and 10 <=
                            now.month <= 12) else now.year

    def __init__(self, full_course: str):
        college, dep_num, section = full_course.split()
        department, number = dep_num[:2], dep_num[2:]

        self.semester_code = 3 if self.semester == "Fall" else 4
        self.college = college.upper()
        self.department = department.upper()
        self.number = number
        self.section = section.upper()

        self.formatted_params = (f"&KeySem={self.year}{self.semester_code}&AddPlannerInd=&College={self.college}"
                                 f"&Dept={self.department}&Course={self.number}&Section={self.section}")

        self.bin_url = self.bin_prefix + self.formatted_params
        self.reg_url = self.reg_prefix + self.formatted_params

    def __str__(self):
        return f"{self.college} {self.department}{self.number} {self.section}"
