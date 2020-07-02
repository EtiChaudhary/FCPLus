import RunCV
import csv, operator


################################
# Combine the best features groups.
#
################################

# This is the index of the column of the result we are comparing in the results file.
ACCURACY_INDEX = 5
MAP_INDEX = 9

# To change whether runs should be sorted by accuracy or MAP, change the values below:
RESULT_SCORE_INDEX = ACCURACY_INDEX
RUN_PREFIX = 'TOP_'

SET_NAME = 'dev+test'
RESULTS_FILE = "../../../data/results/results-answers-cross-validation-"+SET_NAME+".tsv"

TOP_N_FROM = 2
TOP_N_TO = 40

def main():
    # 1. Read the results file and sort the scores (only the single feature groups: -incl)
    # 2. combine the features from the feature group
    best_results = read_best_results()

    max_index = min(TOP_N_TO, len(best_results))

    # for group_score in best_results:
    #     group = group_score[0]
    #     score = group_score[1]

    groups_names = []
    # groups_names_str = ''
    groups_names_str = 'USER_EXPERTISE, ' + 'ANSWER_QUALITY, ' + 'READABILITY, '
    for i in range(0, max_index):
        n = i+1
        index_name = RUN_PREFIX+str(n)
        groups_names.append(best_results[i][0])
        if groups_names_str != '':
            groups_names_str += ', '    
        groups_names_str += best_results[i][0]

        if n >= TOP_N_FROM:
            run_id = index_name + ' ('+groups_names_str + ')'
            print('!!! Running...', run_id)
            RunCV.run(run_id, groups_names)


def read_best_results():
    group_scores = {}
    with open(RESULTS_FILE,encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        for row in csvreader:
            group = row[0]
            score = row[RESULT_SCORE_INDEX]
            if (group.endswith('-incl')):
                group_scores[group] = score
                

    print('BEFORE SORT:', group_scores)
    sorted_group_scores = sorted(group_scores.items(), key=operator.itemgetter(1), reverse=True)

    print('AFTER SORT:', sorted_group_scores)                
    return sorted_group_scores


# Start here:
main()