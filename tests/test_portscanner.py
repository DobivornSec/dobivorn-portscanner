import ipaddress
import pytest
import subprocess
import sys

from portscanner import parse_cidr, parse_ports


def test_parse_ports_range_and_list_combined():
    assert parse_ports("22,80-82,443") == [22, 80, 81, 82, 443]


def test_parse_ports_deduplicates_and_sorts():
    assert parse_ports("443,80,443,22") == [22, 80, 443]


@pytest.mark.parametrize("value", ["", "a", "70000", "100-20", "22-"])
def test_parse_ports_invalid(value):
    with pytest.raises(ValueError):
        parse_ports(value)


def test_parse_cidr_valid():
    cidr = "192.168.1.0/30"
    expected = [str(ip) for ip in ipaddress.ip_network(cidr, strict=False).hosts()]
    assert parse_cidr(cidr) == expected


def test_parse_cidr_invalid():
    with pytest.raises(ValueError):
        parse_cidr("192.168.1.0/99")


def test_cli_rejects_invalid_port_argument():
    result = subprocess.run(
        [sys.executable, "portscanner.py", "127.0.0.1", "-p", "70000"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "Gecersiz port parametresi" in result.stdout


def test_cli_rejects_invalid_cidr():
    result = subprocess.run(
        [sys.executable, "portscanner.py", "192.168.1.0/99"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "Geçersiz CIDR formatı" in result.stdout
