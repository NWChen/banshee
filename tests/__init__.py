import argparse, os, sys
import time

def run_tests(target, params):
    start = time.time() 
    if len(params) > 0:
        params = params.join(' ')
    os.system('python %s %s' % (target, params))
    end = time.time()
    print('%s ran in %f seconds.\n' % (target, end-start))

if __name__ == '__main__':
    args = sys.argv
    target, params = args[1], []
    if len(args) > 2:
        params = args[2:]
    run_tests(target, params)
