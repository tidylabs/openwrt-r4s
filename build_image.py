#!/usr/bin/env python3

import os
import shutil
import subprocess
import tarfile

from pathlib import Path
from urllib.request import urlretrieve
from urllib.parse import urlparse

VERSION = "22.03.4"
TARGET = "rockchip"
SUBTARGET = "armv8"
PROFILE = "friendlyarm_nanopi-r4s"
PACKAGES = [
    "firewall", "ip6tables-legacy", "iptables-legacy", "kmod-ipt-offload",
    "luci-ssl", "-firewall4", "-nftables", "-kmod-nft-offload"
]
EXTRA_PACKAGES = [
]

URL_IMAGEBUILDER = f"https://downloads.openwrt.org/releases/{VERSION}/targets/{TARGET}/{SUBTARGET}/openwrt-imagebuilder-{VERSION}-{TARGET}-{SUBTARGET}.Linux-x86_64.tar.xz"


def urldownload(url, path="."):
    abs_path = os.path.abspath(path)
    if not os.path.isdir(abs_path):
        os.makedirs(abs_path)

    url_path = urlparse(url).path
    filename = os.path.basename(url_path)
    out_path = os.path.join(abs_path, filename)

    print(f"Downloading {filename}")
    return urlretrieve(url, out_path)[0]


if __name__ == "__main__":
    imagebuilder_tar = urldownload(URL_IMAGEBUILDER)
    with tarfile.open(name=imagebuilder_tar) as tar_file:
        tar_file.extractall()

    os.chdir(
        f"openwrt-imagebuilder-{VERSION}-{TARGET}-{SUBTARGET}.Linux-x86_64")

    for package_url in EXTRA_PACKAGES:
        urldownload(package_url, "./packages/")

    subprocess.run([
        "make", "image", f"PROFILE={PROFILE}", f"PACKAGES={' '.join(PACKAGES)}"
    ]).check_returncode()

    bin_dir = Path(f"./bin/targets/{TARGET}/{SUBTARGET}/")
    for image_file in bin_dir.glob(f"openwrt-{VERSION}-{TARGET}-{SUBTARGET}-{PROFILE}-*-sysupgrade.img.gz"):
        print(f"Copying {image_file.name}")
        shutil.copy(image_file, "..")

