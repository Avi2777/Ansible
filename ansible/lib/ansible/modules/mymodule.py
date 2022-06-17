#!/usr/bin/python

# Copyright: (c) 2022, Aviran benhamo <aviranbenhamo@gmail.com>

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import os
import shutil
from ..module_utils.basic import AnsibleModule

DOCUMENTATION = r'''
---
module: mymodule

short_description: This is my custom module 

version_added: "1.0.0"

description: with this module it's possible to create directory/file under a specific path.
            as well to delete directory/file under a specific path and validate if path exist.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
        
    state:
        description:
        -If (create_dir), all intermediate subdirectories will be created if they
      do not exist.    
        -If (create_file), an empty file will be created if the file does not
      exist, while an existing file no change will apply.
        -If (delete_dir), the specified directory will be deleted.
        -If (delete_file), the specified file will be deleted.
        -If (validator), validate if path is exist, if not raise an error.

author:
    - Your Name (@Avi2777)
'''

EXAMPLES = r'''
    - name: create directory under a specific path
      mymodule:
        path: foo/bar/dir
        state: create_dir

    - name: create file under a specific path
      mymodule:
        path: foo/bar/dir/shalom.py
        state: create_file
        
    - name: validate if path exist, if not raise an error
      mymodule:
        path: foo/bar/dir/
        state: validator    
        
    - name: delete file under a specific path
      mymodule:
          path: foo/bar/dir/shalom.py
          state: delete_file    
          
    - name: delete directory under a specific path
      mymodule:
          path: foo/bar/dir/
          state: delete_dir      

'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=False),
        new=dict(type='bool', required=False, default=False),
        state=dict(type='str', choices=['delete_dir', 'delete_file', 'create_dir', 'create_file', 'validator']),
        path=dict(type='path', required=True, aliases=['dest', 'name']),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
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
    path = module.params['path']
    state = module.params['state']

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)

    if not os.path.exists(path):
        if state == 'validator':
            module.fail_json(msg='Error Path not exist', **result)
        if state == 'create_dir':
            os.makedirs(path)
            module.params['new'] = True
        if state == 'create_file':
            with open(path, 'a'):
                module.params['new'] = True
    elif os.path.exists(path):
        if state == 'delete_file':
            os.remove(path)
            module.params['new'] = True
        if state == 'delete_dir':
            shutil.rmtree(path)
            module.params['new'] = True

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
