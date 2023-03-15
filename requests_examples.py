import time
import requests

print('Отправка POST-запроса')
resp = requests.post('http://127.0.0.1:5000/upscale', files={
    'image': open('lama_300px.png', 'rb')
})

resp_data = resp.json()
print(resp_data)
task_id = resp_data.get('task_id')
print(task_id)


print('Отправка get-запроса на получение ответа 1 раз в 5 сек')
while True:
    resp = requests.get(f'http://127.0.0.1:5000/tasks/{task_id}')
    resp_data = resp.json()
    print(resp_data)
    status = resp_data['status']
    file_link = resp_data['file_link']
    if status != 'PENDING':
        break
    time.sleep(5)

print('Получение файла и запись его в файл result_file.png')
resp = requests.get(f'http://127.0.0.1:5000/processed/{file_link}')
if resp.status_code == 200:
    extension = file_link.split('.')[-1]
    file_name = f'result_file.{extension}'
    with open(file_name, 'wb') as f:
        f.write(resp.content)
    print(f'Файл успешно сохранен в {file_name}')
