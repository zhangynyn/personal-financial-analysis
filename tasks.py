from invoke import task


@task
def format(c):
    c.run("black .")
    c.run("isort .")
    c.run("flake8 .")
