'''
Test for correct sqlalchemy version
'''
import sqlalchemy


SQLALCHEMY_TUTORIAL_VERSION = "1.4.0"


def test_sqlalchemy_version():
    ''' Use an assertion to check the output of pd.__version__ '''
    assert sqlalchemy.__version__ in [SQLALCHEMY_TUTORIAL_VERSION]


if __name__ == "__main__":
    test_sqlalchemy_version()
    print("Sqlalchemy version is correct!")
