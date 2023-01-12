FROM alpine:latest as icarus-build
# RUN apk add --no-cache g++ git autoconf make bison flex gperf
# RUN git clone https://github.com/steveicarus/iverilog
# WORKDIR /iverilog
# RUN sh autoconf.sh
# RUN ./configure --prefix /build
# RUN make -j$(nproc)
# RUN make install

FROM alpine:latest AS run
RUN apk add --no-cache iverilog --repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing/

# COPY --from=icarus-build /build* /usr/local/
