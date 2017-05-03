def build_population_query(request, prefix):
    candidates = request.hero.location.npc_set.filter(able=True, unit=None)
    if request.POST.get('{}men'.format(prefix)) and request.POST.get \
            ('{}women'.format(prefix)):
        pass
    elif request.POST.get('{}men'.format(prefix)) and not request.POST.get \
            ('{}women'.format(prefix)):
        candidates = candidates.filter(male=True)
    elif not request.POST.get('{}men'.format(prefix)) and request.POST.get \
            ('{}women'.format(prefix)):
        candidates = candidates.filter(male=False)
    elif not request.POST.get('{}men'.format(prefix)) and not request.POST.get \
            ('{}women'.format(prefix)):
        raise Exception("You must choose at least one gender.")

    if request.POST.get('{}trained'.format(prefix)) and request.POST.get \
            ('{}untrained'.format(prefix)):
        pass
    elif request.POST.get('{}trained'.format(prefix)) and not request.POST.get \
            ('{}untrained'.format(prefix)):
        candidates = candidates.filter(trained_soldier=True)
    elif not request.POST.get('{}trained'.format(prefix)) and request.POST.get \
            ('{}untrained'.format(prefix)):
        candidates = candidates.filter(trained_soldier=False)
    elif not request.POST.get \
            ('{}trained'.format(prefix)) and not request.POST.get \
            ('{}untrained'.format(prefix)):
        raise Exception("You must choose at least one training group.")

    skill_queries = []
    if request.POST.get('{}skill_high'.format(prefix)):
        skill_queries.append(Q(skill_fighting__gte=NPC.TOP_SKILL_LIMIT))
    if request.POST.get('{}skill_medium'.format(prefix)):
        skill_queries.append(Q(skill_fighting__gte=NPC.MEDIUM_SKILL_LIMIT, skill_fighting__lt=NPC.TOP_SKILL_LIMIT))
    if request.POST.get('{}skill_low'.format(prefix)):
        skill_queries.append(Q(skill_fighting__lt=NPC.MEDIUM_SKILL_LIMIT))
    if len(skill_queries) == 0:
        raise Exception("You must choose at least one skill group")

    # See https://stackoverflow.com/questions/852414/how-to-dynamically-compose-an-or-query-filter-in-django
    query = skill_queries.pop()
    for item in skill_queries:
        query |= item
    candidates.filter(query)

    age_queries = []
    if request.POST.get('{}age_old'.format(prefix)):
        age_queries.append(Q(age_months__gte=NPC.OLD_AGE_LIMIT))
    if request.POST.get('{}age_middle'.format(prefix)):
        age_queries.append(Q(age_months__gte=NPC.MIDDLE_AGE_LIMIT, age_months__lt=NPC.OLD_AGE_LIMIT))
    if request.POST.get('{}age_young'.format(prefix)):
        age_queries.append(Q(age_months__gte=NPC.YOUNG_AGE_LIMIT, age_months__lt=NPC.MIDDLE_AGE_LIMIT))
    if request.POST.get('{}age_very_young'.format(prefix)):
        age_queries.append(Q(age_months__gte=NPC.VERY_YOUNG_AGE_LIMIT, age_months__lt=NPC.YOUNG_AGE_LIMIT))
    if len(skill_queries) == 0:
        raise Exception("You must choose at least one age group")

    # See https://stackoverflow.com/questions/852414/how-to-dynamically-compose-an-or-query-filter-in-django
    query = age_queries.pop()
    for item in age_queries:
        query |= item
    candidates.filter(query)

    return candidates