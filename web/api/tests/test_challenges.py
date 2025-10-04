from web.api.app.services import challenges


def test_list_challenges_contains_entries():
    catalog = challenges.list_challenges()
    assert isinstance(catalog, dict)
    assert any(len(items) > 0 for items in catalog.values())


def test_get_challenge_returns_detail():
    catalog = challenges.list_challenges()
    first_difficulty = next(iter(catalog.values()))
    first_challenge = first_difficulty[0]

    detail = challenges.get_challenge(first_challenge.id)
    assert detail.id == first_challenge.id
    assert detail.title
    assert detail.task
