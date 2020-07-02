import Features

# Read multiple sets
def read_feature_sets(set_name, feat_indeces):
    features_map = {}    
    for feat_index in feat_indeces:
        features_from_index = read_feature_set(set_name, feat_index)
        features_map = Features.add_features(features_map, features_from_index) 
    return features_map

def read_feature_set(set_name, feat_index):
    features_map = {}

    # Baseline_Castillo_2011
    if feat_index == 'Baseline_Castillo_2011':
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
    
    if feat_index == 'USER_EXPERTISE':
        features_map = Features.add_features(features_map, Features.features_USER_EXPERTISE(set_name))
        features_map = Features.add_features(features_map, Features.features_USER_LEXICAL_ANALYSIS(set_name))
    
    if feat_index == 'ANSWER_QUALITY':
        features_map = Features.add_features(features_map, Features.features_ANSWER_QUALITY(set_name))

    if feat_index == 'READABILITY':
        features_map = Features.add_features(features_map, Features.features_READABILITY(set_name))

    if feat_index == 'CATEGORIES-incl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
    if feat_index == 'QUALITY-incl':
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
    if feat_index == 'TROLLNESS-incl':
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
    if feat_index == 'ACTIVITY-incl':
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
    if feat_index == 'CREDIBILITY-incl':
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
    if feat_index == 'SENTIMENT-incl':
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
    if feat_index == 'GOOGLE_VEC-incl':
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
    if feat_index == 'QL_VEC-incl':
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
    if feat_index == 'SYNTAX_VEC-incl':
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
    if feat_index == 'RANK_SAME_USER-incl':
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
    if feat_index == 'VEC_COSINES_THREAD-incl':
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
    if feat_index == 'COSINES-incl':
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))

    #linguistic Features
    if feat_index == 'LINGF_BIAS_LEX-incl':
        features_map = Features.add_features(features_map, Features.features_LINGF_BIAS_LEX(set_name))
    #linguistic Features
    if feat_index == 'LINGF_HEDGES-incl':
        features_map = Features.add_features(features_map, Features.features_LINGF_HEDGES(set_name))
    #linguistic Features
    if feat_index == 'LINGF_IMPLICATIVES-incl':
        features_map = Features.add_features(features_map, Features.features_LINGF_IMPLICATIVES(set_name))
    #linguistic Features
    if feat_index == 'LINGF_ASSERTIVES-incl':
        features_map = Features.add_features(features_map, Features.features_LINGF_ASSERTIVES(set_name))
    #linguistic Features
    if feat_index == 'LINGF_FACTIVES-incl':
        features_map = Features.add_features(features_map, Features.features_LINGF_FACTIVES(set_name))
    #linguistic Features
    if feat_index == 'LINGF_REPORT_VERBS-incl':
        features_map = Features.add_features(features_map, Features.features_LINGF_REPORT_VERBS(set_name))
    #linguistic Features
    if feat_index == 'LINGF_All_BIAS_LEX-incl':
        # features_map = Features.add_features(features_map, Features.features_LINGF_All_BIAS_LEX(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_BIAS_LEX(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_HEDGES(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_IMPLICATIVES(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_ASSERTIVES(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_FACTIVES(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_REPORT_VERBS(set_name))
    #linguistic Features
    if feat_index == 'LINGF_STRONGSubj-incl':
        features_map = Features.add_features(features_map, Features.features_LINGF_STRONGSubj(set_name))
    #linguistic Features
    if feat_index == 'LINGF_WEAKSubj-incl':
        features_map = Features.add_features(features_map, Features.features_LINGF_WEAKSubj(set_name))
    #linguistic Features
    if feat_index == 'LINGF_NEGATIVES-incl':
        features_map = Features.add_features(features_map, Features.features_LINGF_NEGATIVES(set_name))
    #linguistic Features
    if feat_index == 'LINGF_POSITIVES-incl':
        features_map = Features.add_features(features_map, Features.features_LINGF_POSITIVES(set_name))
    #linguistic Features
    if feat_index == 'LINGF_MODALS-incl':
        features_map = Features.add_features(features_map, Features.features_LINGF_MODALS(set_name))
    #linguistic Features
    if feat_index == 'LINGF_NEGATIONS-incl':
        features_map = Features.add_features(features_map, Features.features_LINGF_NEGATIONS(set_name))
    #linguistic Features
    if feat_index == 'LINGF_All-incl':
        # features_map = Features.add_features(features_map, Features.features_LINGF_All(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_BIAS_LEX(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_HEDGES(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_IMPLICATIVES(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_ASSERTIVES(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_FACTIVES(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_REPORT_VERBS(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_STRONGSubj(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_WEAKSubj(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_NEGATIVES(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_POSITIVES(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_MODALS(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_NEGATIONS(set_name))
    #linguistic Features
    if feat_index == 'EXTENDED_LINGF_All-incl':
        # features_map = Features.add_features(features_map, Features.features_LINGF_All(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_BIAS_LEX(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_HEDGES(set_name))
        # features_map = Features.add_features(features_map, Features.features_LINGF_IMPLICATIVES(set_name))
        # features_map = Features.add_features(features_map, Features.features_LINGF_ASSERTIVES(set_name))
        # features_map = Features.add_features(features_map, Features.features_LINGF_FACTIVES(set_name))
        # features_map = Features.add_features(features_map, Features.features_LINGF_REPORT_VERBS(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_STRONGSubj(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_WEAKSubj(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_NEGATIVES(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_POSITIVES(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_MODALS(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_NEGATIONS(set_name))
        ###EXTENDED_LINGF_All-incl
        features_map = Features.add_features(features_map, Features.features_LINGF_EXTENDED_MULTIWORDS(set_name))

    #article supports
    if feat_index == 'ARTICLES_SUPPORTS_BESTMATCH-incl':
        features_map = Features.add_features(features_map, Features.features_ARTICLES_SUPPORTS_BESTMATCH(set_name))
    #article supports
    if feat_index == 'ARTICLES_SUPPORTS_BESTMATCH_LEVENSHTEIN-incl':
        features_map = Features.add_features(features_map, Features.features_ARTICLES_SUPPORTS_BESTMATCH(set_name))
        features_map = Features.add_features(features_map, Features.features_ARTICLES_SUPPORTS_BESTMATCH_LEVENSHTEIN(set_name))
    #article supports
    if feat_index == 'ARTICLES_SUPPORTS_QUERY_LEVENSHTEIN-incl':
        features_map = Features.add_features(features_map, Features.features_ARTICLES_SUPPORTS_QUERY(set_name))
        features_map = Features.add_features(features_map, Features.features_ARTICLES_SUPPORTS_QUERY_LEVENSHTEIN(set_name))
    #article supports
    if feat_index == 'ARTICLES_SUPPORTS_ENTIREC-incl':
        features_map = Features.add_features(features_map, Features.features_ARTICLES_SUPPORTS_ENTIREC(set_name))
    #article supports
    if feat_index == 'ARTICLES_SUPPORTS_ENTIREC_LEVENSHTEIN-incl':
        features_map = Features.add_features(features_map, Features.features_ARTICLES_SUPPORTS_ENTIREC(set_name))
        features_map = Features.add_features(features_map, Features.features_ARTICLES_SUPPORTS_ENTIREC_LEVENSHTEIN(set_name))
    #article supports
    if feat_index == 'ARTICLES_SUPPORTS_All-incl':
        features_map = Features.add_features(features_map, Features.features_ARTICLES_SUPPORTS_BESTMATCH(set_name))
        features_map = Features.add_features(features_map, Features.features_ARTICLES_SUPPORTS_ENTIREC(set_name))
    #article supports
    if feat_index == 'ARTICLES_SUPPORTS_All_LEVENSHTEIN-incl':
        features_map = Features.add_features(features_map, Features.features_ARTICLES_SUPPORTS_BESTMATCH(set_name))
        features_map = Features.add_features(features_map, Features.features_ARTICLES_SUPPORTS_BESTMATCH_LEVENSHTEIN(set_name))
        features_map = Features.add_features(features_map, Features.features_ARTICLES_SUPPORTS_ENTIREC(set_name))
        features_map = Features.add_features(features_map, Features.features_ARTICLES_SUPPORTS_ENTIREC_LEVENSHTEIN(set_name))

    #IR Features
    if feat_index == 'IRF_Bing_snippets-incl':
        features_map = Features.add_features(features_map, Features.features_IR_Bing_snippets(set_name))

    if feat_index == 'IRF_Google_snippets-incl':
        features_map = Features.add_features(features_map, Features.features_IR_Google_snippets(set_name))

    if feat_index == 'IRF_ALL_snippets-incl':
        features_map = Features.add_features(features_map, Features.features_IR_Bing_snippets(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_Google_snippets(set_name))

    if feat_index == 'IRF_Bing_snippets_qataronly-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_snippets_qataronly(set_name))

    if feat_index == 'IRF_Google_snippets_qataronly-incl':
        features_map = Features.add_features(features_map, Features.features_IR_google_snippets_qataronly(set_name))

    if feat_index == 'IRF_ALL_snippets_qataronly-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_snippets_qataronly(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_snippets_qataronly(set_name))

    if feat_index == 'IRF_Bing_webpage_qataronly-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_qataronly(set_name))

    if feat_index == 'IRF_Google_webpage_qataronly-incl':
        features_map = Features.add_features(features_map, Features.features_IR_google_webpages_qataronly(set_name))

    if feat_index == 'IRF_ALL_webpages_qataronly-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_qataronly(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_webpages_qataronly(set_name))

    if feat_index == 'IRF_ALL_Google_qataronly-incl':
        features_map = Features.add_features(features_map, Features.features_IR_google_snippets_qataronly(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_webpages_qataronly(set_name))

    if feat_index == 'IRF_ALL-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_snippets_qataronly(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_qataronly(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_qataronly_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_webpages_qataronly_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_snippets_qatar_splited_others_bulk(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_webpages_qatar_splited_others_bulk(set_name))

    if feat_index == 'IRF_ALL_Bing_qataronly-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_snippets_qataronly(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_qataronly(set_name))

    if feat_index == 'IRF_ALL_qataronly-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_snippets_qataronly(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_qataronly(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_snippets_qataronly(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_webpages_qataronly(set_name))

    if feat_index == 'IRF_Bing_snippets_qataronly_splitted-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_snippets_qataronly_splited(set_name))

    if feat_index == 'IRF_Google_snippets_qataronly_splitted-incl':
        features_map = Features.add_features(features_map, Features.features_IR_google_snippets_qataronly_splited(set_name))

    if feat_index == 'IRF_ALL_snippets_qataronly_splitted-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_snippets_qataronly_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_snippets_qataronly_splited(set_name))

    if feat_index == 'IRF_Bing_webpage_qataronly_splitted-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_qataronly_splited(set_name))

    if feat_index == 'IRF_Google_webpage_qataronly_splitted-incl':
        features_map = Features.add_features(features_map, Features.features_IR_google_webpages_qataronly_splited(set_name))

    if feat_index == 'IRF_ALL_webpages_qataronly_splitted-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_qataronly_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_webpages_qataronly_splited(set_name))

    if feat_index == 'IRF_ALL_Google_qataronly_splitted-incl':
        features_map = Features.add_features(features_map, Features.features_IR_google_snippets_qataronly_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_webpages_qataronly_splited(set_name))

    if feat_index == 'IRF_ALL_Bing_qataronly_splitted-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_snippets_qataronly_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_qataronly_splited(set_name))

    if feat_index == 'IRF_ALL_qataronly_splitted-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_snippets_qataronly_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_qataronly_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_snippets_qataronly_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_webpages_qataronly_splited(set_name))

    if feat_index == 'IRF_Bing_snippets_qataronly_splitted_others_bulk-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_snippets_qatar_splited_others_bulk(set_name))

    if feat_index == 'IRF_Google_snippets_qataronly_splitted_others_bulk-incl':
        features_map = Features.add_features(features_map, Features.features_IR_google_snippets_qatar_splited_others_bulk(set_name))

    if feat_index == 'IRF_ALL_snippets_qataronly_splitted_others_bulk-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_snippets_qatar_splited_others_bulk(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_snippets_qatar_splited_others_bulk(set_name))

    if feat_index == 'IRF_Bing_webpage_qataronly_splitted_others_bulk-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_qatar_splited_others_bulk(set_name))

    if feat_index == 'IRF_Google_webpage_qataronly_splitted_others_bulk-incl':
        features_map = Features.add_features(features_map, Features.features_IR_google_webpages_qatar_splited_others_bulk(set_name))

    if feat_index == 'IRF_ALL_webpages_qataronly_splitted_others_bulk-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_qatar_splited_others_bulk(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_webpages_qatar_splited_others_bulk(set_name))

    if feat_index == 'IRF_ALL_Google_qataronly_splitted_others_bulk-incl':
        features_map = Features.add_features(features_map, Features.features_IR_google_snippets_qatar_splited_others_bulk(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_webpages_qatar_splited_others_bulk(set_name))

    if feat_index == 'IRF_ALL_Bing_qataronly_splitted_others_bulk-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_snippets_qatar_splited_others_bulk(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_qatar_splited_others_bulk(set_name))

    if feat_index == 'IRF_ALL_qataronly_splitted_others_bulk-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_snippets_qatar_splited_others_bulk(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_qatar_splited_others_bulk(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_snippets_qatar_splited_others_bulk(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_webpages_qatar_splited_others_bulk(set_name))

    if feat_index == 'IRF_Bing_snippets_splitted-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_snippets_splited(set_name))

    if feat_index == 'IRF_Google_snippets_splitted-incl':
        features_map = Features.add_features(features_map, Features.features_IR_google_snippets_splited(set_name))

    if feat_index == 'IRF_ALL_snippets_splitted-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_snippets_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_snippets_splited(set_name))

    if feat_index == 'IRF_Bing_webpage_splitted-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_splited(set_name))

    if feat_index == 'IRF_External_google_snippets-incl':
        features_map = Features.add_features(features_map, Features.features_IR_External(set_name))

    if feat_index == 'IRF_QL_only-incl':
        features_map = Features.add_features(features_map, Features.features_IR_QL_only(set_name))

    if feat_index == 'IRF_QL_only_reputed-incl':
        features_map = Features.add_features(features_map, Features.features_IR_QL_only_reputed(set_name))

    if feat_index == 'IRF_QL_only_split-incl':
        features_map = Features.add_features(features_map, Features.features_IR_QL_split(set_name))

    if feat_index == 'IRF_QL_only_withPages_reputed-incl':
        features_map = Features.add_features(features_map, Features.features_IR_QL_only_withPages_reputed(set_name))

    if feat_index == 'IRF_QL_only_withPages_split-incl':
        features_map = Features.add_features(features_map, Features.features_IR_QL_withPages_split(set_name))


    if feat_index == 'IRF_ALL_webpages_splitted-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_webpages_splited(set_name))

    if feat_index == 'IRF_ALL_Google_splitted-incl':
        features_map = Features.add_features(features_map, Features.features_IR_google_snippets_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_webpages_splited(set_name))

    if feat_index == 'IRF_ALL_Bing_splitted-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_snippets_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_splited(set_name))

    if feat_index == 'IRF_ALL_splitted-incl':
        features_map = Features.add_features(features_map, Features.features_IR_bing_snippets_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_webpages_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_snippets_splited(set_name))

    if feat_index == 'IRF_Best_combination':
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_qataronly_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_webpages_splited(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_bing_snippets_qataronly(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_bing_webpages_qataronly(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_snippets_qataronly(set_name))
        features_map = Features.add_features(features_map, Features.features_IR_google_webpages_qataronly(set_name))

    if feat_index == 'all':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_All(set_name)) #all linguistic Features
        features_map = Features.add_features(features_map, Features.features_IR_All_snippets(set_name)) # all IR features

    if feat_index == 'IRFeatures-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_All(set_name)) #all linguistic Features
        #features_map = Features.add_features(features_map, Features.features_IR_All_snippets(set_name)) # all IR features
    #linguistic Features
    if feat_index == 'LINGF_All_BIAS_ADDED_TO_OTHERS':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
        features_map = Features.add_features(features_map, Features.features_LINGF_All_BIAS_LEX(set_name)) #all linguistic Features

    #linguistic Features
    if feat_index == 'LINGF_All-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
        # features_map = Features.add_features(features_map, Features.features_LINGF_All(set_name)) #all linguistic Features

    if feat_index == 'CATEGORIES-excl':
        #features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'QUALITY-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        #features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'TROLLNESS-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        #features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'ACTIVITY-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        #features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'CREDIBILITY-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        #features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'SENTIMENT-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        #features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'GOOGLE_VEC-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        #features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'QL_VEC-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        #features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'SYNTAX_VEC-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        #features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'RANK_SAME_USER-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        #features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'VEC_COSINES_THREAD-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        #features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        features_map = Features.add_features(features_map, Features.features_COSINES(set_name))
    if feat_index == 'COSINES-excl':
        features_map = Features.add_features(features_map, Features.features_CATEGORIES(set_name))
        features_map = Features.add_features(features_map, Features.features_QUALITY(set_name))
        features_map = Features.add_features(features_map, Features.features_TROLLNESS(set_name))
        features_map = Features.add_features(features_map, Features.features_ACTIVITY(set_name))
        features_map = Features.add_features(features_map, Features.features_CREDIBILITY(set_name))
        features_map = Features.add_features(features_map, Features.features_SENTIMENT(set_name))
        features_map = Features.add_features(features_map, Features.features_GOOGLE_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_QL_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_SYNTAX_VEC(set_name))
        features_map = Features.add_features(features_map, Features.features_RANK_SAME_USER(set_name))
        features_map = Features.add_features(features_map, Features.features_VEC_COSINES_THREAD(set_name))
        #features_map = Features.add_features(features_map, Features.features_COSINES(set_name))

    return features_map
