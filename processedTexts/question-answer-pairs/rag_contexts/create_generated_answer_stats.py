import json
import os
import statistics
import math

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f'Current working directory: {os.getcwd()}')

current_dir = '.'

# print(os.path.isdir(os.path.join(current_dir,'output_Donald','Recursive')))

# print(os.path.basename(os.path.join(current_dir,'output_Donald','Recursive')))

#statistics needed: avg, std similarity per file, per case, per technique

def create_statistics(dir_names=['output_Donald','output_FBI','output_USA']):

    def calculate_root_mean_square_dev(data):
        squared_diffs = [(x - 1) ** 2 for x in data]
        mean_squared_diff = statistics.mean(squared_diffs)
        return math.sqrt(mean_squared_diff)
    
    def calculate_mean_deviation_from_1(data):
        total_deviation = 0
        for value in data:
            total_deviation += abs(1 - value)  
        mean_deviation = total_deviation / len(data) 
        return mean_deviation



    def add_stats_to_obj(output_obj, data):
        output_obj['Average'] = statistics.mean(data)
        output_obj['StandardDeviation'] = statistics.stdev(data)
        output_obj['Min'] = min(data)
        output_obj['Max'] = max(data)
        output_obj['Median'] = statistics.median(data)
        output_obj['Data'] = data

    
    def add_deviations(output_obj, data):
        output_obj['rmsd'] = calculate_root_mean_square_dev(data)
        output_obj['mean_deviation_from_1'] = calculate_mean_deviation_from_1(data)


    current_dir = '.'
    output = {}

    output['Recursive'] = {}
    output['Semantic'] = {}
    output['Token'] = {}


    sub_folders = ['Recursive','Semantic','Token']
    recursive_cosine_similarity_list = []
    semantic_cosine_similarity_list = []
    token_cosine_similarity_list = []

    for dir in dir_names:
        output[dir] = {}
        output[dir]['Cumulative'] = {}
        dir_cosine_sim = []

        for folder in sub_folders:

            output[dir][folder] = {}

            with open(os.path.join(current_dir,dir,folder,'generated_answer.json'),'r') as file:
                data = json.load(file)
                per_file_similarity = [entry['cosine_similarity'] for entry in data]

                add_stats_to_obj(output[dir][folder], per_file_similarity)

                dir_cosine_sim = dir_cosine_sim + per_file_similarity

                if(folder == 'Recursive'):
                    recursive_cosine_similarity_list = recursive_cosine_similarity_list + per_file_similarity
                if(folder == 'Semantic'):
                    semantic_cosine_similarity_list = semantic_cosine_similarity_list + per_file_similarity
                if(folder == 'Token'):
                    token_cosine_similarity_list = token_cosine_similarity_list + per_file_similarity


        add_stats_to_obj(output[dir]['Cumulative'],dir_cosine_sim)

    print(len(recursive_cosine_similarity_list))
    add_stats_to_obj(output['Recursive'],recursive_cosine_similarity_list)
    add_deviations(output['Recursive'],recursive_cosine_similarity_list)

    print(len(semantic_cosine_similarity_list))
    add_stats_to_obj(output['Semantic'], semantic_cosine_similarity_list)
    add_deviations(output['Semantic'], semantic_cosine_similarity_list)

    print(len(token_cosine_similarity_list))
    add_stats_to_obj(output['Token'],token_cosine_similarity_list)
    add_deviations(output['Token'],token_cosine_similarity_list)

    with open(os.path.join(current_dir,'cumulative_statistics.json'),'w') as file:
        json.dump(output,file,indent=4)



create_statistics()










