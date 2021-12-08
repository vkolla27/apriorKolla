

## Modules used
import itertools
from flask import Flask, flash, redirect, render_template, request, url_for

# This function generates the first candidate set using the dataset
def generation_of_C1(data_set):
    product_dict = {}
    return_set = []
    for data in data_set:
        for product in data:
            if product not in product_dict:
               product_dict[product] = 1
            else:
                 product_dict[product] = product_dict[product] + 1
    for key in product_dict:
        tempArray = []
        tempArray.append(key)
        return_set.append(tempArray)
        return_set.append(product_dict[key])
        tempArray = []
    return return_set

def generation_of_frequentitems(candidate_list, number_of_transactions, minimum_support, data_set, father_frequent_array):
    freqent_items_list = []
    for i in range(len(candidate_list)):
        if i%2 != 0:
            support = (candidate_list[i] * 1.0 / number_of_transactions) * 100.0
            if support >= minimum_support:
                freqent_items_list.append(candidate_list[i-1])
                freqent_items_list.append(candidate_list[i])
            else:
                eliminated_items_list.append(candidate_list[i-1])

    for k in freqent_items_list:
        father_frequent_array.append(k)

    if len(freqent_items_list) == 2 or len(freqent_items_list) == 0:
        return_list = father_frequent_array
        return return_list
    else:
        generation_of_candidate_sets(data_set, eliminated_items_list, freqent_items_list, number_of_transactions, minimum_support)

#   This function creates Candidate sets by taking frequent sets as the input
#   At the end, this function calls generation_of_frequentitemss by feeding the output of the
#   crrent function as the input of the other function

def generation_of_candidate_sets(data_set, eliminated_items_list, freqent_items_list, number_of_transactions, minimum_support):
    elements_only = []
    list_after_combinations = []
    candidate_set_list = []
    for i in range(len(freqent_items_list)):
        if i%2 == 0:
            elements_only.append(freqent_items_list[i])
    for item in elements_only:
        temp_combination_list = []
        k = elements_only.index(item)
        for i in range(k + 1, len(elements_only)):
            for j in item:
                if j not in temp_combination_list:
                    temp_combination_list.append(j)
            for m in elements_only[i]:
                if m not in temp_combination_list:
                    temp_combination_list.append(m)
            list_after_combinations.append(temp_combination_list)
            temp_combination_list = []
    sorted_combination_list = []
    unique_combination_list = []
    for i in list_after_combinations:
        sorted_combination_list.append(sorted(i))
    for i in sorted_combination_list:
        if i not in unique_combination_list:
            unique_combination_list.append(i)
    list_after_combinations = unique_combination_list
    for item in list_after_combinations:
        count = 0
        for transaction in data_set:
            if set(item).issubset(set(transaction)):
                count = count + 1
        if count != 0:
            candidate_set_list.append(item)
            candidate_set_list.append(count)
    generation_of_frequentitems(candidate_set_list, number_of_transactions, minimum_support, data_set, father_frequent_array)

#   This function takes all the frequent sets as the input and generates Association Rules
def generation_of_assocaitation_rule(freqSet):
    association_rule = []
    for item in freqSet:
        if isinstance(item, list):
            if len(item) != 0:
                length = len(item) - 1
                while length > 0:
                    combinations = list(itertools.combinations(item, length))
                    temp = []
                    LHS = []
                    for RHS in combinations:
                        LHS = set(item) - set(RHS)
                        temp.append(list(LHS))
                        temp.append(list(RHS))
                        association_rule.append(temp)
                        temp = []
                    length = length - 1
    return association_rule

def apriori_result(rules, data_set, minimum_support, minimum_confidence,number_of_transactions):
    return_apriori_output = []
    for rule in rules:
        supportOfX = 0
        supportOfXinPercentage = 0
        supportOfXandY = 0
        supportOfXandYinPercentage = 0
        for transaction in data_set:
            if set(rule[0]).issubset(set(transaction)):
                supportOfX = supportOfX + 1
            if set(rule[0] + rule[1]).issubset(set(transaction)):
                supportOfXandY = supportOfXandY + 1
        try:
            supportOfXinPercentage = (supportOfX * 1/ number_of_transactions) * 100
        except ZeroDivisionError:
            supportOfXinPercentage = 0
        try:
            supportOfXandYinPercentage = (supportOfXandY * 1 / number_of_transactions) * 100
        except ZeroDivisionError:
            supportOfXandYinPercentage = 0
        try:
            confidence = (supportOfXandYinPercentage / supportOfXinPercentage) * 100
        except ZeroDivisionError:
            confidence = 0
        if confidence >= minimum_confidence:
            supportOfXAppendString = "Support Of X: " + str(round(supportOfXinPercentage, 2))
            supportOfXandYAppendString = "Support of X & Y: " + str(round(supportOfXandYinPercentage))
            confidenceAppendString = "Confidence: " + str(round(confidence))
            return_apriori_output.append(supportOfXAppendString)
            return_apriori_output.append(supportOfXandYAppendString)
            return_apriori_output.append(confidenceAppendString)
            return_apriori_output.append(rule)
    return return_apriori_output

if __name__ == '__main__':
    input_dataset = []
    eliminated_items_list = []
    number_of_transactions = 0
    father_frequent_array = []
    ### Flask Programming ####
    app = Flask(__name__)
    @app.route('/')
    def index():
        return render_template('input.html',data=[{'name': '1000-out1.csv'}, {'name': '5000-out1.csv'}, {'name': '20000-out1.csv'},{'name': '75000-out1.csv'}])

    @app.route("/result", methods=['GET', 'POST'])
    def result():
        file_name = request.form.get('comp_select')
        min_sup = request.form.get('min_value')
        min_conf = request.form.get('min_conf')
        ## Reading the input files line by line and spliting with comma and storing in dataset
        with open(file_name,'r') as fp:
            lines = fp.readlines()

        for line in lines:
            line = line.rstrip()
            input_dataset.append(line.split(","))

        number_of_transactions = len(input_dataset)
        print(number_of_transactions)
        first_candidate_set = generation_of_C1(input_dataset)
        frequent_item_set = generation_of_frequentitems(first_candidate_set, number_of_transactions, int(min_sup), input_dataset, father_frequent_array)
        association_rules = generation_of_assocaitation_rule(father_frequent_array)
        apriori_output = apriori_result(association_rules, input_dataset, int(min_sup), int(min_conf),number_of_transactions)
        final_data = []
        counter = 1
        if len(apriori_output) == 0:
            print("There are no association rules for this support and confidence.")
        else:
            for i in apriori_output:
                if counter == 4:
                    ha =str(i[0]) + "------>" + str(i[1])
                    final_data.append(ha)
                    final_data.append("---------------------------")
                    print("")
                    counter = 0
                else:
                    final_data.append(str(i))
                counter = counter + 1
        return render_template('output.html', your_list=final_data)
    app.run(host='localhost', port=8080, debug=False)