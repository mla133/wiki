# About Git Hooks (Important Reminder)
.git/hooks/* does NOT get pushed to GitHub

## Keep Hooks in:
```
scripts/git-hooks/post-commit
```
## Add:
```
scripts/install-hooks.sh
```
##  After cloning the repo elsewhere:
```
git clone https://github.com/mla133/wiki.git
cd wiki
./scripts/install-hooks.sh
```
This will copy the current git hooks to the .git/hooks directory

