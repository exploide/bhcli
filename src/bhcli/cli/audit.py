import sys

import click
import prettytable
import datetime

from bhcli import cypher
from bhcli.api.from_config import api
from bhcli.constants import RID
from bhcli.logger import log
from .paramtypes import DomainType


ignored_relations = [
    "ClaimSpecialIdentity",
    "Enroll",
    "LocalToComputer",
    "MemberOf",
    "MemberOfLocalGroup",
]


@click.command()
@click.option("--domain", "-d", type=DomainType(), help="Audit specific domain only.")
def audit(domain):
    """Audit domains for potential security issues."""

    domains = sorted((d["name"], d["id"]) for d in api.domains(collected=True))
    if domain:
        domains = [d for d in domains if d[0] == domain.upper()]
        if not domains:
            log.error("Unknown domain %s.", domain)
            sys.exit(1)

    for dom, domsid in domains:
        print(dom)
        print("=" * len(dom))
        print()

        print("[*] Interesting privileges for domain users or computers")
        query = f"""MATCH (b:Group)-[:MemberOf|ClaimSpecialIdentity*0..]->(g:Group)
                {cypher.where("b", comparison_operator="IN", objectid=[f"{domsid}-{RID.DOMAIN_USERS}", f"{domsid}-{RID.DOMAIN_COMPUTERS}"])}
                WITH g
                MATCH p=(g)-[r]->(o)
                WHERE NOT type(r) IN {cypher.escape(ignored_relations)}
                RETURN p
                """
        result = api.cypher(query)
        nodes = result["nodes"]
        edges = result["edges"]
        relations = set()
        for edge in edges:
            relations.add((nodes[edge['source']]['label'], edge['label'], nodes[edge['target']]['label'], nodes[edge['target']]['kind']))
        count = len(relations)
        print(f"    {count} relations found")
        if count > 0:
            table = prettytable.PrettyTable()
            table.set_style(prettytable.PLAIN_COLUMNS)
            table.align = "l"
            table.field_names = ["Group", "Relation", "Target", "Kind of Target"]
            table.add_rows(sorted(relations))
            print(table)
        print()

        print("[*] Interesting privileges for guests")
        query = f"""MATCH (b:User)-[:MemberOf|ClaimSpecialIdentity*0..]->(g)
                {cypher.where("b", objectid=f"{domsid}-{RID.GUEST}")}
                WITH g
                MATCH p=(g)-[r]->(o)
                WHERE NOT type(r) IN {cypher.escape(ignored_relations)}
                RETURN p
                """
        result = api.cypher(query)
        nodes = result["nodes"]
        edges = result["edges"]
        relations = set()
        for edge in edges:
            relations.add((nodes[edge['source']]['label'], edge['label'], nodes[edge['target']]['label'], nodes[edge['target']]['kind']))
        count = len(relations)
        print(f"    {count} relations found")
        if count > 0:
            table = prettytable.PrettyTable()
            table.set_style(prettytable.PLAIN_COLUMNS)
            table.align = "l"
            table.field_names = ["Guest Object", "Relation", "Target", "Kind of Target"]
            table.add_rows(sorted(relations))
            print(table)
        print()

        print("[*] Kerberoastable user accounts of high value (enabled, no MSA/gMSA)")
        result = api.users(domainsid=domsid, hasspn=True, enabled=True)
        result = [
            n
            for n in result
            if n["isTierZero"]
            and not n["properties"].get("msa", False)
            and not n["properties"].get("gmsa", False)
        ]
        count = len(result)
        print(f"    {count} accounts found")
        result = sorted(n["properties"]["name"] for n in result)
        for n in result:
            print(n)
        print()

        print("[*] AS-REP-roastable user accounts (enabled)")
        result = api.users(domainsid=domsid, dontreqpreauth=True, enabled=True)
        count = len(result)
        print(f"    {count} accounts found")
        result = sorted(n["properties"]["name"] for n in result)
        for n in result:
            print(n)
        print()

        print("[*] Accounts trusted for unconstrained delegation (enabled, no DCs)")
        query = f"""MATCH (dc)-[:MemberOf*1..]->(g:Group)
                {cypher.where("g", objectid=f"{domsid}-{RID.DOMAIN_CONTROLLERS}")}
                WITH COLLECT(dc) AS exclude
                MATCH (n)
                {cypher.where("n", domainsid=domsid, unconstraineddelegation=True, enabled=True)}
                AND NOT n IN exclude
                RETURN n
                """
        result = api.cypher(query)["nodes"].values()
        count = len(result)
        print(f"    {count} accounts found")
        result = sorted(n["properties"]["name"] for n in result)
        for n in result:
            print(n)
        print()

        print("[*] Computers with unsupported operating systems (enabled)")
        query = f"""MATCH (c:Computer)
                {cypher.where("c", domainsid=domsid, enabled=True)}
                AND c.operatingsystem =~ '(?i).*Windows.* (2000|2003|2008|2012|xp|vista|7|8|me|nt).*'
                RETURN c
                """
        result = api.cypher(query)["nodes"].values()
        count = len(result)
        print(f"    {count} computers found")
        result = sorted((n["properties"]["operatingsystem"], n["properties"]["name"]) for n in result)
        for n in result:
            print(f"{n[1]} ({n[0]})")
        print()

        print("[*] Accounts which have PasswordNotRequired set (enabled)")
        query = f"""
                MATCH (u:User) 
                {cypher.where("u", domainsid=domsid, passwordnotreqd=True, enabled=True)} 
                RETURN u
                """
        result = api.cypher(query)["nodes"].values()
        count = len(result)
        print(f"    {count} accounts found")
        
        relations = set()
        for n in result:
            is_tier0 = False
            if n["properties"].get("system_tags") != None and "admin_tier_0" in n["properties"].get("system_tags"):
                is_tier0 = True
            lastLogonDate = datetime.datetime.fromtimestamp(n["properties"]["lastlogon"]).strftime('%Y-%m-%d %H:%M:%S')
            pwLastSetDate = datetime.datetime.fromtimestamp(n["properties"]["pwdlastset"]).strftime('%Y-%m-%d %H:%M:%S')
            relations.add((n["properties"]["name"], n["kind"], pwLastSetDate, lastLogonDate, is_tier0)) 
        if count > 0:
            table = prettytable.PrettyTable()
            table.set_style(prettytable.PLAIN_COLUMNS)
            table.align = "l"
            table.field_names = ["Name", "Type", "PasswordLastSet", "LastLogin", "Tier-0"]
            table.add_rows(sorted(relations))
            print(table)
        print()



        print()
