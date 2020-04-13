import argparse
import objects
import groups
import services
import access_rules

def add_objects():
    print 'inside function objects'
    objects.add()

def add_groups():
    print 'inside function add_groups'
    groups.add()

def add_services():
    print 'inside function add_services'
    services.add()

def add_access_rules():
    print 'inside function add_access_rules'
    access_rules.add()

def main():
    parser = argparse.ArgumentParser(description='Create dummy rules.')

    subparser = parser.add_subparsers(help='Different objects that can be added automatically')

    parser_objects = subparser.add_parser('objects', help='STEP 1: Add objects of host and network type')
    parser_objects.set_defaults(func=add_objects)

    parser_groups = subparser.add_parser('groups', help='STEP 2: Add groups of objects that should be added beforehand')
    parser_groups.set_defaults(func=add_groups)

    parser_service = subparser.add_parser('services', help='STEP 3: Add services of TCP type')
    parser_service.set_defaults(func=add_services)

    parser_rules = subparser.add_parser('access-rule', help='STEP 4: Add access rules for services that should be added previously')
    parser_rules.set_defaults(func=add_access_rules)

    args = parser.parse_args()

    args.func()

if __name__ == '__main__':
    main()
