#! /usr/bin/python

from argparse import ArgumentParser

parser = ArgumentParser(description="Creates labels required by docker containers that need to be routed through Traefik.")

parser.add_argument("service", action="store")
parser.add_argument("cname", action="store")
parser.add_argument("-p", "--port", action="store")
parser.add_argument("-s", "--scheme", action="store")
parser.add_argument("-n", "--network", action="store")
parser.add_argument("-i", "--instance", action="store")

args = parser.parse_args()

template = '''
labels:
  - "traefik.enable=true"
  - "traefik.docker.network={netInternal}"
  - "io.traefik.instance={traefikInstance}"
  - "traefik.http.routers.{serviceInternal}-secure.entrypoints=https"
  - "traefik.http.routers.{serviceInternal}-secure.rule=Host(`{domainCNAME}.ratsnest.dev`)"
  - "traefik.http.routers.{serviceInternal}-secure.tls=true"
  - "traefik.http.services.{serviceInternal}.loadbalancer.server.port={portInternal}"
  - "traefik.http.services.{serviceInternal}.loadbalancer.server.scheme={schemeInternal}"
'''

def main():
    if args.port != None:
        if args.port.isdigit():
            if int(args.port) > 0 and int(args.port) <= 65535:
                port = args.port
            else:
                print("Port assignment must be an integer between 1 and 65535")
                return
        else:
            print("Port assignment must a number")
            return
    else:
        port = "80"

    if args.scheme != None:
        if args.scheme == "http" or args.scheme == "https":
            scheme = args.scheme
        else:
            print("scheme must be http or https")
            return
    else:
        scheme = "http"

    if args.network != None:
        network = args.network
    else:
        network = "backend"

    if args.instance != None:
        instance = args.instance
    else:
        instance = "private"

    print(template.format(serviceInternal=args.service, domainCNAME=args.cname, netInternal=network, portInternal=port, schemeInternal=scheme, traefikInstance=instance))

if __name__ == "__main__":
    main()
