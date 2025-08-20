FROM 192.168.1.50:29006/tools/python-talib:py39-talib

ENV MIRROR=https://pypi.mirrors.ustc.edu.cn/simple
ENV PYTHONPATH=/dropbox/:/dropbox/ctpTrader
ENV TZ=Asia/Shanghai
ENV CHUNK_SIZE=1000000
ENV CTP_TD_SERVER=tcp://182.254.243.31:30001
ENV CTP_MD_SERVER=tcp://182.254.243.31:30011
ENV CTP_BROKER_ID=9999
ENV CTP_USER_ID=224850
ENV CTP_PASSWORD=LIZxihuyu@1128
ENV CTP_AUTH_CODE=0000000000000000
ENV CTP_APP_ID=simnow_client_test
ENV LANG=C.UTF-8

WORKDIR /dropbox
ADD ctpTrader/docker/md/requirement.txt requirement.txt
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources && apt-get update && apt-get -y install locales locales-all
RUN pip install --no-cache-dir -i $MIRROR -r requirement.txt

ADD ctpTrader ctpTrader

ENTRYPOINT ["/usr/bin/bash","/dropbox/ctpTrader/runMd.sh"]