# Todo App backend

## Test
```bash
docker-compose -f docker-test.yml up --build
```

## Run

- Populate env/.env.prod with env variables (database creds)
- build image
```bash
docker build --tag todo_app --file Dockerfile .
```
- run image
```bash
docker run -e APP_ENV=prod -it --rm -p 80:80 --name backend todo_app
```

## Points to improve
- it's generally better to have different python settings file, rather than
one reading from different .env files. For instance, if db credentials stored
as AWS Secret, it would take a much cleaner implementation to fetch them
- Migrate to full async
- Multistage build? Though now it's not producing much smaller build, it may
change in real app over some time bc of new dependencies
- Tests are talking to real DB now. It's worth investing some time in 
reconfiguring test setup to use mock session instead