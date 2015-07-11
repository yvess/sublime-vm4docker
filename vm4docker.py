import sublime_plugin
import sublime
import socket
import subprocess
import os
import sys
import logging


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)


__version__ = '0.1.0'
__authors__ = ['"Yves Serrano" <y@yas.ch>']


def plugin_loaded():
    pass


class DockertouchListener(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        settings = view.settings()
        plugin_settings = sublime.load_settings('vm4docker.sublime-settings')
        host, extensions, paths, do_ssh_key_checking = (
            settings.get(
                'host',
                plugin_settings.get('host', 'docker')
            ),
            settings.get(
                'file_extensions',
                plugin_settings.get('file_extensions', [])
            ),
            settings.get(
                'watch_paths',
                plugin_settings.get('watch_paths', [os.getenv("HOME")])
            ),
            settings.get(
                'do_ssh_key_checking',
                plugin_settings.get('do_ssh_key_checking', False)
            ),
        )
        fname = view.file_name()
        if not self.is_valid_fname(fname, paths, extensions):
            return
        if self.ssh_is_open():
            no_ssh_key_checking = '-oStrictHostKeyChecking=no'
            if do_ssh_key_checking:
                no_ssh_key_checking = ''
            subprocess.check_call(
                ['ssh', no_ssh_key_checking, host, 'touch', '-c', fname]
            )

    def is_valid_fname(self, fname, paths, extensions):
        valid_path = False
        for path in paths:
            if fname.startswith(path):
                valid_path = True
                break
        valid_ext = True
        if extensions:
            valid_ext = fname.split(".")[-1] in [extensions]
        return all([valid_path, valid_ext])

    def ssh_is_open(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        is_open = True if sock.connect_ex(('docker', 22)) == 0 else False

        return is_open
