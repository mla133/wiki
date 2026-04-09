# scripts/install-hooks.sh
#!/bin/sh
mkdir -p .git/hooks
cp scripts/git-hooks/post-commit .git/hooks/post-commit
chmod +x .git/hooks/post-commit

cp scripts/git-hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

echo "✅ Git hooks installed"
