import os
from tptp_metadata import versions_list, years_list
from TPTP_Problem import TPTP_Problem

def get_total_averages(scores_list):
    averaged_scores = []
    for year_ix in range(len(years_list)):
        counter = 0
        year_avg = 0
        for scores in scores_list:
            value = scores[year_ix][1]
            if value and value != "?":
                counter += 1
                year_avg += float(value)

        value_for_year = None if counter == 0 else year_avg / float(counter)
        averaged_scores.append((years_list[year_ix], value_for_year))

    return averaged_scores

if __name__ == "__main__":
    counter = 0
    problem_dict = {}
    for (dirpath, dirnames, filenames) in os.walk("Problems"):
        if not dirnames:
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                problem = TPTP_Problem(filepath)
                if not problem.valid:
                    continue
                if problem.problem_class not in problem_dict:
                    problem_dict[problem.problem_class] = {}
                problem_dict[problem.problem_class][filename] = problem.scores
        counter += 1
        if counter > 6:
            break

    # Hierarchical Averaging
    # averages = get_averages(problem_dict)
    # print(get_averages_all_classes(averages))

    # Equal Averaging
    all_scores = []
    for problems in problem_dict.values():
        for scores in problems.values():
            all_scores.append(scores)
    print(get_total_averages(all_scores))