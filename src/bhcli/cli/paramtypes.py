from click import ParamType
from click.shell_completion import CompletionItem

from bhcli.api.exceptions import ApiException
from bhcli.api.from_config import api


class AssetGroupTagType(ParamType):
    """ParamType for asset-group-tags."""

    name = "asset_group_tag"

    def shell_complete(self, ctx, param, incomplete):
        try:
            asset_group_tags = [
                agt["name"]
                for agt in api.get_asset_group_tags()
                if agt["name"].lower().startswith(incomplete.lower())
            ]
        except ApiException:
            return []
        return [
            CompletionItem(agt)
            for agt in sorted(asset_group_tags)
        ]


class DomainType(ParamType):
    """ParamType for a domain name."""

    name = "domain"

    def shell_complete(self, ctx, param, incomplete):
        try:
            domains = [
                domain["name"]
                for domain in api.domains(collected=True)
                if domain["name"].lower().startswith(incomplete.lower())
            ]
        except ApiException:
            return []
        return [
            CompletionItem(domain)
            for domain in sorted(domains)
        ]


class GroupType(ParamType):
    """ParamType for a group name."""

    name = "group"

    def shell_complete(self, ctx, param, incomplete):
        try:
            groups = [
                group["label"]
                for group in api.groups()
                if group["label"].lower().startswith(incomplete.lower())
            ]
        except ApiException:
            return []
        return [
            CompletionItem(group)
            for group in sorted(groups)
        ]
