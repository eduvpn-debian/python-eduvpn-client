from itertools import chain
from typing import List, Dict, Optional
from eduvpn.i18n import extract_translation
from eduvpn.type import url
from eduvpn.nm import nm_available


def input_int(max_: int):
    """
    Request the user to enter a number.
    """
    while True:
        choice = input("\n> ")
        if choice.isdigit() and int(choice) < max_:
            break
        else:
            print("error: invalid choice")
    return int(choice)


def provider_choice(institutes: List[dict], orgs: List[dict]) -> url:
    """
    Ask the user to make a choice from a list of instutute and secure internet providers.
    """
    print("\nPlease choose server:\n")
    print("Institute access:")
    for i, row in enumerate(institutes):
        print(f"[{i}] {extract_translation(row['display_name'])}")

    print("Secure internet: \n")
    for i, row in enumerate(orgs, start=len(institutes)):
        print(f"[{i}] {extract_translation(row['display_name'])}")

    choice = input_int(max_=len(institutes) + len(orgs))

    if choice < len(institutes):
        return institutes[choice]['base_uri']
    else:
        org = orgs[choice - len(institutes)]
        return org['secure_internet_home']


def menu(institutes: List[dict], orgs: List[dict], search_term: Optional[str] = None) -> Optional[str]:
    if not search_term:
        return provider_choice(institutes, orgs)

    if search_term:
        return search(institutes, orgs, search_term)


def search(institutes: List[dict], orgs: List[dict], search_term: str) -> Optional[str]:
    """
    Search the list of institutes and organisations for a string match.
    """
    institute_match = [i for i in institutes if search_term in extract_translation(i['display_name']).lower()]

    org_match = [i for i in orgs if search_term in extract_translation(i['display_name']).lower() or
                 ('keyword_list' in i and search_term in i['keyword_list'])]

    if len(institute_match) == 0 and len(org_match) == 0:
        print(f"The filter '{search_term}' had no matches")
        return None
    elif len(institute_match) == 1 and len(org_match) == 0:
        institute = institute_match[0]
        print(f"filter '{search_term}' matched with institute '{institute['display_name']}'")
        return institute['base_url']
    elif len(institute_match) == 0 and len(org_match) == 1:
        org = org_match[0]
        print(f"filter '{search_term}' matched with organisation '{org['display_name']}'")
        return org['base_uri']
    else:
        matches = [i['display_name'] for i in chain(institute_match, org_match)]
        print(f"filter '{search_term}' matched with {len(matches)} organisations, please be more specific.")
        print("Matches:")
        [print(f" - {extract_translation(m)}") for m in matches]
        return None


def profile_choice(profiles: List[Dict]) -> int:
    """
    If multiple profiles are available, present user with choice which profile.
    """
    if len(profiles) > 1:
        print("\nplease choose a profile:\n")
        for i, profile in enumerate(profiles):
            print(f" * [{i}] {profile['display_name']}")
        choice = input_int(max_=len(profiles))
        return profiles[int(choice)]['profile_id']
    else:
        return profiles[0]['profile_id']


def write_to_nm_choice() -> bool:
    """
    When Network Manager is available, asks user to add VPN to Network Manager
    """
    if nm_available():
        print("\nWhat would you like to do with your VPN configuration:\n")
        print("* [0] Write .ovpn file to current directory")
        print("* [1] Add VPN configuration to Network Manager")
        return bool(input_int(max_=2))
    else:
        return False
