
FROM python:3.6.3
ADD ./test.py /
RUN ls -al
CMD python test.py