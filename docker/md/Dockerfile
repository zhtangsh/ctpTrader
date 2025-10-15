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
# 使用传统 sources.list 避免 deb822 格式问题
RUN rm -f /etc/apt/sources.list.d/*.sources && \
    echo "deb https://mirrors.aliyun.com/debian bookworm main contrib non-free" > /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian bookworm-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list
# 安装依赖
RUN apt-get update --allow-insecure-repositories && apt-get -y install --allow-unauthenticated locales locales-all sudo dmidecode iproute2 net-tools procps && rm -rf /var/lib/apt/lists/*

ADD ctpTrader/docker/md/requirement.txt requirement.txt
RUN pip install --no-cache-dir -i $MIRROR -r requirement.txt

ADD ctpTrader ctpTrader

ENTRYPOINT ["/usr/bin/bash","/dropbox/ctpTrader/runMd.sh"]