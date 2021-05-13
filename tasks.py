from invoke import task

@task
def publish(c):
    c.run("func azure functionapp publish func-matchnotifier-westeurope-001")
