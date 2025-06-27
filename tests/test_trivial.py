#this is a dummy test for checking unit test system

#NEED to run to set up testing
#pip install pytest-cov
#python3 -m venv .venv
#source .venv/bin/activate
#pip install -r requirements.txt
#brew tap mongodb/brew
#brew install mongodb-community
#brew services start mongodb-community
#deactivate

#then we can start testing
#first, activate your virtual environment: source .venv/bin/activate
#then, run: pytest 
#or if you want to see printed output from your tests: pytest -s

from justinsight.tasks import bbcLogger_task


def test_add():
    assert 1 + 1 == 2

def test_bbcCheck():
    bbcLogger_task()
