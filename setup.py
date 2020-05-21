#!/usr/bin/env python

from setuptools import setup
from setuptools import Extension
import os
import subprocess
import sys
import glob

if sys.platform == "darwin":
    extra_compile_args = "-stdlib=libc++ -std=c++11"
elif sys.platform != "win32":
    extra_compile_args = "-std=c++11"

def main():
    cpu_count = os.cpu_count() or 8
    version = "20200518"
    packages = [
        "hummingbot",
        "hummingbot.client",
        "hummingbot.client.command",
        "hummingbot.client.config",
        "hummingbot.client.ui",
        "hummingbot.core",
        "hummingbot.core.data_type",
        "hummingbot.core.event",
        "hummingbot.core.management",
        "hummingbot.core.utils",
        "hummingbot.data_feed",
        "hummingbot.logger",
        "hummingbot.market",
        "hummingbot.market.bamboo_relay",
        "hummingbot.market.binance",
        "hummingbot.market.bittrex",
        "hummingbot.market.coinbase_pro",
        "hummingbot.market.huobi",
        "hummingbot.market.radar_relay",
        "hummingbot.market.kraken",
        "hummingbot.strategy",
        "hummingbot.strategy.arbitrage",
        "hummingbot.strategy.cross_exchange_market_making",
        "hummingbot.strategy.pure_market_making",
        "hummingbot.templates",
        "hummingbot.wallet",
        "hummingbot.wallet.ethereum",
        "hummingbot.wallet.ethereum.uniswap",
        "hummingbot.wallet.ethereum.watcher",
        "hummingbot.wallet.ethereum.zero_ex",
    ]
    package_data = {
        "hummingbot": [
            "core/cpp/*",
            "wallet/ethereum/zero_ex/*.json",
            "wallet/ethereum/token_abi/*.json",
            "wallet/ethereum/erc20_tokens.json",
            "VERSION",
            "templates/*TEMPLATE.yml"
        ],
    }
    install_requires = [
        "cython==0.29.19",
        "aioconsole",
        "aiokafka",
        "attrdict",
        "cachetools",
        "cytoolz",
        "eth-abi",
        "eth-account",
        "eth-bloom",
        "eth-hash",
        "eth-keyfile",
        "eth-keys",
        "eth-rlp",
        "hexbytes",
        "lru-dict",
        "parsimonious",
        "pycryptodome",
        "ruamel.yaml",
        "requests",
        "rlp",
        "toolz",
        "tzlocal",
        "urllib3",
        "web3",
        "websockets",
        "aiohttp",
        "attrs",
        "certifi",
        "chardet",
        "idna; python_version<'3.7'",
        "idna_ssl; python_version<'3.7'",
        "multidict",
        "numpy",
        "pandas",
        "pytz",
        "pyyaml",
        "pyasn1",
        "python-binance==0.7.1",
        "sqlalchemy",
        "ujson",
        "yarl",
    ]

    ext_include = ["hummingbot/core", "hummingbot/core", "hummingbot/core/data_type"]
    try:
        import numpy as np
        ext_include += [np.get_include()]
    except Exception:
        pass

    ext_modules = []
    for package in packages:
        path = package.replace(".", "/") + "/*.pyx"
        for pyxfile in glob.glob(path):
            module = pyxfile.replace(".", "/")[:-4]
            ext_modules.append(
                Extension(
                    module,
                    [pyxfile],
                    include_dirs=ext_include,
                    language="c++",
                    extra_compile_args=extra_compile_args
                )
            )

    for e in ext_modules:
        e.cython_directives = {'language_level': "3"}


    if "DEV_MODE" in os.environ:
        version += ".dev1"
        package_data[""] = [
            "*.pxd", "*.pyx", "*.h"
        ]
        package_data["hummingbot"].append("core/cpp/*.cpp")

    if len(sys.argv) > 1 and sys.argv[1] == "build_ext" and sys.platform != "win32":
        sys.argv.append(f"--parallel={cpu_count}")

    setup(name="hummingbot",
          version=version,
          description="Hummingbot",
          url="https://github.com/CoinAlpha/hummingbot",
          author="CoinAlpha, Inc.",
          author_email="dev@hummingbot.io",
          license="Apache 2.0",
          packages=packages,
          package_data=package_data,
          install_requires=install_requires,
          setup_requires=[
              "setuptools>=18.0", # Handles Cython extensions natively
              "cython==0.29.19",
              "numpy"
          ],
          ext_modules=ext_modules,
          scripts=[
              "bin/hummingbot.py",
              "bin/hummingbot_quickstart.py"
          ],
          )


if __name__ == "__main__":
    main()
