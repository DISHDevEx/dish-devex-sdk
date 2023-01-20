#FROM public.ecr.aws/amazonlinux/amazonlinux:2.0.20221210.1-amd64 AS base
FROM --platform=linux/amd64 amazonlinux:2 AS base
RUN yum install -y python3 git

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip3 install git+https://github.com/DISHDevEx/dish-devex-sdk.git
RUN pip3 install git+https://github.com/DISHDevEx/eks-ml-pipeline.git
WORKDIR /app
COPY . .
RUN pip3 install venv-pack==0.2.0
RUN  pip3 install boto3
RUN  pip3 install pyarrow
RUN  pip3 install awswrangler
RUN  pip3 install fast-arrow
RUN  pip3 install tf2onnx
RUN pwdxx

RUN mkdir /output && venv-pack -o /output/pyspark_deps_github.tar.gz

FROM scratch AS export
COPY --from=base /output/pyspark_deps_github.tar.gz /