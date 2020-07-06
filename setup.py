import os
from setuptools import setup
from distutils.command.build_py import build_py


def generate_api_endpoints_py_content(directory):
      import json
      filename = 'api_endpoints'
      source_file = 'tinder_api/' + filename + '.json'
      new_file = os.path.join(directory, filename + '.py')
      with open(source_file, 'r') as endpoints_file:
            source_file_contents = endpoints_file.read()
            parsed_source_file_contents = json.loads(source_file_contents)
            new_file_content = filename.upper() + '=' + str(parsed_source_file_contents)
            with open(new_file, 'w') as api_endpoints_py:
                  api_endpoints_py.write(new_file_content)


# https://digip.org/blog/2011/01/generating-data-files-in-setup.py.html
class my_build_py(build_py):
      def run(self):
        # honor the --dry-run flag
        if not self.dry_run:
            target_dir = os.path.join(self.build_lib, 'tinder_api')
            self.mkpath(target_dir)
            generate_api_endpoints_py_content(target_dir)

        # distutils uses old-style classes, so no super()
        build_py.run(self)


setup(name='tinder_api',
      version='1.0.1',
      description='Tinder API wrapper in Python',
      long_description=open('README.md').read().strip(),
      author='Sean Floyd',
      maintainer='Sean Floyd',
      url='https://github.com/SeanLF/Tinder',
      py_modules=['tinder_api.api', 'tinder_api.facebook_auth_token', 'tinder_api.helpers'],
      install_requires=['requests',
                        'robobrowser',
                        'lxml'],
      license='MIT License',
      zip_safe=False,
      keywords=['tinder-api', 'tinder', 'python-3'],
      cmdclass={'build_py': my_build_py},
     )
