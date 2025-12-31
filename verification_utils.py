"""Utility helpers for SheerID verification flows."""

import re

# Branch 映射
BRANCH_ORG_MAP = {
    'Army': {'id': 4070, 'name': 'Army'},
    'Air Force': {'id': 4073, 'name': 'Air Force'},
    'Navy': {'id': 4072, 'name': 'Navy'},
    'Marine Corps': {'id': 4071, 'name': 'Marine Corps'},
    'Coast Guard': {'id': 4074, 'name': 'Coast Guard'},
    'Space Force': {'id': 4544268, 'name': 'Space Force'},
    'Army National Guard': {'id': 4075, 'name': 'Army National Guard'},
    'Army Reserve': {'id': 4076, 'name': 'Army Reserve'},
    'Air National Guard': {'id': 4079, 'name': 'Air National Guard'},
    'Air Force Reserve': {'id': 4080, 'name': 'Air Force Reserve'},
    'Navy Reserve': {'id': 4078, 'name': 'Navy Reserve'},
    'Marine Corps Forces Reserve': {'id': 4077, 'name': 'Marine Corps Forces Reserve'},
    'Coast Guard Reserve': {'id': 4081, 'name': 'Coast Guard Reserve'},
}


def match_branch(input_str: str) -> str:
    """匹配 branch 名称，允许模糊输入。"""
    normalized = input_str.upper().replace('US ', '').strip()

    for branch in BRANCH_ORG_MAP:
        if branch.upper() == normalized:
            return branch

    if 'MARINE' in normalized and 'RESERVE' not in normalized:
        return 'Marine Corps'
    if 'ARMY' in normalized and 'NATIONAL' in normalized:
        return 'Army National Guard'
    if 'ARMY' in normalized and 'RESERVE' in normalized:
        return 'Army Reserve'
    if 'ARMY' in normalized:
        return 'Army'
    if 'NAVY' in normalized and 'RESERVE' in normalized:
        return 'Navy Reserve'
    if 'NAVY' in normalized:
        return 'Navy'
    if 'AIR' in normalized and 'NATIONAL' in normalized:
        return 'Air National Guard'
    if 'AIR' in normalized and 'RESERVE' in normalized:
        return 'Air Force Reserve'
    if 'AIR' in normalized and 'FORCE' in normalized:
        return 'Air Force'
    if 'COAST' in normalized and 'RESERVE' in normalized:
        return 'Coast Guard Reserve'
    if 'COAST' in normalized:
        return 'Coast Guard'
    if 'SPACE' in normalized:
        return 'Space Force'

    return 'Army'


def extract_verification_link(content: str):
    """从邮件内容提取验证链接"""
    match = re.search(r'href="(https://services\.sheerid\.com/verify/[^"]+emailToken=[^"]+)"', content)
    if match:
        return match.group(1).replace('&amp;', '&')

    match = re.search(r'https://services\.sheerid\.com/verify/[^\s<>\"]+emailToken=\d+', content)
    if match:
        return match.group(0)

    return None


def extract_email_token(url: str):
    """从验证链接提取 emailToken"""
    match = re.search(r'emailToken=(\d+)', url)
    return match.group(1) if match else None


def parse_data_line(line: str):
    """解析数据行: firstName|lastName|branch|birthDate|dischargeDate"""
    parts = line.split('|')
    if len(parts) < 4:
        return None

    first_name = parts[0].strip()
    last_name = parts[1].strip()
    branch = parts[2].strip()
    birth_date = parts[3].strip()
    discharge_date = parts[4].strip() if len(parts) > 4 else '2025-01-02'

    branch_name = match_branch(branch)
    org = BRANCH_ORG_MAP.get(branch_name, BRANCH_ORG_MAP['Army'])

    return {
        'firstName': first_name,
        'lastName': last_name,
        'birthDate': birth_date,
        'dischargeDate': discharge_date,
        'organization': org,
    }


__all__ = [
    'BRANCH_ORG_MAP',
    'match_branch',
    'extract_verification_link',
    'extract_email_token',
    'parse_data_line',
]
