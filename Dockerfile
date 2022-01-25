FROM python
WORKDIR /tests_project/
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV ENV=prod
CMD python -m pytest -s --alluredir=test_results/ /tests_project/tests/

# docker pull python
# docker build -t pytest_runner
# docker run --rm --mount type=bind,src= C:\Users\a\Desktop\API,target=/tests/tests_project/ pytest_runner

# --rm - контейнер будет автоматически удален
# --mount - подтягиваем все в контейнер
# target - созданный образ, от которого стартует контейнер
#
#
#
#
#
#
#
#
#
#
#