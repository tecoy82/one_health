import re
from lxml import html
import requests


def get_csrf_token(login_url, session):
    result = session.get(login_url)

    tree = html.fromstring(result.text)

    token = str(tree.xpath('//script[contains(., "CSRF")]/text()')[0])
    token = re.search(r'(?:var CSRF = )([^;]*)', token).group(1)
    token = token.replace("'", "")

    return token


def get_ath_id(tree):
    ath_id = str(tree.xpath('//script[contains(., "CUR_ATH_ID")]/text()')[0])
    ath_id = re.search(r'(?:var CUR_ATH_ID = )([^;]*)', ath_id).group(1)
    ath_id = ath_id.replace("'", "")
    return ath_id


def get_joined_date(tree):
    # joined = str(tree.xpath('//*[contains(., "joined-at-span"")]')[0])
    joined = str(tree.xpath('//span[contains(., "joined-at-span")]//text()')[0])
    print(joined)

    # ath_id = re.search(r'(?:var CUR_ATH_ID = )([^;]*)', ath_id).group(1)
    # ath_id = ath_id.replace("'", "")
    return joined
