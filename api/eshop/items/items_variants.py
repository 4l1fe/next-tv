# coding: utf-8
from utils.validation import validate_int
from models.eshop.variants.variants import Variants


def get(item_id, auth_user, session, **kwargs):
    data = {}
    item_id = validate_int(item_id, min_value=1)
    instance = Variants.get_variants_by_item_id(auth_user, session, item_id)

    return data
