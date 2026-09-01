1) Commit all files and push to main

2) run bump-my-version::

    bump-my-version bump -v --dry-run patch # Test run
    bump-my-version bump patch # Possible values: major / minor / patch

3) Push tags::

    git push --tags

4) Build::

    poetry build

5) Release (replace <token> with value found in password manager).::

    poetry config pypi-token.pypi <token>
    poetry publish
