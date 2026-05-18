# TODO - Number Whisperer Duel

- [ ] Refactor game state in `main.py` to support per-round:
  - [ ] User-entered `user_secret` (1-100)
  - [ ] AI bounds tracking for deducing `user_secret`
  - [ ] Proper win condition: “who guesses first wins”
  - [ ] User also guesses AI secret via entry
- [ ] Implement out-of-rule/cheating validation:
  - [ ] Every Higher/Lower/Correct press must keep bounds consistent
  - [ ] If bounds become inconsistent, show exactly: "This is out of rule and you are cheating"
- [ ] Update UI:
  - [ ] Add dashboard/cards for 5 rounds + match scoreboard
  - [ ] Add clear controls and turn-locking when a round ends
  - [ ] Keep 3 required buttons: Higher / Lower / Correct
- [ ] Fix end-of-round logic and match reset after 5 rounds
- [ ] Manual test playthroughs (normal + cheating scenarios)

