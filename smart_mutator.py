import argparse
from xeger import Xeger

# https://bitbucket.org/leapfrogdevelopment/rstr/src/default/

# This is just an PoC for a new kind of Mutator based Xeger!


def main(samples):
    x = Xeger(limit=30)

    topic_regex = r'(([0-9a-zA-Z#*]{0,10})/)+'
    ip4_regex = r'([0-9]{1,3}\.){3}[0-9]{1,3}'
    url_regex = r'((http|https|ftp|tcp|mqtt)):\/\/(www\.)?((\w){1,10}\.){1,3}(com|org|net|de)'
    non_alphanum_regex = r'[^a-zA-Z\d\s:]+'

    print('#### Generate {} random MQTT Topics ####'.format(samples))
    print('#####> Template: >| {} |<'.format(topic_regex))
    for i in range(samples):
        topic = x.xeger(topic_regex)
        print('[{}]: {}'.format(i, topic))

    print('\n#### Generate {} random IPv4 Addresses ####'.format(samples))
    print('#####> Template: >| {} |<'.format(ip4_regex))
    for i in range(samples):
        addr = x.xeger(ip4_regex)
        print('[{}]: {}'.format(i, addr))

    print('\n#### Generate {} random URLs ####'.format(samples))
    print('#####> Template: >| {} |<'.format(url_regex))
    for i in range(samples):
        urls = x.xeger(url_regex)
        print('[{}]: {}'.format(i, urls))

    print('\n#### Generate {} random non alphanumeric strings ####'.format(samples))
    print('#####> Template: >| {} |<'.format(non_alphanum_regex))
    for i in range(samples):
        non_alphanum = x.xeger(non_alphanum_regex)
        print('[{}]: {}'.format(i, non_alphanum))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple samples', add_help=False)
    parser.add_argument('-s', default=10, dest='samples', required=False, type=int)
    args = parser.parse_args()

    main(args.samples)
