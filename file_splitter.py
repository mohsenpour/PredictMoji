'''
script to split the training file into three portions for each team member use
'''
if __name__ == "__main__":
    line_count =0
    with open('full_train_plaintext.txt', 'r') as training_file:
        for line in training_file:
            line_count+=1
    first = int(line_count/ 3)
    second = 2 * first
    with open('full_train_plaintext.txt', 'r') as training_file:
        with open("Mo.txt",'w') as mo_file:
            for line_index, line in enumerate(training_file):
                if line_index <= first:
                    mo_file.write(line)

    with open('full_train_plaintext.txt', 'r') as training_file:
        with open("Assad.txt",'w') as assad_file:
            for line_index, line in enumerate(training_file):
                if line_index > first and line_index <= second:
                    assad_file.write(line)

    with open('full_train_plaintext.txt', 'r') as training_file:
        with open("Rohit.txt",'w') as rohit_file:
            for line_index, line in enumerate(training_file):
                if line_index > second:
                    rohit_file.write(line)
