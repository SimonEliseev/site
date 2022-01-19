import json
import requests
import typer
import os
import shutil


def main():
    base_dir = 'content/jobs'
    base_api_url = 'https://api.hh.ru/vacancies?'
    urbamatica_vacancy = requests.get(
        f'{base_api_url}area=237&area=2377&specialization=1&per_page=90&employer_id=5461019')

    yandex_vacancy = requests.get(
        f'{base_api_url}area=237&area=2377&specialization=1&per_page=90&employer_id=1740')

    tinkoff_vacancy = requests.get(
        f'{base_api_url}area=237&area=2377&specialization=1&per_page=20&employer_id=78638')

    wellyes_vacancy = requests.get(
        f'{base_api_url}area=237&area=2377&specialization=1&per_page=20&employer_id=2568447')

    other_vacancy = requests.get(f'{base_api_url}area=237&area=2377&specialization=1&per_page=4')

    content = {urbamatica_vacancy, yandex_vacancy, tinkoff_vacancy, wellyes_vacancy, other_vacancy}

    # If directory exist then re-create again else just create directory
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
        make_job_dir(base_dir)
    else:
        make_job_dir(base_dir)

    for element in content:
        fill_content(base_dir, element)


def fill_content(base_dir, response):
    data = json.loads(response.text)
    vacancies = data['items']

    for vacancy in vacancies:
        # Take company from vacancy
        company = vacancy["employer"]
        # If directory exist then add new vacancy
        if os.path.exists(f'{base_dir}/{vacancy["employer"]["id"]}'):
            make_vacancy(base_dir, vacancy)
        else:
            make_employer(base_dir, vacancy)  # Else create directory of company
            make_vacancy(base_dir, vacancy)  # Add vacancy in existing company


def make_job_dir(base_dir):
    os.mkdir(base_dir)
    create_job_file(base_dir, "contents.lr")
    create_job_file(base_dir, "contents+en.lr")
    create_job_file(base_dir, "contents+ru.lr")


def create_job_file(base_dir, file_name):
    with open(f'{base_dir}/{file_name}', 'w') as f:
        f.write(f'_model: job')


def make_employer(base_dir, vacancy):
    os.mkdir(f'{base_dir}/{vacancy["employer"]["id"]}')
    create_employer_file(base_dir, vacancy, "contents.lr")
    create_employer_file(base_dir, vacancy, "contents+en.lr")
    create_employer_file(base_dir, vacancy, "contents+ru.lr")


def create_employer_file(base_dir, vacancy, file_name):
    with open(f'{base_dir}/{vacancy["employer"]["id"]}/{file_name}', 'w') as f:
        f.write(f'title: {vacancy["employer"]["name"]}\n')


def make_vacancy(base_dir, vacancy):
    if not (os.path.exists(f'{base_dir}/{vacancy["employer"]["id"]}/{vacancy["id"]}')):
        os.mkdir(f'{base_dir}/{vacancy["employer"]["id"]}/{vacancy["id"]}')
        create_vacancy_file(base_dir, vacancy, "contents.lr")
        create_vacancy_file(base_dir, vacancy, "contents+en.lr")
        create_vacancy_file(base_dir, vacancy, "contents+ru.lr")


def create_vacancy_file(base_dir, vacancy, file_name):
    with open(f'{base_dir}/{vacancy["employer"]["id"]}/{vacancy["id"]}/{file_name}', 'w') as f:
        f.write(f'title:{vacancy["name"]}'
                f'\n---\n'
                f'url:{vacancy["alternate_url"]}'
                f'\n---\n'
                f'schedule:{vacancy["schedule"]["name"]}')


if __name__ == "__main__":
    typer.run(main)
