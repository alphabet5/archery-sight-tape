FROM node as compress

COPY web /web
RUN mkdir /compressed
RUN npm install html-minifier -g
RUN html-minifier --collapse-whitespace --remove-comments --remove-optional-tags --remove-redundant-attributes --remove-script-type-attributes --remove-tag-whitespace --use-short-doctype --minify-css true --minify-js true -o /compressed/index.html /web/index.html


FROM golang as builder

RUN dpkgArch="$(dpkg --print-architecture)"; \
    case "$dpkgArch" in \
        arm) ARCH='arm' ;; \
        arm64) ARCH='arm64' ;; \
        amd64) ARCH='amd64' ;; \
        386) ARCH='386' ;; \
        *) echo >&2 "error: unsupported architecture: $apkArch"; exit 1 ;; \
    esac

RUN mkdir -p /app
RUN adduser --disabled-password --gecos "" --home /app --uid 1001 server
RUN mkdir -p /build
COPY main.go /build/main.go
COPY go.mod /build/go.mod

RUN cd /build && \
    go mod tidy && \
    CGO_ENABLED=0 GOOS=linux go build -trimpath -o '/app/server' ./main.go && \
    chmod +x /app/server && \
    chown -R 1001 /app/

FROM scratch

COPY --from=builder /app /app
COPY --from=compress /compressed /app/web
EXPOSE 8090

USER 1001
WORKDIR /app
ENTRYPOINT ["/app/server"]