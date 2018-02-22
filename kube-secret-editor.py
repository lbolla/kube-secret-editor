#!/usr/bin/env python3
import base64
import os
import subprocess
import sys

import yaml


EDITOR = os.environ.get('EDITOR', 'vi')


class NoDatesSafeLoader(yaml.SafeLoader):
    @classmethod
    def remove_implicit_resolver(cls, tag_to_remove):
        """
        Remove implicit resolvers for a particular tag

        Takes care not to modify resolvers in super classes.

        We want to load datetimes as strings, not dates, because we
        go on to serialise as json which doesn't have the advanced types
        of yaml, and leads to incompatibilities down the track.
        """
        if 'yaml_implicit_resolvers' not in cls.__dict__:
            cls.yaml_implicit_resolvers = cls.yaml_implicit_resolvers.copy()

        for first_letter, mappings in cls.yaml_implicit_resolvers.items():
            cls.yaml_implicit_resolvers[first_letter] = [
                (tag, regexp)
                for tag, regexp in mappings
                if tag != tag_to_remove
            ]


def repr_str(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar(
            u'tag:yaml.org,2002:str', data, style='|')
    return dumper.orig_represent_str(data)


def decode(secret):
    secret['data'] = {
        k: base64.b64decode(v).decode('utf8')
        for k, v in secret['data'].items()
    }
    return secret


def encode(secret):
    secret['data'] = {
        k: base64.b64encode(v.encode())
        for k, v in secret['data'].items()
    }
    return secret


def edit(fname):
    with open(fname, 'r') as fid:
        secret = yaml.load(fid, Loader=NoDatesSafeLoader)
        decoded = decode(secret)

    with open(fname, 'w') as fid:
        fid.write(yaml.safe_dump(decoded, default_flow_style=False))

    subprocess.call(EDITOR.split() + [fname])

    with open(fname, 'r') as fid:
        edited = yaml.load(fid, Loader=NoDatesSafeLoader)
        encoded = encode(edited)

    with open(fname, 'w') as fid:
        fid.write(yaml.safe_dump(encoded, default_flow_style=False))


def main():
    NoDatesSafeLoader.remove_implicit_resolver('tag:yaml.org,2002:timestamp')
    yaml.SafeDumper.orig_represent_str = yaml.SafeDumper.represent_str
    yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)
    fname = sys.argv[1]
    edit(fname)


if __name__ == '__main__':
    main()
