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
def collect_data(name, cpf, email):
    person = {"name": name, "cpf": cpf, "email": email}
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
    info = data.split(',')
    string_send = str(info) + "|" + dst_org
    send_data(string_send, 5042)


if __name__ == "__main__":
    cli()
