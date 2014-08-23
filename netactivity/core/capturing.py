from ..models import Client, TargetHost, NetSession


def register_session(date_occurred, client_ip, destination_ip, port):
    destination, created = TargetHost.objects.get_or_create(ip_address=destination_ip)
    client, created = Client.objects.get_or_create(last_ip_address=client_ip)
    session = NetSession(target_host=destination, client=client, port=port, date_created=date_occurred)
    session.save()