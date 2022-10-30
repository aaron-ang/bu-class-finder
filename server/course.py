from datetime import datetime


class Course:
    def __init__(self, college, department, number, section):
        now = datetime.now()
        self.year = now.year
        self.semester = "Fall" if 4 <= now.month < 10 else "Spring"
        self.college = college.upper()
        self.department = department.upper()
        self.number = number
        self.section = section.upper()
        self.reg_url = ("https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1?ModuleName="
                        f"univschr.pl&SearchOptionDesc=Class+Number&SearchOptionCd=S&"
                        f"ViewSem={self.semester}+{self.year}&KeySem=20233&AddPlannerInd="
                        f"&College={self.college}&Dept={self.department}&Course={self.number}&Section={self.section}")

    def __str__(self):
        return f"{self.college} {self.department}{self.number} {self.section}"
