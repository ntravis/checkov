

from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck


class GCPCloudRunPrivateService(BaseResourceCheck):
    def __init__(self):
        name = "Ensure that GCP Cloud Run services are not anonymously or publicly accessible"
        id = "CKV_GCP_102"
        supported_resources = ['google_cloud_run_service_iam_member', 'google_cloud_run_service_iam_binding']
        categories = [CheckCategories.GENERAL_SECURITY]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        public_principals = (
            "allUsers",
            "allAuthenticatedUsers"
            )
        # Depending on the terraform resource type -
        # The member config is either a list or single principal
        if self.entity_type == "google_cloud_run_service_iam_member":
            # conf.get returns as a list
            # so we create a string for comparison
            if "member" in conf.keys():
                member = conf.get("member")[0]
                if member in public_principals:
                    return CheckResult.FAILED
                else:
                    return CheckResult.PASSED
        # iam_binding returns a list of principals
        elif self.entity_type == "google_cloud_run_service_iam_binding":
            # Since conf.get returns a list and iam_binding returns a list (nested list)
            # we pull out the members list using the index 0
            if "members" in conf.keys():
                members_list = conf.get("members")[0]
                if any(member in public_principals for member in members_list):
                    return CheckResult.FAILED
                else:
                    return CheckResult.PASSED

check = GCPCloudRunPrivateService()
