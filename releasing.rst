1) Commit all files and push to main

2) run bump-my-version::

    bump-my-version bump -v --dry-run patch # Test run
    bump-my-version bump patch # Possible values: major / minor / patch

3) Push tags::

    git push --tags

4) Build::

    poetry build

5) Release (username "__token__", password is in password manager).::

    twine upload dist/*
