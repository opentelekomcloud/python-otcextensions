#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
'''SDRS Job CLI implementation'''
import logging
import json

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def _add_sub_jobs_to_obj(obj, data, columns):
    name = 'entities'
    data += ('\n'.join((f'sub_job={ent.job_id}'
                        for ent in obj.entities.sub_jobs)),)

    columns = columns + (name,)
    return data, columns


def _add_server_group_to_obj(obj, data, columns):
    name = 'entities'
    data += ('protection_group_id=' + obj.entities.server_group_id,)

    columns = columns + (name,)
    return data, columns


def _add_parsed_task_to_obj(obj, data, columns):
    first, last = obj.fail_reason.split('error : ')
    error_dict = json.loads(last)
    message = next(iter(error_dict.values()))['message']
    code = next(iter(error_dict.values()))['code']
    data += (message,)
    columns = columns + ('message',)
    data += (code,)
    columns = columns + ('status_code',)
    data += (obj.error_code,)
    columns += ('error_code',)
    return data, columns

def _flatten_job(obj):
    """Flatten the structure of the job into a single dict
    """

    data = {
        'id': obj.job_id,
        'status': obj.status,
        'job_type': obj.job_type,
        'begin_time': obj.begin_time,
        'end_time': obj.end_time
    }

    return data


class ShowJob(command.ShowOne):
    _description = _('Show single job details')
    columns = (
        'id',
        'status',
        'job_type',
        'begin_time',
        'end_time'
    )

    def get_parser(self, prog_name):
        parser = super(ShowJob,self).get_parser(prog_name)
        parser.add_argument(
            'job',
            metavar='<job>',
            help=_('ID of the SDRS job.')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.sdrs

        obj = client.get_job(
            job=parsed_args.job
        )

        data = utils.get_dict_properties(
            _flatten_job(obj), self.columns
        )

        if obj.entities.sub_jobs:
            data, self.columns = _add_sub_jobs_to_obj(obj, data,
                                                      self.columns)

        if obj.entities.server_group_id:
            data, self.columns = _add_server_group_to_obj(obj, data,
                                                          self.columns)

        if obj.fail_reason:
            data, self.columns = _add_parsed_task_to_obj(obj, data,
                                                         self.columns)

        return (self.columns, data)
