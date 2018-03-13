import rules

@rules.predicate
def user_in_edition_groups(user, obj):
    try:
        if user in [u for g in obj.layer.edition_groups.all() for u in g.user_set.all()]:
            return True
        else:
            return False
    except (NameError, AttributeError):
        return False

@rules.predicate
def user_in_creation_layer_groups(user, layer):
    try:
        if user in [u for g in layer.creation_groups.all() for u in g.user_set.all()]:
            return True
        else:
            return False
    except (NameError, AttributeError):
        return False

@rules.predicate
def user_in_creation_groups(user, obj):
    try:
        if user in [u for g in obj.layer.creation_groups.all() for u in g.user_set.all()]:
            return True
        else:
            return False
    except (NameError, AttributeError):
        return False


rules.add_perm('core.change_archaeologicalplace', user_in_edition_groups )#& rules.always_deny)
rules.add_perm('core.add_archaeologicalplace', user_in_creation_groups | user_in_creation_layer_groups )
