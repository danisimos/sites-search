import os
import re

import pymorphy2

from task2tokenize import get_tokens_from_file


def parse_lemmas_from_file(file_path):
    lemmas_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if (len(line) > 0):

                lemma, tokens_str = line.strip().split(': ')
                tokens = tokens_str.split(', ')
                for token in tokens:
                    lemmas_dict[token] = tokens[0]

    return lemmas_dict


def create_html_index(html_files_dir, lemmas_dir):
    index = {}
    for doc_i in range(1, 100):
        file_path = os.path.join(html_files_dir, f'{doc_i}.html')

        words = get_tokens_from_file(file_path)
        print(f'page #{doc_i}, words in page: {len(words)}')
        for word in words:
            lemma = lemmas_dir.get(word)
            if lemma:
                if lemma not in index:
                    index[lemma] = {'count': 0, 'inverted_array': []}
                if doc_i not in index[lemma]['inverted_array']:
                    index[lemma]['inverted_array'].append(doc_i)
                    index[lemma]['count'] += 1

    return index


def write_index_to_file(index, index_file_name):
    with open(index_file_name, 'w', encoding='utf-8') as file:
        for key, value in index.items():
            count = value['count']
            array = value['inverted_array']
            file.write(f'{{"word":"{key}", "count":{count},"inverted_array":{array}}}\n')


def write_index_list_to_file(index, index_file_name):
    with open(index_file_name, 'w', encoding='utf-8') as file:
        for key, value in index.items():
            count = value['count']
            array = value['inverted_array']
            array = ', '.join(map(str, array))
            file.write(f'{key}:{array}\n')


def build_index(index_file_name, html_dir, lemma_file_name, index_list_name):
    lemmas_dir = parse_lemmas_from_file(lemma_file_name)
    index = create_html_index(html_dir, lemmas_dir)
    write_index_to_file(index, index_file_name)
    write_index_list_to_file(index, index_list_name)


def read_data_from_file(filename):
    inverted_index = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            lemma, file_number = line.strip().split(':')
            file_number = file_number.strip().split(', ')
            inverted_index[lemma] = set(file_number)

    return inverted_index


def evaluate_expression(expression, inverted_index):
    morph = pymorphy2.MorphAnalyzer()
    stack = []
    operator_stack = []
    tokens = re.findall(r'\(|\)|\w+|[^\s\w]', expression)
    tokens = list(filter(None, tokens))

    for token in tokens:
        if token in ["AND", "OR", "NOT", "(", ")"]:
            if token == "(":
                operator_stack.append(token)
            elif token == ")":
                while operator_stack and operator_stack[-1] != "(":
                    apply_operator(operator_stack.pop(), stack, inverted_index)
                operator_stack.pop()
            else:
                operator = token
                if operator_stack and precedence(operator) <= precedence(operator_stack[-1]):
                    apply_operator(operator_stack.pop(), stack, inverted_index)
                operator_stack.append(token)
        else:
            token = morph.parse(token)[0].normal_form
            if token in inverted_index:
                stack.append(inverted_index[token])
            else:
                stack.append({'0'})

    while operator_stack:
        apply_operator(operator_stack.pop(), stack, inverted_index)

    return sorted(stack[-1], key=int)


def apply_operator(operator, stack, inverted_index):
    if operator == "AND":
        operand2 = stack.pop()
        operand1 = stack.pop()
        stack.append(operand1.intersection(operand2))
    elif operator == "OR":
        operand2 = stack.pop()
        operand1 = stack.pop()
        stack.append(operand1.union(operand2))
    elif operator == "NOT":
        operand2 = stack.pop()
        operand1 = stack.pop()
        stack.append(operand1.difference(operand2))


def precedence(operator):
    if operator == "NOT":
        return 3
    elif operator == "AND":
        return 2
    elif operator == "OR":
        return 1
    else:
        return 0


def boolean_search(query, inverted_index):
    result = evaluate_expression(query, inverted_index)
    return result


def search():
    filename = 'inverted_index_tokens.txt'
    inverted_index = read_data_from_file(filename)

    query = input("Введите запрос: ")
    result = boolean_search(query, inverted_index)

    with open('index.txt', 'r') as file:
        links = file.read().splitlines()
    if result and not (len(result) == 1 and result[0] == '0'):
        print(f"Найденные страницы, содержащие запрос '{query}':")
        for item in result:
            if item != '0':
                print(links[int(item) - 1])
    else:
        print("Ничего не найдено.")


index_file_name = 'inverted_index.txt'
index_list_file_name = 'inverted_index_tokens.txt'
lemma_file_name = 'task2_result/lemmas.txt'
html_dir = 'выкачка'


def main():
    build_index(index_file_name, html_dir, lemma_file_name, index_list_file_name)

    while True:
        search()


if __name__ == "__main__":
    main()
