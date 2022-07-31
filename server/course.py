class Course:
    def __init__(self, college, department, number, section):
        self.college = college.upper()
        self.department = department.upper()
        self.number = number
        self.section = section.upper()
        self.reg_url = ("https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1?ModuleName="
                        f"reg%2Fadd%2Fbrowse_schedule.pl&SearchOptionDesc=Class+Number&SearchOptionCd=S&"
                        f"ViewSem=Fall+2022&KeySem=20233&AddPlannerInd=&College={self.college}&Dept={self.department}&Course={self.number}&Section={self.section}")

    def __str__(self):
        return f"{self.college} {self.department}{self.number} {self.section}"