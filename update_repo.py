import shutil
import zipfile

import os

import re
from xml.etree import ElementTree

from addons_xml_generator import Generator

if __name__ == "__main__":
    if __name__ == '__main__':
        for addon_name in os.listdir('..'):
            source_addon_dir = os.path.join('..', addon_name)
            source_addon_xml = os.path.join(source_addon_dir, 'addon.xml')
            source_addon_icon = os.path.join(source_addon_dir, 'icon.png')
            target_addon_dir = os.path.join(addon_name)
            target_addon_xml = os.path.join(target_addon_dir, 'addon.xml')
            target_addon_icon = os.path.join(target_addon_dir, 'icon.png')

            if os.path.exists(source_addon_xml):
                tree = ElementTree.parse(source_addon_xml)
                doc = tree.getroot()
                addon_version = doc.attrib['version']
                target_addon_zip = os.path.join(target_addon_dir, '{0:s}-{1:s}.zip'.format(addon_name, addon_version))

                if not os.path.exists(target_addon_dir):
                    os.mkdir(target_addon_dir)
                shutil.copy(source_addon_xml, target_addon_xml)
                if os.path.exists(source_addon_icon):
                    shutil.copy(source_addon_icon, target_addon_icon)
                if addon_name.startswith('repository.'):
                    if os.path.exists(target_addon_zip):
                        os.unlink(target_addon_zip)
                    source_addon_dir = addon_name
                with zipfile.ZipFile(target_addon_zip, 'w', zipfile.ZIP_DEFLATED) as zip:
                    for root, dirs, files in os.walk(source_addon_dir):
                        for f in files:
                            filename = os.path.join(root, f)
                            if source_addon_dir == addon_name:
                                arcname = filename
                            else:
                                arcname = os.path.relpath(filename, os.path.join('..'))

                            if f in [
                                'addon.py',
                                'addon.xml',
                                'changelog.txt',
                                'fanart.jpg',
                                'icon.png',
                                'LICENSE.txt'
                            ] or arcname.startswith(os.path.join(addon_name, 'resources')):
                                zip.write(filename, arcname)

        Generator()
