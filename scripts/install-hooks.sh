# scripts/install-hooks.sh
#!/bin/sh
mkdir -p .git/hooks
cp scripts/git-hooks/post-commit .git/hooks/post-commit
chmod +x .git/hooks/post-commit
echo "✅ Git hooks installed"
