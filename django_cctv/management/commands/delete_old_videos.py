from django.core.management.base import BaseCommand

import os


def get_space_usage(path):
    """
    get used hdd space in percent
    :param path:
        path from the mounted hdd
    :return:
        float percent number of used space
    """
    # get disk space with path
    st = os.statvfs(path)
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize

    used_space_percent = 100 / total * used

    return used_space_percent


class Command(BaseCommand):
    help = 'Delete old videos to make new free space.'

    def add_arguments(self, parser):
        # path
        parser.add_argument('path', type=str)

        # set free space minimum in percent argument
        parser.add_argument(
            '--set-space-maximum',
            dest='space-maximum',
            action="store",
            type=int,
            help='Enable to delete videos without any motions',
        )

    def handle(self, *args, **options):
        path = options['path']

        if options['space-maximum']:
            space_maximum = options['space-maximum']
        else:
            space_maximum = 90

        # if used space higher as maximum delete files
        if get_space_usage(path) >= space_maximum:

            os.chdir(path)
            files = filter(os.path.isfile, os.listdir(path))
            files = [os.path.join(path, f) for f in files]  # add path to each file
            files.sort(key=lambda x: os.path.getmtime(x))

            for file in files:
                print("delete: %s" % file)
                os.remove(file)
                if get_space_usage(path) <= space_maximum:
                    break