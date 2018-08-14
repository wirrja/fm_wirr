FROM ubuntu:18.04


RUN apt-get update -y && apt-get upgrade -y \
	&& apt-get install -y python3-dev python3-pip \
	&& apt-get install -y build-essential nginx-light \
	&& apt-get autoremove -y \
	&& apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 

WORKDIR /opt/app

ADD requirements.txt /opt/app
ADD . /opt/app
ADD etc/ /etc/

RUN pip3 install --no-cache-dir -r requirements.txt \
	&& python3 -c 'import compileall, os; compileall.compile_dir(os.curdir, force=1)' > /dev/null 

CMD ["circusd", "/etc/circus/web.ini"]
