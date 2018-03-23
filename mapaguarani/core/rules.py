import rules

@rules.predicate
def user_in_permission_groups(user, obj):
    try:
        if user in [u for g in obj.layer.permission_groups.all() for u in g.user_set.all()]:
            return True
        else:
            return False
    except (NameError, AttributeError):
        return False


rules.add_perm('core.change_archaeologicalplace', user_in_permission_groups)
rules.add_perm('core.add_archaeologicalplace', user_in_permission_groups)

rules.add_perm('core.change_indigenousland', user_in_permission_groups)
rules.add_perm('core.add_indigenousland', user_in_permission_groups)

rules.add_perm('core.change_indigenousvillage', user_in_permission_groups)
rules.add_perm('core.add_indigenousvillage', user_in_permission_groups)
