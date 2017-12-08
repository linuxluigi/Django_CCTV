import os
from django.template.loader import get_template
from django.core.files import File
from django.conf import settings

from cctv.settings import PROJECT_ROOT
from django_cctv.models import MonitorPage


def remove_monitor_script(monitor):
    """
    Remove Monitor service & run script
    :param monitor: Model MonitorPage
    """
    service_file_path = '%s/service/%s-service.sh' % (PROJECT_ROOT, monitor.stream_key)
    command = "%s purge" % service_file_path
    os.system(command)


def update_monitor_script(monitor):
    """
    Update or create new Monitor service & run script
    :param monitor: Model MonitorPage
    """
    print("Monitor: %s" % monitor.title)

    # try to stop current monitor process
    service_file_path = '%s/service/%s-service.sh' % (PROJECT_ROOT, monitor.stream_key)
    command_stop = "%s stop" % service_file_path
    os.system(command_stop)

    monitor_page = MonitorPage.objects.get(pk=monitor.pk)
    monitor.stream_key = monitor_page.stream_key
    monitor.stream_source = monitor_page.stream_source

    template_service = get_template("django_cctv/service/service.sh", using=None)
    template_run = get_template("django_cctv/service/run.sh", using=None)

    file_path = '%s/service/%s' % (PROJECT_ROOT, monitor.stream_key)
    service_file_path = '%s/service/%s-service.sh' % (PROJECT_ROOT, monitor.stream_key)
    run_file_path = '%s/service/%s-run.sh' % (PROJECT_ROOT, monitor.stream_key)

    context = {
        'monitor': monitor,
        'user': settings.UNIX_CAM_USER,
        'path': file_path
    }

    # create service script
    write_shell_script(template_service, service_file_path, context)

    # create run script
    write_shell_script(template_run, run_file_path, context)

    # try to run monitor script
    command_start = "%s start" % service_file_path
    os.system(command_start)


def write_shell_script(template, file_path, context):
    """
    Write run & service script for monitor
    """
    output_from_parsed_template = template.render(context)

    # write the script
    with open(file_path, 'w') as f:
        file = File(f)
        file.write(output_from_parsed_template)

    # make script executable
    mode = os.stat(file_path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(file_path, mode)
