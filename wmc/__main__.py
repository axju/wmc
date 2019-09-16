import sys
from wmc.cli import  dispatch


if __name__ == '__main__':
    dispatch(sys.argv[1:])
