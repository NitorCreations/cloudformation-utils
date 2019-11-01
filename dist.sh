#!/bin/bash
rm -rf build dist
VERSION=$1
MESSAGE="$2"
bumpversion --new-version $VERSION --message "$MESSAGE" setup.py
python setup.py sdist bdist_wheel
gpg -o dist/cloudformation_utils-${VERSION}-py2.py3-none-any.whl.asc -a -b dist/cloudformation_utils-${VERSION}-py2.py3-none-any.whl
gpg -o dist/cloudformation-utils-${VERSION}.tar.gz.asc -a -b dist/cloudformation-utils-${VERSION}.tar.gz
twine upload dist/*