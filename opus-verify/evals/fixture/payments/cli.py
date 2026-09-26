import argparse


def main(argv=None):
    p = argparse.ArgumentParser(prog="payments")
    p.add_argument("amount", type=int)
    p.add_argument("--currency", default="eur")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args(argv)
