ARG ARCH=
FROM ${ARCH}alpine:3.12
LABEL maintainer="info@cstan.io"

# install packages
RUN apk update && apk add ansible-lint yamllint py3-flake8 py3-pip shellcheck && pip3 install pylint && rm -rf /var/cache/apk

# add entrypoint
ADD entrypoint.sh /entrypoint.sh

# volume configuration
VOLUME ["/data"]

# run linter
CMD /entrypoint.sh
