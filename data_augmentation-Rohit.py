import pandas


def get_data():
    header = ['tweet', 'label']
    data_set = pandas.read_csv('cleaned_data.txt', delimiter='\t', names=header)
    return data_set


def get_data_set():
    return global_data_set


if __name__ == '__main__':
    data_set = get_data()
    # mapping = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    num_classes = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    copies = {0: 1, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for label in data_set['label']:
        num_classes[label] += 1

    with open('cleaned_data.txt', 'r') as clean_data_file:
        with open('augmented_data.txt', 'a') as augmented_data_file:
            for line in clean_data_file:
                whole_line = line.split(sep='\t')
                label = whole_line[-1].replace('\n', '')
                label = int(label)
                tweet = whole_line[0]
                num_copies = int(num_classes[0] / num_classes[label])
                for i in range(num_copies):
                    augmented_data_file.write(tweet + '\t' + str(label) + "\n")


    print(num_classes)