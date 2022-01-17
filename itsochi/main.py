import json
import requests
import typer
import os
import shutil


def main():
    base_dir = 'content/jobs'
    base_api_url = 'https://api.hh.ru/vacancies?'
    # urbamatica_vacancy = requests.get()
    yandex_vacancy = requests.get(
        f'{base_api_url}area=237&area=2377&specialization=1&per_page=90&employer_id=1740')

    tinkoff_vacancy = requests.get(
        f'{base_api_url}area=237&area=2377&specialization=1&per_page=20&employer_id=78638')

    wellyes_vacancy = requests.get(
        f'{base_api_url}area=237&area=2377&specialization=1&per_page=20&employer_id=2568447')

    other_vacancy = requests.get(f'{base_api_url}area=237&area=2377&specialization=1&per_page=4')

    content = {yandex_vacancy, tinkoff_vacancy, wellyes_vacancy, other_vacancy}

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
        if os.path.exists(f'{base_dir}/{company["id"]}'):
            make_vacancy(base_dir, company, vacancy)
        else:
            make_employer(base_dir, company)  # Else create directory of company
            make_vacancy(base_dir, company, vacancy)  # Add vacancy in existing company


def make_job_dir(base_dir):
    os.mkdir(base_dir)
    with open(f'{base_dir}/contents.lr', 'w') as f:
        f.write(f'_model: job')
    with open(f'{base_dir}/contents+en.lr', 'w') as f:
        f.write(f'_model: job')
    with open(f'{base_dir}/contents+ru.lr', 'w') as f:
        f.write(f'_model: job')


def make_employer(base_dir, company):
    os.mkdir(f'{base_dir}/{company["id"]}')
    with open(f'{base_dir}/{company["id"]}/contents.lr', 'w') as f:
        f.write(f'title: {company["name"]}\n')
    with open(f'{base_dir}/{company["id"]}/contents+en.lr', 'w') as f:
        f.write(f'title: {company["name"]}\n')
    with open(f'{base_dir}/{company["id"]}/contents+ru.lr', 'w') as f:
        f.write(f'title: {company["name"]}\n')


def make_vacancy(base_dir, company, vacancy):
    if not(os.path.exists(f'{base_dir}/{company["id"]}/{vacancy["id"]}')):
        os.mkdir(f'{base_dir}/{company["id"]}/{vacancy["id"]}')
        with open(f'{base_dir}/{company["id"]}/{vacancy["id"]}/contents.lr', 'w') as f:
            f.write(f'title:{vacancy["name"]}'
                    f'\n---\n'
                    f'url:{vacancy["alternate_url"]}')
        with open(f'{base_dir}/{company["id"]}/{vacancy["id"]}/contents+en.lr', 'w') as f:
            f.write(f'title:{vacancy["name"]}'
                    f'\n---\n'
                    f'url:{vacancy["alternate_url"]}')
        with open(f'{base_dir}/{company["id"]}/{vacancy["id"]}/contents+ru.lr', 'w') as f:
            f.write(f'title:{vacancy["name"]}'
                    f'\n---\n'
                    f'url:{vacancy["alternate_url"]}')


if __name__ == "__main__":
    typer.run(main)