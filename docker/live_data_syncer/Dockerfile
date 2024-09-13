FROM 192.168.1.50:29006/tools/python-talib:py39-talib

ENV MIRROR=https://pypi.mirrors.ustc.edu.cn/simple
ENV PYTHONPATH=/dropbox/:/dropbox/ctpTrader
ENV RQDATAC2_CONF=rqdata://license:bRFOV6yI5yB4q6jEDHG6d8-CO7XIfm30vPiz5x6HEHo1Tdv0NmwKkzIVwRAXCD2GTlZ1saBStp5QoseqRaqDgxrQH2iwx9W0cX_oXFBKryxP315CUrwdnmJMANNFI6RkygqqHjtd8tEoquzZkNRLJsAfcIU7J4YfH_LV3Lr-VnM=C-EpgalM0c02FKu1xLi-F-vGmhe6l98EOZq9oNdSf_CqolOd_dYbOSg8wzU2NAX0t2wUvFfyOAyUHY2r30mVOORPFRC7KaUzm0QJQwSDwo5urLhbOw8KuzLJCggjZpHRVrndoleoP3NgTL-jitixt6Tk9JPImuni5vj4Jz6IR7c=@rqdatad-pro.ricequant.com:16011
ENV TZ=Asia/Shanghai
ENV CHUNK_SIZE=1000000
ENV CTP_TD_SERVER=tcp://180.168.146.187:10201
ENV CTP_MD_SERVER=tcp://180.168.146.187:10211
ENV CTP_BROKER_ID=9999
ENV CTP_USER_ID=224850
ENV CTP_PASSWORD=q9yvcbw7RuHv@Zs
ENV CTP_AUTH_CODE=0000000000000000
ENV CTP_APP_ID=simnow_client_test
ENV PERSIST_TYPE=kafka
ENV LANG=C.UTF-8
ENV UNDERLYING_LIST='["IO","HO"]'
ENV MATURITY_LIST='["2409","2410","2411"]'

WORKDIR /dropbox
ADD ctpTrader/docker/live_data_syncer/requirement.txt requirement.txt
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources && apt-get update && apt-get -y install locales locales-all
RUN pip install --no-cache-dir -i $MIRROR -r requirement.txt

ADD ctpTrader ctpTrader

ENTRYPOINT ["/usr/local/bin/python"]