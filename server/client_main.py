from pki import *
from client_socket import *
import json
import click

@click.group(chain=True, invoke_without_command=True)
def cli():
    pass

@cli.command(name='saveData', help='Generates data in json to be sent to the server')
@click.option('-n','--name', default='John Doe', help='Your name')
@click.option('-c','--cpf', default='123.456.789-01', help='Your CPF')
@click.option('-e','--email', default='john@doe.com', help='Your e-mail address')
@click.option('-s', '--share', default='name,email', help='What to grant permissions to server, e.g., \'name,email\' grants to the server the permission of sharing your name and your email')
def collect_data(name, cpf, email, share):
    """
    collect_data function collects data from user, e.g., name, cpf, email
    and their permissions. The user also sends their permissions. As an 
    example, if the user allows the server to share his email and name to
    another domain, he must use the --share option with name,email. The code
    splits the argument in the comma and modifies a dictionary that will be
    sent to the server. The data and the permissions are sent to the server
    """
    person = {"name": [name, "none"], "cpf": [cpf, "none"], "email": [email, "none"]}
    share = share.split(',')
    for element in share:
        person[element][1] = "share"
    print ("Saving data: " + str(person))
    personJSON = json.dumps(person)
    send_data(personJSON)

def send_data(dataInJSON, PORT=5041):
    print("Sending " + str(dataInJSON) + " through port " + str(PORT))
    client(bytes(dataInJSON, encoding="utf-8"), PORT)

@cli.command(name='issueRequest', help='Sends message to domain, informing stored data in another domain')
@click.option('-d', '--data', default='name,cpf,email', help='Data stored in domain that user wants to grant access')
@click.option('-o', '--dst_org', default='Org1', help='Domain that stores client data')
def issue_request(data, dst_org):
    """
    issueRequest sends a message to a server authorizing the
    request of the clients data that is stored in another domain.
    The client sends as argument the data that is stored in another
    domain, e.g., 'name,email', and the domain that stores it through
    the dst_org argument.
    """
    info = data.split(',')
    string_send = str(info) + "|" + dst_org
    send_data(string_send, 5042)


if __name__ == "__main__":
    cli()
