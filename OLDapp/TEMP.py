from datetime import datetime
from typing import List


class Base:
    def __init__(self, full_amount, invested_amount) -> None:
        self.full_amount = full_amount
        self.invested_amount = invested_amount
        self.fully_invested = False
        self.close_date = None

    def __repr__(self) -> str:
        return (
            f'full_amount = {self.full_amount}\n'
            f'invested_amount = {self.invested_amount}\n'
            f'fully_invested = {self.fully_invested}\n'
            f'close_date = {self.close_date}\n'
            '\n'
        )

    def not_invested(self) -> int:
        return self.full_amount - self.invested_amount

    def invest(self, investition):
        if investition > self.not_invested():
            return
        self.invested_amount += investition
        if self.full_amount == self.invested_amount:
            self.fully_invested = True
            self.close_date = datetime.now()


class Project(Base):
    ...


class Donation(Base):
    ...


def do_invest(proj: Project, donat: Donation):
    if proj.not_invested() >= donat.not_invested():
        investition = donat.not_invested()
        proj.invest(investition)
        donat.invest(investition)
    elif proj.not_invested() < donat.not_invested():
        investition = proj.not_invested()
        proj.invest(investition)
        donat.invest(investition)


def invest(projects: List[Project], donations: List[Donation]):
    projects_iter = iter(projects)
    donations_iter = iter(donations)
    project = next(projects_iter)
    donation = next(donations_iter)
    while project and donation:

        do_invest(project, donation)
        if project.fully_invested:
            try:
                project = next(projects_iter)
            except StopIteration:
                project = None
        if donation.fully_invested:
            try:
                donation = next(donations_iter)
            except StopIteration:
                donation = None


donat1 = Donation(100, 0)
donat2 = Donation(800, 0)
donat3 = Donation(100, 0)
donat4 = Donation(1000, 0)
donat5 = Donation(1000, 0)
donat6 = Donation(3001, 0)
big_donat = Donation(50000, 0)
lil_donat = Donation(1, 0)

donat = [donat1, donat2, donat3, donat4, donat5, donat6]

proj1 = Project(1000, 0)
proj2 = Project(2000, 0)
proj3 = Project(3000, 0)

# proj = [proj1, proj2, proj3]
proj = [proj3, proj2, proj1]
# proj.fully_invested = True
donat = [lil_donat]
invest(proj, donat)

# donat = [donat1, donat2, donat3, donat4, donat5, donat6]
proj = [proj3, proj2, proj1]
# proj = [proj1, proj2, proj3]
print(proj, donat)

# myiter = iter(proj)
# print(next(myiter))
# print(next(myiter))
# print(next(myiter))
# print(next(myiter))  # StopIteration
