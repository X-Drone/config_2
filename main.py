import os
import subprocess
#import json


def run_git_command(command, repo_path):
    """ Выполняет команду git в указанном репозитории """
    result = subprocess.run(command, cwd=repo_path, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Git command failed: {result.stderr}")
    return result.stdout


def get_commit_history(tag_name, repo_path):
    """ Получает историю коммитов до указанного тега """
    command = ['git', 'log', '--pretty=format:%H', tag_name]
    commit_history = run_git_command(command, repo_path)
    commits = commit_history.splitlines()
    return commits


def get_files_changed_between_commits(commit_from, commit_to, repo_path):
    """ Получает список измененных файлов между двумя коммитами """
    command = ['git', 'diff', '--name-only', commit_from, commit_to]
    changed_files = run_git_command(command, repo_path)
    return changed_files.splitlines()


def build_dependency_graph(tag_name, repo_path):
    """ Строит граф зависимостей для тегов """
    commits = get_commit_history(tag_name, repo_path)
    dependencies = {}

    for i in range(len(commits) - 1):
        commit_from = commits[i + 1]
        commit_to = commits[i]
        changed_files = get_files_changed_between_commits(commit_from, commit_to, repo_path)
        dependencies[commit_to] = changed_files

    return dependencies


def generate_mermaid_graph(dependencies):
    """ Генерирует граф Mermaid для отображения зависимостей """
    mermaid_code = 'graph TD\n'

    for commit, files in dependencies.items():
        for file in files:
            mermaid_code += f'    {commit} --> {file}\n'

    return mermaid_code


def save_graph_to_file(graph_code, output_file):
    """ Сохраняет граф Mermaid в файл """
    with open(output_file, 'w') as f:
        f.write(graph_code)


def main():
    repo_path = "C:/Users/nicks/source/repos/AI_vision"
    tag_name = "master"
    output_file = "output.txt"

    if not all([repo_path, tag_name, output_file]):
        print("Ошибка: Отсутствуют необходимые параметры в конфигурации.")
        return

    # Строим граф зависимостей
    dependencies = build_dependency_graph(tag_name, repo_path)

    # Генерируем код графа Mermaid
    graph_code = generate_mermaid_graph(dependencies)

    # Сохраняем результат в файл
    save_graph_to_file(graph_code, output_file)

    # Выводим граф на экран
    print(graph_code)


if __name__ == '__main__':
    main()
