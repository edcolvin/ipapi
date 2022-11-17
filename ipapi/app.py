from flask import Flask, url_for, request
from ipaddress import (
    ip_network,
    ip_address,
    IPv4Address,
    IPv6Address,
    IPv4Network,
    IPv6Network,
)

HTTP_BAD_REQUEST = 400

app = Flask(__name__)


def error_response(err_type: str, title: str, status: int, detail: str, instance: str):
    return (
        {
            "type": err_type,
            "title": title,
            "status": status,
            "detail": detail,
            "instance": instance,
        },
        status,
    )


def network_url(netw: "IPv4Network | IPv6Network"):
    return url_for(
        ".network", addr=netw.network_address, prefix=netw.prefixlen, _external=True
    )


def serialize_addr(addr: str):
    ipaddr: "IPv4Address | IPv6Address" = ip_address(addr)
    return {
        "address": str(ipaddr),
        "network": network_url(ip_network(f"{addr}/{ipaddr.max_prefixlen}")),
        "is_multicast": ipaddr.is_multicast,
        "is_loopback": ipaddr.is_loopback,
        "is_global": ipaddr.is_loopback,
        "is_link_local": ipaddr.is_link_local,
        "is_loopback": ipaddr.is_loopback,
        "is_multicast": ipaddr.is_multicast,
        "is_private": ipaddr.is_private,
        "is_reserved": ipaddr.is_reserved,
        "is_unspecified": ipaddr.is_unspecified,
        "version": ipaddr.version,
        "compressed": ipaddr.compressed,
        "exploded": ipaddr.exploded,
    }


def serialize_network(addr, prefix):
    netw: "IPv4Network | IPv6Network" = ip_network(f"{addr}/{prefix}", strict=False)
    return {
        "broadcast_address": str(netw.broadcast_address),
        "compressed": netw.compressed,
        "exploded": netw.exploded,
        "hostmask": str(netw.hostmask),
        "is_global": netw.is_global,
        "is_link_local": netw.is_link_local,
        "is_loopback": netw.is_loopback,
        "is_multicast": netw.is_multicast,
        "is_private": netw.is_private,
        "is_reserved": netw.is_reserved,
        "is_unspecified": netw.is_unspecified,
        "max_prefixlen": netw.max_prefixlen,
        "netmask": str(netw.netmask),
        "network_address": str(netw.network_address),
        "num_addresses": netw.num_addresses,
        "prefixlen": netw.prefixlen,
        "reverse_pointer": netw.reverse_pointer,
        "subnets": [network_url(subnet) for subnet in netw.subnets()],
        "supernet": network_url(netw.supernet()),
        "version": netw.version,
        "with_hostmask": netw.with_hostmask,
        "with_netmask": netw.with_netmask,
        "with_prefixlen": netw.with_prefixlen,
    }


@app.route("/address/<string:addr>")
def address(addr: int):
    try:
        return serialize_addr(addr)
    except ValueError as err:
        return error_response(
            "ValueError",
            "Error processing address request.",
            HTTP_BAD_REQUEST,
            str(err),
            request.url,
        )


@app.route("/network/<string:addr>/<int:prefix>")
def network(addr: int, prefix: int):
    try:
        return serialize_network(addr, prefix)
    except ValueError as err:
        return error_response(
            "ValueError",
            "Error processing network request.",
            HTTP_BAD_REQUEST,
            str(err),
            request.url,
        )
