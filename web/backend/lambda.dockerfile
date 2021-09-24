FROM amazon/aws-lambda-python

RUN yum -y groupinstall "Development Tools"

# python requirements
RUN python3 -m ensurepip
COPY web/backend/requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install mangum

# python piro module
COPY setup.py ${LAMBDA_TASK_ROOT}
COPY piro ${LAMBDA_TASK_ROOT}/piro
RUN pip install -e .

# python backend api code
COPY web/backend/app ${LAMBDA_TASK_ROOT}/app

ENV ENABLE_REACT=0

CMD ["app.lambda.handler"]