FROM python:3.8.6-slim

ENV APP_HOME /app
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY . /app

RUN pip install --upgrade pip
RUN pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install -r requirements.txt

ADD https://cdn.huggingface.co/deepset/bert-large-uncased-whole-word-masking-squad2/config.json /app/index/bert/
ADD https://cdn.huggingface.co/deepset/bert-large-uncased-whole-word-masking-squad2/pytorch_model.bin /app/index/bert/
ADD https://cdn.huggingface.co/deepset/bert-large-uncased-whole-word-masking-squad2/special_tokens_map.json /app/index/bert/
ADD https://cdn.huggingface.co/deepset/bert-large-uncased-whole-word-masking-squad2/tokenizer_config.json /app/index/bert/
ADD https://cdn.huggingface.co/deepset/bert-large-uncased-whole-word-masking-squad2/vocab.txt /app/index/bert/

EXPOSE 8080

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8080", "app:create_app()"]