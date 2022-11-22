import app

def test_one_line_valid(capsys):
    test_app = app.CLIManager(['-t', 'https://www.google.com/'])
    test_app.run()

    captured = capsys.readouterr()
    assert captured.out == 'The URL https://www.google.com/ is valid\n'
    assert captured.err == ''

def test_one_line_invalid(capsys):
    test_app = app.CLIManager(['-t', 'sample'])
    test_app.run()

    captured = capsys.readouterr()
    assert captured.out == 'The line sample is invalid URL\n'
    assert captured.err == ''

def test_sample_txt(capsys):
    test_app = app.CLIManager(['-f', 'sample.txt'])
    test_app.run()

    captured = capsys.readouterr()
    assert captured.out == '{\n  "https://www.youtube.com/": {\n    "GET": 200,\n    "HEAD": 200\n  }\n}\n'
    assert captured.err == ''

def test_sample2_txt(capsys):
    test_app = app.CLIManager(['-f', 'sample2.txt'])
    test_app.run()

    captured = capsys.readouterr()
    assert captured.out == 'Line 1 is not a URL\n{\n  "https://www.youtube.com/": {\n    "GET": 200,\n    "HEAD": 200\n  }\n}\n'
    assert captured.err == ''

def test_no_such_file(capsys):
    test_app = app.CLIManager(['-f', 'wrong.txt'])
    test_app.run()

    captured = capsys.readouterr()
    assert captured.out == 'No such file or directory\n'
    assert captured.err == ''


