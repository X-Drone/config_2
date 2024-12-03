import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import subprocess
import os
import sys

from main import *


class TestGitFunctions(unittest.TestCase):

    @patch('subprocess.run')
    def test_run_git_command_success(self, mock_run):
        # Мокаем успешный результат выполнения команды
        mock_run.return_value = MagicMock(returncode=0, stdout="commit_hash", stderr="")
        result = run_git_command(['git', 'log'], '/mock/repo/path')
        self.assertEqual(result, "commit_hash")

    @patch('subprocess.run')
    def test_run_git_command_failure(self, mock_run):
        # Мокаем ошибку выполнения команды
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="error occurred")
        with self.assertRaises(Exception):
            run_git_command(['git', 'log'], '/mock/repo/path')

    @patch('subprocess.run')
    def test_get_commit_history(self, mock_run):
        # Мокаем историю коммитов
        mock_run.return_value = MagicMock(returncode=0, stdout="commit1\ncommit2\n", stderr="")
        commits = get_commit_history('v1.0', '/mock/repo/path')
        self.assertEqual(commits, ['commit1', 'commit2'])

    @patch('subprocess.run')
    def test_get_files_changed_between_commits(self, mock_run):
        # Мокаем измененные файлы между коммитами
        mock_run.return_value = MagicMock(returncode=0, stdout="file1.txt\nfile2.txt\n", stderr="")
        changed_files = get_files_changed_between_commits('commit_from', 'commit_to', '/mock/repo/path')
        self.assertEqual(changed_files, ['file1.txt', 'file2.txt'])

    def test_generate_mermaid_graph(self):
        # Тестируем генерацию графа Mermaid
        dependencies = {
            'commit1': ['file1.txt', 'file2.txt'],
            'commit2': ['file3.txt']
        }
        expected_output = '''graph TD
    commit1 --> file1.txt
    commit1 --> file2.txt
    commit2 --> file3.txt
'''
        graph_code = generate_mermaid_graph(dependencies)
        self.assertEqual(graph_code, expected_output)

    @patch('subprocess.run')
    def test_main(self, mock_run):
        # Мокаем весь основной процесс
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="commit1\ncommit2\n", stderr=""),  # Для get_commit_history
            MagicMock(returncode=0, stdout="file1.txt\nfile2.txt\n", stderr=""),  # Для get_files_changed_between_commits
        ]

        # Патчим open, чтобы проверить сохранение в файл
        with patch('builtins.open', new_callable=MagicMock) as mock_open:
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()  # Запуск main функции
                mock_open.assert_called_once_with('output.txt', 'w')
                self.assertIn("graph TD", mock_stdout.getvalue())  # Проверяем, что граф выводится

if __name__ == '__main__':
    unittest.main()
