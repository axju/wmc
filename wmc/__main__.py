"""Only the entry point for the python command"""
import sys
from wmc.utils import Dispatch


if __name__ == '__main__':
    Dispatch().main(sys.argv[1:])
