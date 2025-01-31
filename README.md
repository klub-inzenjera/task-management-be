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

## Git commands
```
git init    --   Inicijalizuje novi Git repozitorijum u trenutnom direktorijumu
git add <ime_fajla>  
git commit -m "Poruka"
git push
git clone <repo_URL>
git pull origin <branch>  --   Preuzima najnovije promene iz udaljenog repozitorijuma i spaja ih sa lokalnim
git branch  --  Prikazuje listu svih grana u repozitorijumu
git branch <ime_grane>  --  Kreira novu granu
git switch -c <ime_grane>  --  Kreira novu granu i odmah se prebacuje na nju
git log --graph --all --pretty="%x09 %C(Yellow)%h  %C(reset)%ad (%C(Green)%cr%C(reset)) %x09 %C(Cyan)%an:%Cred%d %C(reset)%s" --date=short  --  Prikazuje istorijat commit-ova u repozitorijumu.
git merge <ime_grane>  --  Spaja promene iz određene grane u trenutnu granu
git reset --hard <commit_id>  --  Vraća repozitorijum na određeni commit i briše sve naknadne promene
git remote -v  --  Prikazuje listu udaljenih repozitorijuma povezanih sa lokalnim
