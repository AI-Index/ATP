from tptp_metadata import versions_list, version_to_year

class TPTP_Problem:
    # just the ratings tuple
    # tuples including each version
    # score by year
    def __init__(self, filepath):
        try:
            with open(filepath, "r") as f:
                lines = f.readlines()
        except:
            print("Could not read lines from file %s" % filepath)
            Exception()
        self.valid = True
        self.last_version_updated = last_update_from_lines(lines)
        self.problem_instance = problem_instance_from_lines(lines)
        self.problem_class = self.problem_instance[:3]
        if filepath.split(".")[-1] == "rm" or self.last_version_updated < "v5.0.0":
            self.valid = False
            return

        self.spc = spc_from_lines(lines)
        self.reported_ratings = ratings_from_lines(lines)
        self.ratings = ratings_from_tuples(self.reported_ratings)
        self.scores = score_by_year(self.ratings)

        self.last_score = self.scores[-1][1]

        # self.score_at_v5_0_0 = dict(self.ratings)["v5.0.0"]
        ratings_dict = dict(self.ratings)
        most_recent = None
        index = versions_list.index("v5.0.0")
        while most_recent is None:
            most_recent = ratings_dict[versions_list[index]]
            index += 1
        self.score_at_v5_0_0 = most_recent

        if (self.score_at_v5_0_0 == self.last_score) and (self.last_score == 1 or self.last_score == 0):
            self.valid = False


    def last_changed(self):
        return self.last_version_updated

    def __str__(self):
        lines = ([
            "",
            self.problem_instance,
            "---",
            "SPC:\t\t%s" % self.spc,
            "Last Updated:\t%s" % self.last_version_updated,
            "",
            ])
        return "\n".join(lines)

def versions_before(version):
    versions = []
    index = 0
    while version > versions_list[index]:
        versions.append(versions_list[index])
        index += 1

    return versions

def versions_between(v1, v2):
    versions = []
    index = 0
    while v1 > versions_list[index]:
        index += 1

    while v2 > versions_list[index]:
        versions.append(versions_list[index])
        index += 1

    return versions

def versions_after(version):
    index = 0
    while version > versions_list[index]:
        index += 1
    return versions_list[index:]

def ratings_from_tuples(tuples):
    ratings = []

    # Fill in all versions before first version with None
    for v in versions_before(tuples[0][1]):
        ratings.append((v, None))

    for (score, v1), (_, v2) in zip(tuples, tuples[1:]):
        for v in versions_between(v1, v2):
            ratings.append((v, score))

    for v in versions_after(tuples[-1][1]):
        ratings.append((v, tuples[-1][0]))

    return ratings

def ratings_from_lines(lines):
    ratings_lines = [line for line in lines if line[:8] == "% Rating"]
    if len(ratings_lines) != 1:
        print("More or less than one line with ratings line in file %s" % filepath)
        Exception()

    ratings_line = ratings_lines[0]
    split_ratings = ratings_line.split(":")
    if len(split_ratings) > 2:
        print("More than one semilcolon in ratings line in file %s" % filepath)
        Exception()

    ratings = split_ratings[1].strip()
    ratings_tuple = list(reversed([tuple(item.split(" ")) for item in ratings.split(", ")]))
    return ratings_tuple

def spc_from_lines(lines):
    spc_lines = [line for line in lines if line[:5] == "% SPC"]
    if len(spc_lines) == 0:
        return -1
    return spc_lines[0].split(":")[1].strip().split("_")[0]

def last_update_from_lines(lines):
    last_updated = lines[1].strip().split(" ")[-1][:-1]
    if last_updated not in versions_list:
        last_updated = versions_after(last_updated)[0]
    return last_updated

def problem_instance_from_lines(lines):
    return lines[1].split(":")[1].strip()

def score_by_year(ratings):
    scores = []
    ratings_dict = dict(ratings)
    for v, y in sorted(version_to_year.items()):
        scores.append((y, ratings_dict[v]))
    return scores

if __name__ == "__main__":
    import os
    filepath = os.path.join("Problems", "ALG", "ALG001-1.p")
    tptp_prob = TPTP_Problem(filepath)
    print(tptp_prob)
