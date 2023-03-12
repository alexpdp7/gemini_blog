import logging

import bicephalus
from bicephalus import main as bicephalus_main
from bicephalus import ssl
from bicephalus import otel


def handler(request: bicephalus.Request) -> bicephalus.Response:
    if request.proto == bicephalus.Proto.GEMINI:
        content = f"# Hello at {request.path}"
        content_type = "text/gemini"
    elif request.proto == bicephalus.Proto.HTTP:
        content = f"<html><body><h1>Hello at {request.path}</h1></body></html>"
        content_type = "text/html"
    else:
        assert False, f"unknown protocol {request.proto}"

    return bicephalus.Response(
        content=content.encode("utf8"),
        content_type=content_type,
        status=bicephalus.Status.OK,
    )


def main():
    otel.configure_logging(logging.INFO)
    with ssl.temporary_ssl_context("localhost") as ssl_context:
        bicephalus_main.main(handler, ssl_context, 8000)


if __name__ == "__main__":
    main()
