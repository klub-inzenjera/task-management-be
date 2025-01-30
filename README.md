# task-management-be

## Project Setup
```bash
  python -m venv venv
  source venv/bin/activate
```
```bash
  pip install fastapi uvicorn
```
```bash
  uvicorn main:app --reload
```



## Basic Git Commands

### Initializing and Cloning
```bash
  git init  # Initialize a new Git repository
  git clone <repo_url>  # Clone an existing repository
```

### Staging and Committing Changes
```bash
  git status  # Check the status of your files
  git add <file>  # Stage a specific file
  git add .  # Stage all changes
  git commit -m "Your commit message"  # Commit staged changes
```

### Working with Branches
```bash
  git branch  # List all branches
  git branch <branch_name>  # Create a new branch
  git checkout <branch_name>  # Switch to a branch
  git checkout -b <branch_name>  # Create and switch to a new branch
```

### Pushing and Pulling Changes
```bash
  git push origin <branch_name>  # Push changes to remote repository
  git pull origin <branch_name>  # Pull latest changes from remote
```

### Merging and Rebasing
```bash
  git merge <branch_name>  # Merge a branch into the current branch
  git rebase <branch_name>  # Rebase the current branch onto another
```

### Undoing Changes
```bash
  git reset --soft HEAD~1  # Undo last commit but keep changes staged
  git reset --hard HEAD~1  # Undo last commit and discard changes
  git revert <commit_hash>  # Create a new commit that undoes a previous one
```

### Checking History
```bash
  git log  # View commit history
  git log --oneline --graph  # View a simplified commit history
```
