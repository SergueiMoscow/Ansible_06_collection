#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

DOCUMENTATION = r'''
---
module: my_own_module

short_description: This is test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    path:
        description: Path to create file.
        required: true
        type: str
    content:
        description:
            - File content.
        required: false
        type: str

author:
    - Sergey Sushkov (@SergueiMoscow)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test create file with specify content
  my_own_module:
    path: '/tmp/test/test1.txt'
    content: 'Test content'

# pass in a message and have changed true
- name: Test with a message and changed output
  my_own_module:
    path: '/tmp/test/test1.txt'
    content: 'Test content'

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'File <filename> created'
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=False, default='Default content')
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    path = module.params['path']
    content = module.params['content']

    try:
        # Создание дерева директорий, если они не существуют
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            result['changed'] = True
            result['message'] = 'File %s created' % path
        else:
            with open(path, 'r') as file:
                existing_content = file.read()
            result['changed'] = existing_content != content
            result['message'] = 'File %s updated' % path if result['changed'] else 'File already exists with correct content'

        if result['changed']:
            with open(path, 'w') as file:
                file.write(content)
    except Exception as e:
        module.fail_json(msg='Failed to handle file %s: %s' % (path, str(e)))

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()