# -*- coding: utf-8 -*-
import logging
from util import full_stack
from workflow.steps.util.base import BaseStep
from workflow.exceptions.error_codes import DBAAS_0021
from dbaas_nfsaas.models import HostAttr

LOG = logging.getLogger(__name__)


class UpdateDbaaSMetadata(BaseStep):

    def __unicode__(self):
        return "Updating dbaas metadata..."

    def do(self, workflow_dict):
        try:
            old_host_attr = HostAttr.objects.get(nfsaas_path=workflow_dict['export_path'])
            old_host_attr.is_active = False
            old_host_attr.save()

            new_host_attr = HostAttr()
            new_host_attr.host = old_host_attr.host
            new_host_attr.nfsaas_export_id = workflow_dict['new_export_id']
            new_host_attr.nfsaas_path = workflow_dict['new_export_path']
            new_host_attr.is_active = True
            new_host_attr.save()

            host = workflow_dict['not_primary_hosts'][0]
            old_host_attr = HostAttr.objects.get(host=host, is_active=True)
            old_host_attr.is_active = False
            old_host_attr.save()

            new_host_attr = HostAttr()
            new_host_attr.host = old_host_attr.host
            new_host_attr.nfsaas_export_id = workflow_dict['new_export_id_2']
            new_host_attr.nfsaas_path = workflow_dict['new_export_path_2']
            new_host_attr.is_active = True
            new_host_attr.save()

            return True
        except Exception:
            traceback = full_stack()

            workflow_dict['exceptions']['error_codes'].append(DBAAS_0021)
            workflow_dict['exceptions']['traceback'].append(traceback)

            return False

    def undo(self, workflow_dict):
        LOG.info("Running undo...")
        try:
            return True
        except Exception:
            traceback = full_stack()

            workflow_dict['exceptions']['error_codes'].append(DBAAS_0021)
            workflow_dict['exceptions']['traceback'].append(traceback)

            return False
