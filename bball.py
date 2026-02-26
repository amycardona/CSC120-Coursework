''' 
File: bball.py
Author: Amy Cardona
Class: CSC120, Fall 2025
Purpose: The program reads a basketball data file, creates 
Team objects for each line, and groups them into Conference 
objects within a ConferenceSet. It calculates each team's win 
ratio, computes average win ratios for all conferences, and 
prints the conference(s) with the highest average 
win ratio.
'''

class Team:
    def __init__(self, line):
        line = line.strip()
        # Find rightmost '(' and ')'
        right_paren = line.rfind(')')
        left_paren = line.rfind('(', 0, right_paren)
        self._conf = line[left_paren + 1:right_paren].strip()

        # Extract wins and losses (last two tokens)
        tokens = line[right_paren + 1:].split()
        self._wins = int(tokens[0])
        self._losses = int(tokens[1])

        # Team name = everything before left_paren
        self._name = line[:left_paren].strip()

    def name(self):
        return self._name

    def conf(self):
        return self._conf

    def win_ratio(self):
        total = self._wins + self._losses
        if total == 0:
            return 0.0
        return float(self._wins) / total

    def __str__(self):
        return "{} : {}".format(self._name, str(self.win_ratio()))


class Conference:
    def __init__(self, conf):
        self._name = conf
        self._teams = []

    def __contains__(self, team):
        # Check if this team is already in the conference
        for t in self._teams:
            if t.name() == team.name():
                return True
        return False

    def name(self):
        return self._name

    def add(self, team):
        if not self.__contains__(team):
            self._teams.append(team)

    def win_ratio_avg(self):
        if len(self._teams) == 0:
            return 0.0
        total = 0.0
        count = 0
        for t in self._teams:
            total = total + t.win_ratio()
            count = count + 1
        return total / count

    def __str__(self):
        return "{} : {}".format(self._name, str(self.win_ratio_avg()))


class ConferenceSet:
    def __init__(self):
        self._confs = []

    def add(self, team):
        # See if conference already exists
        conf_name = team.conf()
        found = False
        for conf in self._confs:
            if conf.name() == conf_name:
                conf.add(team)
                found = True
                break
        if not found:
            new_conf = Conference(conf_name)
            new_conf.add(team)
            self._confs.append(new_conf)

    def best(self):
        # Find the highest average ratio
        best_avg = 0.0
        for conf in self._confs:
            avg = conf.win_ratio_avg()
            if avg > best_avg:
                best_avg = avg

        # Collect all with this average
        best_list = []
        for conf in self._confs:
            if conf.win_ratio_avg() == best_avg:
                best_list.append(conf)

        # Sort alphabetically
        best_list.sort(key=lambda c: c.name())
        return best_list


def main():
    filename = input().strip()
    infile = open(filename, 'r')

    confs = ConferenceSet()

    for line in infile:
        line = line.strip()
        if len(line) == 0 or line.startswith('#'):
            continue
        team = Team(line)
        confs.add(team)

    infile.close()

    best_confs = confs.best()
    for conf in best_confs:
        print("{} : {}".format(conf.name(), conf.win_ratio_avg()))


# Run the program
if __name__ == "__main__":
    main()
